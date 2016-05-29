# -*- encoding=utf-8 -*-
#import sys,os
#dirpath=os.path.dirname(os.path.abspath(__file__))
#fuel_dir='../fuel'
#sys.path.append(dirpath+'/'+fuel_dir)
import threading
import time
import oauth2 as oauth
import pprint
import json, urllib2
import ConfigParser
from libs.fuel import fuel
###import ignore_twitter_keys.py



def get_tweets(fuel_tank = "", since_id = "", account_name = ""):

    ACCOUNT = u"@namaphonebox"
    COUNT = 100 ## max100件

    query = ACCOUNT.encode('utf-8')

    url = 'https://api.twitter.com/1.1/search/tweets.json'
    params = {'q': query, 'since_id': since_id, 'count': COUNT}

    conf = ConfigParser.SafeConfigParser()
    conf.read('/home/pi/nama_phone_engine/libs/tweets/ignored_twitter_keys.cfg')

    ## ここから配列
    CK = conf.get(account_name, 'cons_key')
    CS =  conf.get(account_name, 'cons_sec')
    AT = conf.get(account_name, 'acc_token')
    AS = conf.get(account_name, 'acc_sec')

    consumer = oauth.Consumer(key=CK, secret=CS)
    token = oauth.Token(key=AT, secret=AS)

    request = oauth.Request.from_consumer_and_token(consumer, token, http_url=url,parameters=params)
    request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, token)
    res = urllib2.urlopen(request.to_url())

    for r in res:
        data = json.loads(r)

    status_list = data['statuses']
    max_id = data['search_metadata']['max_id_str']

    if fuel_tank != "" :
        fuel_tank.add_fuel(len(status_list))

    print len(status_list)
    #pprint.pprint(data)

    return max_id


class TwitterThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.fuel_tank = fuel.Fuel()
        self.INTERVAL = 30
        self.TWITTER_ACCOUNTS = ['twitterkeys', 'twitterkeys2']

    def run(self):
        max_id = ""
        account_index = 0
        max_id = get_tweets(account_name=self.TWITTER_ACCOUNTS[account_index])
        counter = 1
        time.sleep(self.INTERVAL)
        while 1:
            #次のアカウントへ切り替える
            account_index = counter % len(self.TWITTER_ACCOUNTS)

            max_id = get_tweets(self.fuel_tank, max_id, self.TWITTER_ACCOUNTS[account_index])
            print "FUEL: " + str(self.fuel_tank.fuel)

            counter = counter + 1

            time.sleep(self.INTERVAL)

if __name__ == '__main__':
    tweet_crawl = TwitterThread()
    tweet_crawl.start()

