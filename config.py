#!/usr/bin/env python

class Config(object):
    #General
    DATABASE = 'database.db'
    PRIMARY_POST = "furaffinity"
    # This should be regenerated with os.urandom(24)
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    #Twitter
    TWITTER_CONSUMER_KEY = "zYCVAqsDnJyKhfdw9K73fx9My"
    TWITTER_CONSUMER_SECRET = "AxmFKz6Rh6m87hUukkEgBlboOMkTMTziDIVJCTHmpBouJqvKcd"

    #Facebook
    #~ FACEBOOK_CONSUMER_KEY
    #~ FACEBOOK_CONSUMER_SECRET

    #Weasyl
    #~ WEASYL_API_KEY

    #Meetup
    #~ MEETUP_API_KEY

    #Furaffinity
    COOKIE_FILE = "cookies.txt"

class DevelopmentConfig(Config):
    DEBUG = True

