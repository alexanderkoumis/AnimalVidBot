import datetime
import traceback

from tweepy.streaming import StreamListener


TWEET_TIMEOUT_SECONDS = 90 # Wait at least this long between tweets


class AnimalVidListener(StreamListener):


    def __init__(self, api, *args, **kwargs):
        super(StreamListener, self).__init__(*args, **kwargs)
        self.api = api
        self.last_tweet_time = datetime.datetime.now()

    def on_status(self, status):
        try:
            if self._filter_status(status):
                return
            video_link = self._status_video_link(status)
            if video_link is not None:
                self.api.retweet(status.id)
                self.last_tweet_time = datetime.datetime.now()
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

    def _filter_status(self, status):
        if (self._too_fast() or
                self._adult_post(status) or
                self._food_post(status) or
                self._animal_phrase(status) or
                hasattr(status, 'retweeted_status')):
            return True
        return False

    def _adult_post(self, status):
        for word in ['sex', 'sexy', 'porn', 'fuck', 'nude', 'playboy',
                     'screwed', 'hot', 'naked', 'anal']:
            if word in status.text.lower():
                return True
        return False

    def _food_post(self, status):
        for word in ['cook', 'nuggets', 'eat', 'ribs', 'grill', 'dinner', 'broth', 'sauce']:
            if word in status.text.lower():
                return True
        return False

    def _animal_phrase(self, status):
        for word in ['early bird', 'jessica rabbit', 'copy cat']:
            if word in status.text.lower():
                return True
        return False

    def _too_fast(self):
        return False        
        # time_elapsed = datetime.datetime.now() - self.last_tweet_time
        # if time_elapsed.seconds < TWEET_TIMEOUT_SECONDS:
        #     return True
        # return False

    def _status_video_link(self, status):
        if 'media' in status.entities:
            for item in status.entities['media']:
                if 'video' in item['expanded_url']:
                    return item['expanded_url']
        return None
