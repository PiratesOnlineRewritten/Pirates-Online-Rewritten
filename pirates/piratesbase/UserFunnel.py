import requests
import json
from panda3d.core import PandaSystem
from direct.directnotify.DirectNotifyGlobal import directNotify

class UserFunnel:
    notify = directNotify.newCategory('UserFunnel')

    def __init__(self):
        self.project_title = config.GetString('parse-project-title', '')
        self.restful_key = config.GetString('parse-restful-key', '')
        self.parse_url = config.GetString('parse-server-url', 'http://127.0.0.1:1337')
        self.parse_path = config.GetString('parse-url-path', 'por-parse')
        self.build_version = config.GetString('server-version', 'pirates-dev')
        self.engine_version = 'Panda3D %s' % PandaSystem.getVersionString()

    def report_client_opened(self):
        # Tell Parse the game was opened
        return self.submit_event('AppOpened')

    def __build_headers(self):
        return {
            "Content-Type": "application/json",
            "X-Parse-Application-Id": self.project_title,
            "X-Parse-REST-API-Key": self.restful_key,
        }

    def __get_event_url(self, event_name):
        return '%s/%s/events/%s' % (
            self.parse_url, 
            self.parse_path,
            event_name)

    def submit_event(self, event, **kwargs):
        self.notify.debug('Logging %s event with server' % event)
        payload = {
            'version': self.build_version,
            'engine_version': self.engine_version,
        }
        payload.update(kwargs)
        request = requests.post(
            self.__get_event_url('AppOpened'), 
            data=payload, 
            headers=self.__build_headers())
        return request.json()

def logSubmit(id, event_name):
    print(':UserFunnel(warning): Deprecated logSubmit called. An upgrade is recommended')
    base.funnel.submit_event(event_name)