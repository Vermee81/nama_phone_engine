#-*- coding:utf8 -*-
import os
import re
import yaml
import socket
import cookielib
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

yml = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.yaml')
CONFIG = yaml.load(open(yml))

br = Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.open('https://secure.nicovideo.jp/secure/login_form')

br.select_form(nr=0)
br['mail_tel'] = CONFIG['mail']
br['password'] = CONFIG['password']
br.submit()

# http://live.nicovideo.jp/watch/lv190173383?ref=top&zroute=index
lv = 'lv193566061' # set lv id e.g. lv00000000
br.open('http://watch.live.nicovideo.jp/api/getplayerstatus?v=%s' % lv) 
soup = BeautifulSoup(br.response().read())

thread = int(soup.find('thread').renderContents())
addr = soup.find('addr').renderContents()
port = int(soup.find('port').renderContents())

#<addr>omsg103.live.nicovideo.jp</addr>
# <port>2812</port>
# <thread>1373766965</thread>

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((addr, port))
sock.send('<thread thread="%d" version="20061206" res_from="-1"/>¥0' % thread)

print str(sock)

try:
    data = sock.recv(2048)
except socket.error, e:
    if e.errno != errno.EINTR:
        print e
        print e.errno
        raise
    else:
        print data

while True:
    data = sock.recv(2048)[:-1]
    d = BeautifulSoup(data)
    chat = d.find('chat')
    num = dict(chat.attrs)['no']
    comment = chat.renderContents()
    if not 'mail' in dict(chat.attrs): print num,comment
    else:
        if re.compile('nottalk|hidden').search(dict(chat.attrs)['mail']): continue
        else: print num, comment
    if comment == u"/disconnect": break
