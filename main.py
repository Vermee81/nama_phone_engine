# -*- coding: utf-8 -*-
import time
import sys,os
dirpath=os.path.dirname(os.path.abspath(__file__))
gpio_dir='/libs/gpio'
tweet_dir='/libs/tweets'
fuel_dir='/libs/fuel'
sys.path.append(dirpath+gpio_dir)
sys.path.append(dirpath+fuel_dir)
sys.path.append(dirpath+tweet_dir)
from libs.gpio import gpio
from libs.tweets import twitter_crawler
from libs.fuel import fuel

def change_gpio_state(my_gpio, power_time):
    if power_time > 0 :
        my_gpio.on()
    elif power_time == 0 :
        my_gpio.off()

def main():
    # Raspberry Piをコントロールするオブジェクトを生成
    my_gpio = gpio.Gpio()
    fuel_tank = fuel.Fuel()

    # Remaining time that the fan is kept working.
    power_time = 0

    # 一定間隔でツイッターのツイート数を監視する
    # ツイッターを監視するスレッドを生成
    tweet_crawl = twitter_crawler.TwitterThread()
    tweet_crawl.start()

    fuel_tank = tweet_crawl.fuel_tank

    while 1:
        change_gpio_state(my_gpio, power_time)

        # 燃料供給
        power_time += fuel_tank.fuel
        fuel_tank.fuel = 0
        print "燃料供給後", power_time

        # 毎秒燃料は減っていく
        if power_time > 0:
            power_time -= 1
            print "燃料減った後", power_time

        time.sleep(1)


if __name__ == "__main__":
    main()



