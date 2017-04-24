#!/usr/bin/env python3

import argparse
import json

import tweepy

from animal_vid_listener import AnimalVidListener


def get_args():
    """Parse user args, get config file path"""
    parser = argparse.ArgumentParser(description='SendBeatsBot app')
    parser.add_argument('config_filename', help='Path to JSON config file.')
    return parser.parse_args()

def load_config(config_filename):
    """Read the config file and parse the JSON"""
    with open(config_filename, 'r') as config_file:
        return json.load(config_file)

def run(config):
    """Run the main logic"""
    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])

    api = tweepy.API(auth)

    listener = AnimalVidListener(api)

    stream = tweepy.Stream(auth, listener)
    stream.filter(track=['animal,dog,cat,lion,cheetah,zoo,bird,leopard,boar,deer,giraffe,chicken,'
                         'dachshund,buffalo,donkey,horse,monkey,bear,pug,pig,rabbit,sheep,llama,'
                         'elephant,hyena,alligator,turtle'])

def main():
    """Main app outer loop"""
    args = get_args()
    config = load_config(args.config_filename)
    # Keep the app running when it periodically hangs
    while True:
        try:
            run(config)
        except Exception as exc:
            # Trying to figure out what kind of exception this throws
            print('Exception type in main(): {}, exception: {}'.format(type(exc), str(exc)))

if __name__ == '__main__':
    main()