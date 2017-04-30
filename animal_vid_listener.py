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
        if (datetime.datetime.now() - self.last_tweet_time) < TWEET_TIMEOUT_SECONDS:
            return True
        if hasattr(status, 'retweeted_status'):
            return True
        # There is a suprising amount of porn tweets out there, skip them
        adult_words = ['sex', 'sexy', 'porn', 'fuck', 'nude', 'playboy',
                       'screw', 'hot', 'naked', 'anal', 'cum', 'cock']
        food_words = ['cook', 'nuggets', 'eat', 'ribs', 'grill', 'dinner',
                      'broth', 'sauce']
        animal_phrases = ['early bird', 'jessica rabbit', 'copy cat']
        for word in adult_words + food_words + animal_phrases:
            if word in status.text.lower():
                return True
        return False

    def _status_video_link(self, status):
        if 'media' in status.entities:
            for item in status.entities['media']:
                if 'video' in item['expanded_url']:
                    return item['expanded_url']
        return None
