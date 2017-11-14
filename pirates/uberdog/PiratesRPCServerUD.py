from direct.directnotify.DirectNotifyGlobal import *
from direct.task import Task
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from threading import Thread
import traceback
import json
import sys


class PiratesRPCHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/PRPC2',)


class PiratesRPCServerUD(Thread):
    notify = directNotify.newCategory('PiratesRPCServerUD')
    notify.setInfo(True)

    def __init__(self, air):
        Thread.__init__(self)
        self.air = air
        self.hostname = config.GetString('rpc-hostname', '127.0.0.1')
        self.port = config.GetInt('rpc-port', 6484)
        self.running = True
        self.server = SimpleXMLRPCServer((self.hostname, self.port), logRequests=False, requestHandler=PiratesRPCHandler)
        self.server.register_introspection_functions()
        self.registerCommands()

    def register_function(self, function, name=None):
        self.server.register_function(function, name)

    def run(self):
        self.notify.info('Starting RPC server at %s:%d' % (self.hostname, self.port))
        self.server.serve_forever()

    def stop_Server(self):
        self.server.shutdown()
        self.server.server_close()

    def registerCommands(self):
        self.register_function(self.ping)
        self.register_function(self.systemMessage)
        self.register_function(self.systemMessageChannel)
        self.register_function(self.kickChannel)

    def formatCallback(self, code=200, message='Success', **kwargs):
        response = {'code': code, 'message': message}
        for keyword in kwargs:
            response[keyword] = kwargs[keyword]
        return json.dumps(response)

    def ping(self, response):
        """
        Summary:
            Responds with the [data] that was sent. This method exists only for
            testing purposes.

        Parameters:
            [any data] = The data to be given back in response.

        Example response: 'pong'
        """
        return self.formatCallback(response=response)

    def systemMessage(self, message):
        """
        Summary:
            Broadcasts a [message] to the entire server globally.

        Parameters:
        [str message] = The message to broadcast.
        """
        self.air.systemMessage(message)

        return self.formatCallback()

    def systemMessageChannel(self, message, channel):
        """
        Summary:
            Broadcasts a [message] to any client whose Client Agent is
            subscribed to the provided [channel].

        Parameters:
            [int channel] = The channel to direct the message to.
            [str message] = The message to broadcast.
        """
        self.air.systemMessage(message, channel)

        return self.formatCallback()

    def kickChannel(self, channel, reason=1, message=''):
        """
        Summary:
            Kicks any users whose CAs are subscribed to a particular [channel] with a [code].

        Parameters:
            [int channel] = The channel to direct the message to.
            [int code] = An optional code to kick.
            [string reason] = An optional reason.
        """

        try:
            self.air.kickChannel(channel, reason, message)
        except Exception as e:
            return self.formatCallback(code=100, message='Failed to kick channel, An unexpected error occured', error=repr(e))

        return self.formatCallback()
