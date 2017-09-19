import requests
import json
import hmac
import base64
import hashlib
import sys
import time
from datetime import datetime
import calendar
import uuid
import gzip
import platform
from StringIO import StringIO
from panda3d.core import PandaSystem
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task import Task

class UserFunnel:
    notify = directNotify.newCategory('UserFunnel')

    def __init__(self):
        self.platform = self.__get_platform()
        self.os_version = self.__get_os_version()
        self.manufacturer = self.__getManufacturer()
        self.sdk_version = 'rest api v2'
        self.build_version = config.GetString('server-version', 'pirates-dev')
        self.engine_version = 'Panda3D %s' % PandaSystem.getVersionString()
        self.game_key = config.GetString('analytics-game-key', '')
        self.secret_key = config.GetString('analytics-secret-key', '')
        self.use_gzip = config.GetBool('analytics-gzip', True)
        self.client_ts_offset = 0
        self.session_id = None
        self.url_init = 'http://api.gameanalytics.com/v2/' + self.game_key + '/init'
        self.url_events = 'http://api.gameanalytics.com/v2/' + self.game_key + '/events'
        if config.GetBool('want-analytics-sandbox', False):
            self.notify.warning('Running in Sandbox')
            self.url_init = 'http://sandbox-api.gameanalytics.com/v2/' + self.game_key + '/init'
            self.url_events = 'http://sandbox-api.gameanalytics.com/v2/' + self.game_key + '/events'
        self.event_queue = []
        self.session_start_time = None
        self.ready = False
        if config.GetBool('want-analytics', False):
            self.__initialize()

    def __get_platform(self):
        return 'windows' #TODO

    def __get_os_version(self):
        return 'windows 10' #TODO

    def __getManufacturer(self):
        return 'microsoft' #TODO

    def __request_init(self):
        init_payload = {
            'platform': self.platform,
            'os_version': self.os_version,
            'sdk_version': self.sdk_version
        }

        init_payload_json = json.dumps(init_payload)

        headers = {
            'Authorization': self.__hmac_hash_with_secret(init_payload_json, self.secret_key),
            'Content-Type': 'application/json'
        }

        response_dict = None
        status_code = None

        try:
            init_response = requests.post(self.url_init, data=init_payload_json, headers=headers)
        except:
            self.notify.warning('Failed to initialize UserFunnel')
            return (None, 0)

        status_code = init_response.status_code

        try:
            response_dict = init_response.json()
        except:
            response_dict = None

        if not isinstance(status_code, (long, int)) and self.GetBool('want-dev', __dev__):
            print "---- Submit Init ERROR ----"
            print "URL: " + str(url_init)
            print "Payload JSON: " + str(init_payload_json)
            print "Headers: " + str(headers)          

        response_string = ('' if status_code is None else 'Returned: ' + str(status_code) + ' response code.')

        if status_code == 401:
            self.notify.warning('Failed to submit events; UNAUTHORIZED')
            self.notify.debug('Response: %s' % init_response.text)
            self.notify.debug('Verify your authorization code and game key')
            return (None, None)

        if status_code != 200:
            self.notify.warning('Failed to initialize; %s' % status_code)
            if self.GetBool('want-dev', __dev__):
                print response_string
                if isinstance(response_dict, dict):
                    print response_dict
                elif isinstance(init_response.text, basestring):
                    print 'Response contents: %s' % init_response.text
            return (None, None)

        if 'server_ts' not in response_dict or not isinstance(response_dict['server_ts'], (int, long)):
            self.notify.warning('Init failed; Did not return proper ts')
            return (None, None)

        self.ready = True
        if 'enabled' in response_dict and response_dict['enabled'] is False:
            self.ready = False

        return (response_dict, status_code)

    def __generate_new_session_id(self):
        self.session_id = str(uuid.uuid1())
        self.notify.debug('Session Id: %s' % self.session_id)

    def __update_client_ts_offset(self, server_ts):
        now_ts = datetime.utcnow()
        client_ts = calendar.timegm(now_ts.timetuple())
        offset = client_ts - server_ts

        # if too small difference then ignore
        if offset < 10:
            self.client_ts_offset = 0
        else:
            self.client_ts_offset = offset  
        self.notify.debug('Client TS offset calculated to: %s' % str(offset))      

    def __initialize(self):
        init_response, init_response_code = self.__request_init()

        if init_response is None:
            return

        self.__update_client_ts_offset(init_response['server_ts'])
        self.notify.debug('Successfully initialized')

        if self.ready is False:
            self.notify.warning('UserFunnel is disabled.')
            return

        self.__generate_new_session_id()

        self.__submitEvents()
        self.submit_task = taskMgr.doMethodLater(5, self.__submitEvents, 'submit-events')

    def __hmac_hash_with_secret(self, message, key):
        return base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest())

    def __annotate_event_with_default_values(self, event_dict):
        now_ts = datetime.utcnow()

        client_ts = calendar.timegm(now_ts.timetuple()) - self.client_ts_offset

        default_annotations = {
            'v': 2,
            'user_id': 'dev',
            'custom_01': 'dev_server',
            'client_ts': client_ts,
            'sdk_version': self.sdk_version,
            'os_version': self.os_version,
            'manufacturer': self.manufacturer,
            'device': 'Desktop',
            'platform': self.platform,
            'session_id': self.session_id,
            'build': self.build_version,
            'session_num': 1
        }
        event_dict.update(default_annotations)

    def get_session_start_event(self):
        event_dict = {
            'category': 'user'
        }
        return event_dict

    def start_session(self):
        if not self.ready:
            return
        
        self.add_to_event_queue(self.get_session_start_event())
        self.session_start_time = time.time()
        self.notify.debug('Starting session')

    def get_session_end_event(self, length=0):
        event_dict = {
            'category': 'session_end',
            'length': length
        }
        return event_dict

    def end_session(self):
        if not self.ready:
            return

        if self.session_start_time is None:
            return

        length = time.time() - self.session_start_time
        self.add_to_event_queue(self.get_session_end_event(length))
        self.notify.debug('Ending session; Length: %d' % length)

    def add_to_event_queue(self, event_dict):
        if not isinstance(event_dict, dict):
            return

        self.__annotate_event_with_default_values(event_dict)
        self.event_queue.append(event_dict)

    def __get_gzip_string(self, string_for_gzip):
        zip_text_file = StringIO()
        zipper = gzip.GzipFile(mode='wb', fileobj=zip_text_file)
        zipper.write(string_for_gzip)
        zipper.close()

        enc_text = zip_text_file.getvalue()
        return enc_text

    def submit_events(self):
        if not self.ready:
            self.notify.debug('Funnel is not ready!')
            return

        if len(self.event_queue) == 0:
            return

        try:
            event_list_json = json.dumps(self.event_queue)
        except:
            self.notify.warning('Event queue failed JSON encoding.')
            return

        self.event_queue = []

        if event_list_json is None:
            return

        if self.use_gzip:
            event_list_json = self.__get_gzip_string(event_list_json)

        headers = {
            'Authorization': self.__hmac_hash_with_secret(event_list_json, self.secret_key),
            'Content-Type': 'application/json'
        }

        if self.use_gzip:
            headers['Content-Encoding'] = 'gzip'

        try:
            events_response = requests.post(self.url_events, data=event_list_json, headers=headers)
        except Exception as e:
            self.notify.warning('Failed to submit events')
            if config.GetBool('want-dev', __dev__):
                self.notify.warning(e.reason)
            return (None, None)

        status_code = events_response.status_code
        try:
            response_dict = events_response.json()
        except:
            response_dict = None

        self.notify.debug('Submit events response: %s' % str(response_dict))

        if not isinstance(response_dict, dict):
            self.notify.warning('Submit events succeeded, but JSON decode failed.')
            self.notify.debug(events_response.text)
            return (None, None)

        if status_code == 401:
            self.notify.warning('Failed to submit events; UNAUTHORIZED')
            self.notify.debug('Response: %s' % init_response.text)
            self.notify.debug('Verify your authorization code and game key')
            return (None, None)

        if status_code != 200:
            self.notify.warning('Failed to submit events; %s' % status_code)
            if self.GetBool('want-dev', __dev__):
                print response_string
                if isinstance(response_dict, dict):
                    print response_dict
                elif isinstance(init_response.text, basestring):
                    print 'Response contents: %s' % init_response.text
            return (None, None)

        if status_code == 200:
            self.notify.debug('Events submitted')
        else:
            self.notify.warning('Failed to submit events')

        return (response_dict, status_code)

    def __submitEvents(self, task=None):
        self.submit_events()

        return Task.again

    def get_design_event(self, event_id, value):
        event_dict = {
            'category': 'design',
            'event_id': event_id,
        }
        if isinstance(value, (int, long, float)):
            event_dict['value'] = value

        return event_dict        


def logSubmit(setHostID, setMileStone):
    if __dev__ and not config.GetBool('dev-analyics', False):
        return None

    print ':Userfunnel: use of logSubmit is deprecated; Please switch to add_event.'
    #base.funnel.add_to_event_queue(base.funnel.get_design_event(setHostID, setMileStone))