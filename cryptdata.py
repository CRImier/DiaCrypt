#!/usr/bin/env python
# encoding: utf-8
"""
This module is responsible for diary file storage and encryption-decryption.
It uses Blowfish encryption with password and salt for key generation
so that unique key is generated each time. 
"""

__all__ = []
__version__ = 0.1
__date__ = '2013-04-09'
__updated__ = '2013-04-09'
DEBUG = False

import blowfish
import random
import md5
import os

if __name__ == "__main__":
    print "Not to be used as independent module."

def first_launch():
    """ Simply checks if there is diary file. If not, returns True. """
    if os.path.exists('diary.db'):
        return False
    else:
        return True

sallen = 16
crypttimes = 500

def creatediary(data, password, level):
    encryptdiary(data, password, level)
    return decryptdiary(password)

def decryptdiary(password):
    f=open('diary.db','rb')
    string = f.read()
    f.close()
    salt = string[len(string)-sallen:]
    string = string[:len(string)-sallen]
    stringc = string
    key = createkey(password+salt)
    cipher = blowfish.Blowfish (key)
    cipher.initCTR()
    data = cipher.decryptCTR(string)
    if DEBUG:
        print "Decrypting:"
        print "Salt:"+salt
        print "Password:"+password
        print "Key:"+key
        print len(string)+sallen
        print len(string)
        print "Encrypted string:"
        print string
        print "Decrypted string:"
        print data
    level = data[:2]
    if level not in ['$1','$2','$3']:
        return False #Decryption error
    level = int(level[1:])
    data = data[2:]
    try:
        data = eval(data)
    except: 
        return False #Decryption problem
    if level in [2, 3]:
        fh = open('diary.hash', 'r')
        hashf = fh.read()
        fh.close()
        if hashf != md5calc(stringc)+md5calc(repr(data)):
            return [data, level, 'ERROR!']
        else:
            return [data, level]
    else:
        return [data, level]
    
def createkey(base):    
    for x in range(crypttimes):
        base = md5calc(base)
    return base[:18]

def encryptdiary(data, password, level):
    salt = createsalt()
    key = createkey(password+salt)
    cipher = blowfish.Blowfish (key)
    cipher.initCTR()
    diary = ''
    if level == 1:
        diary += ('$1')
    elif level == 2:
        diary += ('$2')        
    elif level == 3:
        diary += ('$3')
    diary += (repr(data))
    crypted = cipher.encryptCTR(diary)
    if DEBUG:
        print "Encrypting:"
        print "Salt:"+salt
        print "Password:"+password
        print "Key:"+key
        print len(diary)+sallen
        print len(diary)
        print "Decrypted string:"
        print diary
        print "Encrypted string:"
        print crypted
    f=open('diary.db','wb')
    f.write(crypted+salt)
    if level == 2 or level == 3:
        fh=open('diary.hash','wb')
        fh.write(md5calc(crypted)+md5calc(repr(data)))
        fh.close()
    f.close()
    return True    
        
def createsalt():
    length = sallen
    chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-='
    salt = ''.join(random.choice(chars) for x in range(length))
    return salt

def md5calc(data):
    return md5.new(str(data)).digest()

def encryptentry(entry, password):
    salt = createsalt()
    key = createkey(password+salt)
    cipher = blowfish.Blowfish (key)
    cipher.initCTR()
    entry[1] = 'entryok'+entry[1]
    entry[1] = cipher.encryptCTR(entry[1])
    return entry+[salt]

def decryptentry(entry, password):
    if len(entry) <= 2:
        return 'notenc'
    salt = entry[len(entry)-1]
    key = createkey(password+salt)
    cipher = blowfish.Blowfish (key)
    cipher.initCTR()
    entry[1] = cipher.decryptCTR(entry[1])
    if entry[1][:7] != 'entryok':
        return False #Decryption error
    entry[1] = entry[1][7:]
    return entry[:len(entry)-1]

    
def deletediary():
    try:
        os.remove('diary.db')
        os.remove('diary.hash')
    except:
        pass
    
def exportdata(data, filename):
    try:
        f = open(filename, 'w')
        f.write(repr(data))
        f.close()
        return True
    except:
        return False
    
def importdata(filename):
    try:
        f = open(filename, 'r')
        data = f.read()
        f.close()
        return eval(data)
    except:
        return False