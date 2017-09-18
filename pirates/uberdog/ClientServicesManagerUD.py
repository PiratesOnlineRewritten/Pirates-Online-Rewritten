import semidbm
import base64
import hashlib
import hmac
import json
import time
import urllib2
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.fsm.FSM import FSM
from pandac.PandaModules import *
from otp.distributed import OtpDoGlobals
from pirates.pirate.HumanDNA import HumanDNA

# Import from PyCrypto only if we are using a database that requires it. This
# allows local hosted and developer builds of the game to run without it:
accountDBType = simbase.config.GetString('accountdb-type', 'developer')
if accountDBType == 'remote':
    from Crypto.Cipher import AES

# Sometimes we'll want to force a specific access level, such as on the
# developer server:
minAccessLevel = simbase.config.GetInt('min-access-level', 100)
accountServerEndpoint = simbase.config.GetString('account-server-endpoint', 'https://toontowninfinite.com/api/')
accountServerSecret = simbase.config.GetString('account-server-secret', '6163636f756e7473')

http = HTTPClient()
http.setVerifySsl(0)

def executeHttpRequest(url, **extras):
    timestamp = str(int(time.time()))
    signature = hmac.new(accountServerSecret, timestamp, hashlib.sha256)
    request = urllib2.Request(accountServerEndpoint + url)
    request.add_header('User-Agent', 'TTI-CSM')
    request.add_header('X-CSM-Timestamp', timestamp)
    request.add_header('X-CSM-Signature', signature.hexdigest())
    for k, v in extras.items():
        request.add_header('X-CSM-' + k, v)
    try:
        return urllib2.urlopen(request).read()
    except:
        return None

blacklist = executeHttpRequest('names/blacklist.json')
if blacklist:
    blacklist = json.loads(blacklist)

def judgeName(name):
    if not name:
        return False

    if blacklist:
        for namePart in name.split(' '):
            namePart = namePart.lower()
            if len(namePart) < 1:
                return False

            for banned in blacklist.get(namePart[0], []):
                if banned in namePart:
                    return False
    return True

# --- ACCOUNT DATABASES ---
# These classes make up the available account databases for Toontown Infinite.
# Databases with login tokens use the PyCrypto module for decrypting them.
# DeveloperAccountDB is a special database that accepts a username, and assigns
# each user with 600 access automatically upon login.

class AccountDB:
    notify = directNotify.newCategory('AccountDB')

    def __init__(self, csm):
        self.csm = csm

        filename = simbase.config.GetString(
            'account-bridge-filename', 'account-bridge')
        self.dbm = semidbm.open(filename, 'c')

    def addNameRequest(self, avId, name):
        return 'Success'

    def getNameStatus(self, avId):
        return 'APPROVED'

    def removeNameRequest(self, avId):
        return 'Success'

    def lookup(self, username, callback):
        pass  # Inheritors should override this.

    def storeAccountID(self, userId, accountId, callback):
        self.dbm[str(userId)] = str(accountId)  # semidbm only allows strings.
        if getattr(self.dbm, 'sync', None):
            self.dbm.sync()
            callback(True)
        else:
            self.notify.warning('Unable to associate user %s with account %d!' % (userId, accountId))
            callback(False)


class DeveloperAccountDB(AccountDB):
    notify = directNotify.newCategory('DeveloperAccountDB')

    def lookup(self, username, callback):
        # Let's check if this user's ID is in your account database bridge:
        if str(username) not in self.dbm:

            # Nope. Let's associate them with a brand new Account object! We
            # will assign them with 600 access just because they are a
            # developer:
            response = {
                'success': True,
                'userId': username,
                'accountId': 0,
                'accessLevel': max(600, minAccessLevel)
            }
            callback(response)
            return response

        else:

            # We have an account already, let's return what we've got:
            response = {
                'success': True,
                'userId': username,
                'accountId': int(self.dbm[str(username)]),
            }
            callback(response)
            return response


# This is the same as the DeveloperAccountDB, except it doesn't automatically
# give the user an access level of 600. Instead, the first user that is created
# gets 700 access, and every user created afterwards gets 100 access:

class LocalAccountDB(AccountDB):
    notify = directNotify.newCategory('LocalAccountDB')

    def lookup(self, username, callback):
        # Let's check if this user's ID is in your account database bridge:
        if str(username) not in self.dbm:

            # Nope. Let's associate them with a brand new Account object!
            response = {
                'success': True,
                'userId': username,
                'accountId': 0,
                'accessLevel': max((700 if not self.dbm else 100), minAccessLevel)
            }
            callback(response)
            return response

        else:

            # We have an account already, let's return what we've got:
            response = {
                'success': True,
                'userId': username,
                'accountId': int(self.dbm[str(username)])
            }
            callback(response)
            return response


class RemoteAccountDB(AccountDB):
    notify = directNotify.newCategory('RemoteAccountDB')

    def addNameRequest(self, avId, name):
        return executeHttpRequest('names/append', ID=str(avId), Name=name)

    def getNameStatus(self, avId):
        return executeHttpRequest('names/status/?Id=' + str(avId))

    def removeNameRequest(self, avId):
        return executeHttpRequest('names/remove', ID=str(avId))

    def lookup(self, token, callback):
        # First, base64 decode the token:
        try:
            token = base64.b64decode(token)
        except TypeError:
            self.notify.warning('Could not decode the provided token!')
            response = {
                'success': False,
                'reason': "Can't decode this token."
            }
            callback(response)
            return response

        # Ensure this token is a valid size:
        if (not token) or ((len(token) % 16) != 0):
            self.notify.warning('Invalid token length!')
            response = {
                'success': False,
                'reason': 'Invalid token length.'
            }
            callback(response)
            return response

        # Next, decrypt the token using AES-128 in CBC mode:
        accountServerSecret = simbase.config.GetString(
            'account-server-secret', '6163636f756e7473')

        # Ensure that our secret is the correct size:
        if len(accountServerSecret) > AES.block_size:
            self.notify.warning('account-server-secret is too big!')
            accountServerSecret = accountServerSecret[:AES.block_size]
        elif len(accountServerSecret) < AES.block_size:
            self.notify.warning('account-server-secret is too small!')
            accountServerSecret += '\x80'
            while len(accountServerSecret) < AES.block_size:
                accountServerSecret += '\x00'

        # Take the initialization vector off the front of the token:
        iv = token[:AES.block_size]

        # Truncate the token to get our cipher text:
        cipherText = token[AES.block_size:]

        # Decrypt!
        cipher = AES.new(accountServerSecret, mode=AES.MODE_CBC, IV=iv)
        try:
            token = json.loads(cipher.decrypt(cipherText).replace('\x00', ''))
            if ('timestamp' not in token) or (not isinstance(token['timestamp'], int)):
                raise ValueError
            if ('userid' not in token) or (not isinstance(token['userid'], int)):
                raise ValueError
            if ('accesslevel' not in token) or (not isinstance(token['accesslevel'], int)):
                raise ValueError
        except ValueError, e:
            print e
            self.notify.warning('Invalid token.')
            response = {
                'success': False,
                'reason': 'Invalid token.'
            }
            callback(response)
            return response

        # Next, check if this token has expired:
        expiration = simbase.config.GetInt('account-token-expiration', 1800)
        tokenDelta = int(time.time()) - token['timestamp']
        if tokenDelta > expiration:
            response = {
                'success': False,
                'reason': 'This token has expired.'
            }
            callback(response)
            return response

        # This token is valid. That's all we need to know. Next, let's check if
        # this user's ID is in your account database bridge:
        if str(token['userid']) not in self.dbm:

            # Nope. Let's associate them with a brand new Account object!
            response = {
                'success': True,
                'userId': token['userid'],
                'accountId': 0,
                'accessLevel': max(int(token['accesslevel']), minAccessLevel)
            }
            callback(response)
            return response

        else:

            # Yep. Let's return their account ID and access level!
            response = {
                'success': True,
                'userId': token['userid'],
                'accountId': int(self.dbm[str(token['userid'])]),
                'accessLevel': max(int(token['accesslevel']), minAccessLevel)
            }
            callback(response)
            return response


# --- FSMs ---
class OperationFSM(FSM):
    TARGET_CONNECTION = False

    def __init__(self, csm, target):
        self.csm = csm
        self.target = target

        FSM.__init__(self, self.__class__.__name__)

    def enterKill(self, reason=''):
        if self.TARGET_CONNECTION:
            self.csm.killConnection(self.target, reason)
        else:
            self.csm.killAccount(self.target, reason)
        self.demand('Off')

    def enterOff(self):
        if self.TARGET_CONNECTION:
            del self.csm.connection2fsm[self.target]
        else:
            del self.csm.account2fsm[self.target]


class LoginAccountFSM(OperationFSM):
    notify = directNotify.newCategory('LoginAccountFSM')
    TARGET_CONNECTION = True

    def enterStart(self, token):
        self.token = token
        self.demand('QueryAccountDB')

    def enterQueryAccountDB(self):
        self.csm.accountDB.lookup(self.token, self.__handleLookup)

    def __handleLookup(self, result):
        if not result.get('success'):
            self.csm.air.writeServerEvent('tokenRejected', self.target, self.token)
            self.demand('Kill', result.get('reason', 'The account server rejected your token.'))
            return

        self.userId = result.get('userId', 0)
        self.accountId = result.get('accountId', 0)
        self.accessLevel = result.get('accessLevel', 0)
        if self.accountId:
            self.demand('RetrieveAccount')
        else:
            self.demand('CreateAccount')

    def enterRetrieveAccount(self):
        self.csm.air.dbInterface.queryObject(
            self.csm.air.dbId, self.accountId, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields
        self.demand('SetAccount')

    def enterCreateAccount(self):
        self.account = {
            'ACCOUNT_AV_SET': [0] * 6,
            'ESTATE_ID': 0,
            'ACCOUNT_AV_SET_DEL': [],
            'CREATED': time.ctime(),
            'LAST_LOGIN': time.ctime(),
            'ACCOUNT_ID': str(self.userId),
            'ACCESS_LEVEL': self.accessLevel
        }
        self.csm.air.dbInterface.createObject(
            self.csm.air.dbId,
            self.csm.air.dclassesByName['AccountUD'],
            self.account,
            self.__handleCreate)

    def __handleCreate(self, accountId):
        if self.state != 'CreateAccount':
            self.notify.warning('Received a create account response outside of the CreateAccount state.')
            return

        if not accountId:
            self.notify.warning('Database failed to construct an account object!')
            self.demand('Kill', 'Your account object could not be created in the game database.')
            return

        self.accountId = accountId
        self.csm.air.writeServerEvent('accountCreated', accountId)
        self.demand('StoreAccountID')

    def enterStoreAccountID(self):
        self.csm.accountDB.storeAccountID(
            self.userId,
            self.accountId,
            self.__handleStored)

    def __handleStored(self, success=True):
        if not success:
            self.demand('Kill', 'The account server could not save your user ID!')
            return

        self.demand('SetAccount')

    def enterSetAccount(self):
        # If necessary, update their account information:
        if self.accessLevel:
            self.csm.air.dbInterface.updateObject(
                self.csm.air.dbId,
                self.accountId,
                self.csm.air.dclassesByName['AccountUD'],
                {'ACCESS_LEVEL': self.accessLevel})

        # If there's anybody on the account, kill them for redundant login:
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.csm.GetAccountConnectionChannel(self.accountId),
            self.csm.air.ourChannel,
            CLIENTAGENT_EJECT)
        datagram.addUint16(100)
        datagram.addString('This account has been logged in from elsewhere.')
        self.csm.air.send(datagram)

        # Next, add this connection to the account channel.
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.target,
            self.csm.air.ourChannel,
            CLIENTAGENT_OPEN_CHANNEL)
        datagram.addChannel(self.csm.GetAccountConnectionChannel(self.accountId))
        self.csm.air.send(datagram)

        # Now set their sender channel to represent their account affiliation:
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.target,
            self.csm.air.ourChannel,
            CLIENTAGENT_SET_CLIENT_ID)

        # Account ID in high 32 bits, 0 in low (no avatar):
        datagram.addChannel(self.accountId << 32)
        self.csm.air.send(datagram)

        # Un-sandbox them!
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.target,
            self.csm.air.ourChannel,
            CLIENTAGENT_SET_STATE)

        datagram.addUint16(2)  # ESTABLISHED
        self.csm.air.send(datagram)

        # Update the last login timestamp:
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.accountId,
            self.csm.air.dclassesByName['AccountUD'],
            {'LAST_LOGIN': time.ctime(),
             'ACCOUNT_ID': str(self.userId)})

        # We're done.
        self.csm.air.writeServerEvent('accountLogin', self.target, self.accountId, self.userId)
        self.csm.sendUpdateToChannel(self.target, 'acceptLogin', [])
        self.demand('Off')

class CreateAvatarFSM(OperationFSM):
    notify = directNotify.newCategory('CreateAvatarFSM')

    def enterStart(self, dna, index):
        # Basic sanity-checking:
        if index >= 4:
            self.demand('Kill', 'Invalid index specified!')
            return

        if not HumanDNA().isValidNetString(dna):
            self.demand('Kill', 'Invalid DNA specified!')
            return

        self.index = index
        self.dna = dna

        # Okay, we're good to go, let's query their account.
        self.demand('RetrieveAccount')

    def enterRetrieveAccount(self):
        self.csm.air.dbInterface.queryObject(
            self.csm.air.dbId, self.target, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields

        self.avList = self.account['ACCOUNT_AV_SET']
        # Sanitize:
        self.avList = self.avList[:4]
        self.avList += [0] * (4-len(self.avList))

        # Make sure the index is open:
        if self.avList[self.index]:
            self.demand('Kill', 'This avatar slot is already taken by another avatar!')
            return

        # Okay, there's space. Let's create the avatar!
        self.demand('CreateAvatar')

    def enterCreateAvatar(self):
        pirateFields = {
            'setName': ('dbp',),
            'WishNameState': ('OPEN',),
            'WishName': ('',),
            'setDNAString': (self.dna,),
            'setDISLid': (self.target,)
        }

        self.csm.air.dbInterface.createObject(
            self.csm.air.dbId,
            self.csm.air.dclassesByName['DistributedPlayerPirateUD'],
            pirateFields,
            self.__handleCreate)

    def __handleCreate(self, avId):
        if not avId:
            self.demand('Kill', 'Database failed to create the new avatar object!')
            return

        self.avId = avId
        self.demand('StoreAvatar')

    def enterStoreAvatar(self):
        # Associate the avatar with the account...
        self.avList[self.index] = self.avId
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.target,
            self.csm.air.dclassesByName['AccountUD'],
            {'ACCOUNT_AV_SET': self.avList},
            {'ACCOUNT_AV_SET': self.account['ACCOUNT_AV_SET']},
            self.__handleStoreAvatar)

    def __handleStoreAvatar(self, fields):
        if fields:
            self.demand('Kill', 'Database failed to associate the new avatar to your account!')
            return

        # Otherwise, we're done!
        self.csm.air.writeServerEvent('avatarCreated', self.avId, self.target, self.dna.encode('hex'), self.index)
        self.csm.sendUpdateToAccountId(self.target, 'createAvatarResp', [self.avId])
        self.demand('Off')


class AvatarOperationFSM(OperationFSM):
    POST_ACCOUNT_STATE = 'Off'  # This needs to be overridden.

    def enterRetrieveAccount(self):
        # Query the account:
        self.csm.air.dbInterface.queryObject(
            self.csm.air.dbId, self.target, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields

        self.avList = self.account['ACCOUNT_AV_SET']
        # Sanitize:
        self.avList = self.avList[:6]
        self.avList += [0] * (6-len(self.avList))

        self.demand(self.POST_ACCOUNT_STATE)


class GetAvatarsFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('GetAvatarsFSM')
    POST_ACCOUNT_STATE = 'QueryAvatars'

    def enterStart(self):
        self.demand('RetrieveAccount')

    def enterQueryAvatars(self):
        self.pendingAvatars = set()
        self.avatarFields = {}
        for avId in self.avList:
            if avId:
                self.pendingAvatars.add(avId)

                def response(dclass, fields, avId=avId):
                    if self.state != 'QueryAvatars':
                        return
                    if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
                        self.demand('Kill', "One of the account's avatars is invalid!")
                        return
                    self.avatarFields[avId] = fields
                    self.pendingAvatars.remove(avId)
                    if not self.pendingAvatars:
                        self.demand('SendAvatars')

                self.csm.air.dbInterface.queryObject(
                    self.csm.air.dbId,
                    avId,
                    response)

        if not self.pendingAvatars:
            self.demand('SendAvatars')

    def enterSendAvatars(self):
        potentialAvs = []

        for avId, fields in self.avatarFields.items():
            index = self.avList.index(avId)
            wishNameState = fields.get('WishNameState', [''])[0]
            name = fields['setName'][0]
            nameState = 0

            if wishNameState == 'OPEN':
                nameState = 1
            elif wishNameState == 'PENDING':
                actualNameState = self.csm.accountDB.getNameStatus(avId)
                self.csm.air.dbInterface.updateObject(
                    self.csm.air.dbId,
                    avId,
                    self.csm.air.dclassesByName['DistributedPlayerPirateUD'],
                    {'WishNameState': [actualNameState]}
                )
                if actualNameState == 'PENDING':
                    nameState = 2
                if actualNameState == 'APPROVED':
                    nameState = 3
                    name = fields['WishName'][0]
                elif actualNameState == 'REJECTED':
                    nameState = 4
            elif wishNameState == 'APPROVED':
                nameState = 3
            elif wishNameState == 'REJECTED':
                nameState = 4

            potentialAvs.append([avId, name, fields['setDNAString'][0],
                                 index, nameState])

        self.csm.sendUpdateToAccountId(self.target, 'setAvatars', [potentialAvs])
        self.demand('Off')

# This inherits from GetAvatarsFSM, because the delete operation ends in a
# setAvatars message being sent to the client.
class DeleteAvatarFSM(GetAvatarsFSM):
    notify = directNotify.newCategory('DeleteAvatarFSM')
    POST_ACCOUNT_STATE = 'ProcessDelete'

    def enterStart(self, avId):
        self.avId = avId
        GetAvatarsFSM.enterStart(self)

    def enterProcessDelete(self):
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to delete an avatar not in the account!')
            return

        index = self.avList.index(self.avId)
        self.avList[index] = 0

        avsDeleted = list(self.account.get('ACCOUNT_AV_SET_DEL', []))
        avsDeleted.append([self.avId, int(time.time())])

        estateId = self.account.get('ESTATE_ID', 0)

        if estateId != 0:
            # This assumes that the house already exists, but it shouldn't
            # be a problem if it doesn't.
            self.csm.air.dbInterface.updateObject(
                self.csm.air.dbId,
                estateId,
                self.csm.air.dclassesByName['DistributedEstateAI'],
                {'setSlot%dToonId' % index: [0],
                 'setSlot%dItems' % index: [[]]}
            )

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.target,
            self.csm.air.dclassesByName['AccountUD'],
            {'ACCOUNT_AV_SET': self.avList,
             'ACCOUNT_AV_SET_DEL': avsDeleted},
            {'ACCOUNT_AV_SET': self.account['ACCOUNT_AV_SET'],
             'ACCOUNT_AV_SET_DEL': self.account['ACCOUNT_AV_SET_DEL']},
            self.__handleDelete)
        self.csm.accountDB.removeNameRequest(self.avId)

    def __handleDelete(self, fields):
        if fields:
            self.demand('Kill', 'Database failed to mark the avatar as deleted!')
            return

        self.csm.air.writeServerEvent('avatarDeleted', self.avId, self.target)
        self.demand('QueryAvatars')

class SetNameTypedFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('SetNameTypedFSM')
    POST_ACCOUNT_STATE = 'RetrieveAvatar'

    def enterStart(self, avId, name):
        self.avId = avId
        self.name = name

        if self.avId:
            self.demand('RetrieveAccount')
            return

        # Hmm, self.avId was 0. Okay, let's just cut to the judging:
        self.demand('JudgeName')

    def enterRetrieveAvatar(self):
        if self.avId and self.avId not in self.avList:
            self.demand('Kill', 'Tried to name an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        if fields['WishNameState'][0] != 'OPEN':
            self.demand('Kill', 'Avatar is not in a namable state!')
            return

        self.demand('JudgeName')

    def enterJudgeName(self):
        # Let's see if the name is valid:
        status = judgeName(self.name)

        if self.avId and status:
            resp = self.csm.accountDB.addNameRequest(self.avId, self.name)
            if resp != 'Success':
                status = False
            else:
                self.csm.air.dbInterface.updateObject(
                    self.csm.air.dbId,
                    self.avId,
                    self.csm.air.dclassesByName['DistributedPlayerPirateUD'],
                    {'WishNameState': ('PENDING',),
                     'WishName': (self.name,)})

        if self.avId:
            self.csm.air.writeServerEvent('avatarWishname', self.avId, self.name)

        self.csm.sendUpdateToAccountId(self.target, 'setNameTypedResp', [self.avId, status])
        self.demand('Off')

class SetNamePatternFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('SetNamePatternFSM')
    POST_ACCOUNT_STATE = 'RetrieveAvatar'

    def enterStart(self, avId, pattern):
        self.avId = avId
        self.pattern = pattern

        self.demand('RetrieveAccount')

    def enterRetrieveAvatar(self):
        if self.avId and self.avId not in self.avList:
            self.demand('Kill', 'Tried to name an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        if fields['WishNameState'][0] != 'OPEN':
            self.demand('Kill', 'Avatar is not in a namable state!')
            return

        self.demand('SetName')

    def enterSetName(self):
        # Render the pattern into a string:
        parts = []
        for p, f in self.pattern:
            part = self.csm.nameGenerator.nameDictionary.get(p, ('', ''))[1]
            if f:
                part = part[:1].upper() + part[1:]
            else:
                part = part.lower()
            parts.append(part)

        parts[2] += parts.pop(3) # Merge 2&3 (the last name) as there should be no space.
        while '' in parts:
            parts.remove('')
        name = ' '.join(parts)

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.avId,
            self.csm.air.dclassesByName['DistributedPlayerPirateUD'],
            {'WishNameState': ('',),
             'WishName': ('',),
             'setName': (name,)})

        self.csm.air.writeServerEvent('avatarNamed', self.avId, name)
        self.csm.sendUpdateToAccountId(self.target, 'setNamePatternResp', [self.avId, 1])
        self.demand('Off')


class AcknowledgeNameFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('AcknowledgeNameFSM')
    POST_ACCOUNT_STATE = 'GetTargetAvatar'

    def enterStart(self, avId):
        self.avId = avId
        self.demand('RetrieveAccount')

    def enterGetTargetAvatar(self):
        # Make sure the target avatar is part of the account:
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to acknowledge name on an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        # Process the WishNameState change.
        wishNameState = fields['WishNameState'][0]
        wishName = fields['WishName'][0]
        name = fields['setName'][0]

        if wishNameState == 'APPROVED':
            wishNameState = ''
            name = wishName
            wishName = ''
            self.csm.accountDB.removeNameRequest(self.avId)
        elif wishNameState == 'REJECTED':
            wishNameState = 'OPEN'
            wishName = ''
            self.csm.accountDB.removeNameRequest(self.avId)
        else:
            self.demand('Kill', "Tried to acknowledge name on an avatar in %s state!" % wishNameState)
            return

        # Push the change back through:
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.avId,
            self.csm.air.dclassesByName['DistributedPlayerPirateUD'],
            {'WishNameState': (wishNameState,),
             'WishName': (wishName,),
             'setName': (name,)},
            {'WishNameState': fields['WishNameState'],
             'WishName': fields['WishName'],
             'setName': fields['setName']})

        self.csm.sendUpdateToAccountId(self.target, 'acknowledgeAvatarNameResp', [])
        self.demand('Off')


class LoadAvatarFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('LoadAvatarFSM')
    POST_ACCOUNT_STATE = 'GetTargetAvatar'

    def enterStart(self, avId):
        self.avId = avId
        self.demand('RetrieveAccount')

    def enterGetTargetAvatar(self):
        # Make sure the target avatar is part of the account:
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to play an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        self.avatar = fields
        self.demand('SetAvatar')

    def enterSetAvatarTask(self, channel, task):
        # Finally, grant ownership and shut down.
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.avId,
            self.csm.air.ourChannel,
            STATESERVER_OBJECT_SET_OWNER)
        datagram.addChannel(self.target<<32 | self.avId)
        self.csm.air.send(datagram)

        self.csm.air.writeServerEvent('avatarChosen', self.avId, self.target)
        self.demand('Off')
        return task.done

    def enterSetAvatar(self):
        channel = self.csm.GetAccountConnectionChannel(self.target)

        # First, give them a POSTREMOVE to unload the avatar, just in case they
        # disconnect while we're working.
        datagramCleanup = PyDatagram()
        datagramCleanup.addServerHeader(
            self.avId,
            channel,
            STATESERVER_OBJECT_DELETE_RAM)
        datagramCleanup.addUint32(self.avId)
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_ADD_POST_REMOVE)
        datagram.addString(datagramCleanup.getMessage())
        self.csm.air.send(datagram)

        # Activate the avatar on the DBSS:
        self.csm.air.sendActivate(
            self.avId, 0, 0, self.csm.air.dclassesByName['DistributedPlayerPirateUD'], {})

        # Next, add them to the avatar channel:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_OPEN_CHANNEL)
        datagram.addChannel(self.csm.GetPuppetConnectionChannel(self.avId))
        self.csm.air.send(datagram)

        # Now set their sender channel to represent their account affiliation:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_SET_CLIENT_ID)
        datagram.addChannel(self.target<<32 | self.avId)
        self.csm.air.send(datagram)

        # setup the avatar's inventory.
        self.csm.air.inventoryManager.initiateInventory(self.avId)

        # Eliminate race conditions.
        taskMgr.doMethodLater(0.2, self.enterSetAvatarTask,
                              'avatarTask-%s' % self.avId, extraArgs=[channel],
                              appendTask=True)

class UnloadAvatarFSM(OperationFSM):
    notify = directNotify.newCategory('UnloadAvatarFSM')

    def enterStart(self, avId):
        self.avId = avId

        # We don't even need to query the account, we know the avatar is being played!
        self.demand('UnloadAvatar')

    def enterUnloadAvatar(self):
        channel = self.csm.GetAccountConnectionChannel(self.target)

        # Clear off POSTREMOVE:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_CLEAR_POST_REMOVES)
        self.csm.air.send(datagram)

        # Remove avatar channel:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_CLOSE_CHANNEL)
        datagram.addChannel(self.csm.GetPuppetConnectionChannel(self.avId))
        self.csm.air.send(datagram)

        # Reset sender channel:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_SET_CLIENT_ID)
        datagram.addChannel(self.target<<32)
        self.csm.air.send(datagram)

        # Unload avatar object:
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.avId,
            channel,
            STATESERVER_OBJECT_DELETE_RAM)
        datagram.addUint32(self.avId)
        self.csm.air.send(datagram)

        # Done!
        self.csm.air.writeServerEvent('avatarUnload', self.avId)
        self.demand('Off')


# --- CLIENT SERVICES MANAGER UBERDOG ---
class ClientServicesManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('ClientServicesManagerUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        # These keep track of the connection/account IDs currently undergoing an
        # operation on the CSM. This is to prevent (hacked) clients from firing up more
        # than one operation at a time, which could potentially lead to exploitation
        # of race conditions.
        self.connection2fsm = {}
        self.account2fsm = {}

        # Instantiate our account DB interface:
        if accountDBType == 'developer':
            self.accountDB = DeveloperAccountDB(self)
        elif accountDBType == 'local':
            self.accountDB = LocalAccountDB(self)
        elif accountDBType == 'remote':
            self.accountDB = RemoteAccountDB(self)
        else:
            self.notify.error('Invalid accountdb-type: ' + accountDBType)

    def killConnection(self, connId, reason):
        datagram = PyDatagram()
        datagram.addServerHeader(
            connId,
            self.air.ourChannel,
            CLIENTAGENT_EJECT)
        datagram.addUint16(122)
        datagram.addString(reason)
        self.air.send(datagram)

    def killConnectionFSM(self, connId):
        fsm = self.connection2fsm.get(connId)

        if not fsm:
            self.notify.warning('Tried to kill connection %d for duplicate FSM, but none exists!' % connId)
            return

        self.killConnection(connId, 'An operation is already underway: ' + fsm.name)

    def killAccount(self, accountId, reason):
        self.killConnection(self.GetAccountConnectionChannel(accountId), reason)

    def killAccountFSM(self, accountId):
        fsm = self.account2fsm.get(accountId)
        if not fsm:

            self.notify.warning('Tried to kill account %d for duplicate FSM, but none exists!' % accountId)
            return

        self.killAccount(accountId, 'An operation is already underway: ' + fsm.name)

    def runAccountFSM(self, fsmtype, *args):
        sender = self.air.getAccountIdFromSender()

        if not sender:
            self.killAccount(sender, 'Client is not logged in.')

        if sender in self.account2fsm:
            self.killAccountFSM(sender)
            return

        self.account2fsm[sender] = fsmtype(self, sender)
        self.account2fsm[sender].request('Start', *args)

    def login(self, cookie):
        self.notify.debug('Received login cookie %r from %d' % (cookie, self.air.getMsgSender()))

        sender = self.air.getMsgSender()

        if sender >> 32:
            self.killConnection(sender, 'Client is already logged in.')
            return

        if sender in self.connection2fsm:
            self.killConnectionFSM(sender)
            return

        self.connection2fsm[sender] = LoginAccountFSM(self, sender)
        self.connection2fsm[sender].request('Start', cookie)

    def requestAvatars(self):
        self.notify.debug('Received avatar list request from %d' % (self.air.getMsgSender()))
        self.runAccountFSM(GetAvatarsFSM)

    def createAvatar(self, dna, index):
        self.runAccountFSM(CreateAvatarFSM, dna, index)

    def deleteAvatar(self, avId):
        self.runAccountFSM(DeleteAvatarFSM, avId)

    def setNameTyped(self, avId, name):
        self.runAccountFSM(SetNameTypedFSM, avId, name)

    def setNamePattern(self, avId, p1, f1, p2, f2, p3, f3, p4, f4):
        self.runAccountFSM(SetNamePatternFSM, avId, [(p1, f1), (p2, f2), (p3, f3), (p4, f4)])

    def acknowledgeAvatarName(self, avId):
        self.runAccountFSM(AcknowledgeNameFSM, avId)

    def chooseAvatar(self, avId):
        currentAvId = self.air.getAvatarIdFromSender()
        accountId = self.air.getAccountIdFromSender()
        if currentAvId and avId:
            self.killAccount(accountId, 'A Toon is already chosen!')
            return
        elif not currentAvId and not avId:
            # This isn't really an error, the client is probably just making sure
            # none of its Toons are active.
            return

        if avId:
            self.runAccountFSM(LoadAvatarFSM, avId)
        else:
            self.runAccountFSM(UnloadAvatarFSM, currentAvId)
