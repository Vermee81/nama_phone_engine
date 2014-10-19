# -*- coding: utf-8 -*-
import time
from libs.gpio import gpio
from libs.tweets import twitter_crawler
from libs.fuel import fuel

status = "OFF"

def change_gpio_state(my_gpio, power_time):
    if power_time > 0 and my_gpio.state == 'OFF':
        my_gpio.on()
    if power_time == 0 and my_gpio.state == 'ON':
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
        power_time += fuel_tank.give_fuel()
        print "燃料供給後", power_time

        # 毎秒燃料は減っていく
        power_time -= 1
        print "燃料減った後", power_time

        time.sleep(1)


if __name__ == "__main__":
    main()



