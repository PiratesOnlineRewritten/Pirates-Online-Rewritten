import json
import requests

__all__ = [
    'WebhookException', 'WebhookBase', 'GenericWebhook', 'GithubWebhook', 'SlackWebhook',
    'SlackAttachmentException', 'SlackAttachment', 'SlackField']

class WebhookException(Exception):
    """
    Generic Discord Webhook Exception
    """

class WebhookBase(object):

    """
    Base class for all Discord webhooks
    """

    def __init__(self, url, extension=None):
        self.url = url
        self.extension = extension

    def getExtension(self):
        return self.extension

    def formatMessage(self):
        """
        Called prior to posting to the url. Returns a formatted message
        """
        return NotImplemented

    def send(self):
        """
        Sends the formatted message to the specified `self.url`
        """

        formatted = self.formatMessage()
        if not formatted:
            raise WebhookException('Unable to send webhook post; formatMessage returned None')

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        url = self.url
        if self.extension:
            url += self.extension

        result = requests.post(url, headers=headers, data=formatted).text
        if result != '' and result != 'ok':
            raise WebhookException('Unexpected error occured while sending post; %s' % str(result))

        return True

class GenericWebhook(WebhookBase):

    """
    Represents a generic basic message Discord webhook
    """

    def __init__(self, url, message, author=None, avatar=None):
        WebhookBase.__init__(self, url)
        self.message = message
        self.author = author
        self.avatar = avatar

    def formatMessage(self):
        """
        Called prior to posting to the url. Returns a formatted message
        """

        data = {}
        data['content']= self.message

        if self.author:
            data['username'] = self.author

        if self.avatar:
            data['avatar_url'] = self.avatar

        return json.dumps(data)

class GithubWebhook(WebhookBase):

    """
    Represents a Github Discord webhook
    """

    def init(self, url):
        WebhookBase.__init__(self, url, '/github')

    def formatMessage(self):
        """
        Called prior to posting to the url. Returns a formatted message
        """

        return NotImplemented   

class SlackWebhook(WebhookBase):

    """
    Represents a Slack Discord webhook
    """

    def __init__(self, url, message='', author='', avatar=None):
        WebhookBase.__init__(self, url, '/slack')
        self.message = message
        self.author = author
        self.avatar = avatar
        self.attachments = []

    def getAttachments(self):
        return self.attachments

    def addAttachment(self, attachment):
        """
        Adds the specified SlackAttachment to self.attachments for later usage.
        """

        if isinstance(attachment, SlackAttachment):
            self.attachments.append(attachment)
        else:
            raise WebhookException('Unable to add attachment. %s is not an instance of %s' % (attachment.__class__.__name__, SlackAttachment.__name__))

    def formatMessage(self):
        """
        Called prior to posting to the url. Returns a formatted message
        """

        data = {}
        data['text'] = self.message
        data['username'] = self.author
        if self.avatar:
            data['icon_url'] = self.avatar

        data['attachments'] = [] 
        for attachment in self.attachments:
            att = {}
            att['author_name'] = attachment.author_name
            att['author_icon'] = attachment.author_icon
            att['color'] = attachment.color
            att['pretext'] = attachment.pretext
            att['title'] = attachment.title
            att['title_link'] = attachment.title_link
            att['image_url'] = attachment.image_url
            att['thumb_url'] = "http://example.com/path/to/thumb.png"
            att['footer'] = attachment.footer
            att['footer_icon'] = attachment.footer_icon
            att['ts'] = attachment.ts
            att['fields'] = []

            for field in attachment.fields:
                f = {}
                f['title'] = field.title
                f['value'] = field.value
                f['short'] = field.short

                att['fields'].append(f)

            data['attachments'].append(att)

        formatted = json.dumps(data)

        return formatted

class SlackAttachmentException(Exception):
    """
    Exception specified to the SlackAttachment object
    """

class SlackAttachment(object):

    """
    Represents a attachment for the SlackWebhook object
    """
    
    def __init__(self, author_name='', author_icon='', color='', pretext='', title='', title_link='', image_url='', footer='', footer_icon='', ts=0, fields=[]):
        self.author_name = author_name
        self.author_icon = author_icon
        self.color = color
        self.pretext = pretext
        self.title = title
        self.title_link = title_link
        self.image_url = image_url
        self.footer = footer
        self.footer_icon = footer_icon
        self.ts = ts
        self.fields = fields

    def addField(self, field):
        """
        Adds the specified field t o the current SlackAttachment object.
        """

        if isinstance(field, SlackField):
            self.fields.append(field)
        else:
            raise SlackAttachmentException('Unable to add field; %s is not an instance of %s' % (field.__class__.__name__, SlackField.__name__))

class SlackField(object):
    
    """
    Represents a SlackAttachment field
    """

    def __init__(self, title='', value='', short=False):
        self.title = title
        self.value = value
        self.short = short