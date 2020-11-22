import sys
import re

def isHangul(text):
    '''한글검사 함수 
    from https://m.blog.naver.com/PostView.nhn?blogId=chandong83&logNo=221142971719&proxyReferer=https:%2F%2Fwww.google.com%2F
    '''
    #Check the Python Version
    pyVer3 =  sys.version_info >= (3, 0)

    if pyVer3 : # for Ver 3 or later
        encText = text
    else: # for Ver 2.x
        if type(text) is not unicode:
            encText = text.decode('utf-8')
        else:
            encText = text

    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', encText))
    return hanCount > 0