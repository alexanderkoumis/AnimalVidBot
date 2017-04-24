import traceback

from tweepy.streaming import StreamListener


class AnimalVidListener(StreamListener):


    def __init__(self, api, *args, **kwargs):
        super(StreamListener, self).__init__(*args, **kwargs)
        self.api = api

    def on_status(self, status):
        try:
            if hasattr(status, 'retweeted_status'):
                return
            if self._adult_post(status):
                return
            video_link = self._status_video_link(status)
            if video_link is not None:
                self.api.retweet(status.id)
        except Exception as exc:
            # Trying to figure out what kind of exception this throws
            print('Exception[{}] in on_status: {}, text: {}'.format(
                type(exc), str(exc), status.text))
            traceback.print_stack()

    def on_error(self, status_code):
        print('Error: {}'.format(status_code))
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

    def _adult_post(self, status):
        for word in ['sex', 'sexy', 'porn', 'fuck', 'nude', 'playboy',
                     'screwed', 'hot', 'naked', 'anal']:
            if word in status.text:
                return True
        return False

    def _status_video_link(self, status):
        if 'media' in status.entities:
            for item in status.entities['media']:
                if 'video' in item['expanded_url']:
                    return item['expanded_url']
        return None
