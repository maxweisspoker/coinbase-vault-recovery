#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
try:  from __builtin__ import bytes, str, open, super, range, zip, round, int, pow, object, input
except ImportError:  pass
try:  from __builtin__ import raw_input as input
except:  pass
from getpass import getpass
from simplebitcoinfuncs import *
from simplebitcoinfuncs.hexhashes import *
from pybip38 import bip38decrypt


print()

while True:
    userseed = input("Please enter your user seed (begins with K or L) or your master xprv key:\n")
    userseed = normalize_input(userseed).replace('\r','').replace('\n','').replace(' ','')
    try:
        if userseed[0] == 'K' or userseed[0] == 'L':
            userseed = privtohex(userseed)
            assert len(userseed) == 64
        elif userseed[:4] != 'xprv':
            raise Exception(' ')
        userkey = BIP32(userseed)
    except:
        print("\nInvalid user seed entered.\n")
    else:
        break

print("\nExcellent! Your user public key appears to be:\n" + userkey.xpub)

while True:
    sharedseed = input("\nPlease enter the shared seed (begins with 6P):\n")
    sharedseed = normalize_input(sharedseed).replace('\r','').replace('\n','').replace(' ','')
    try:
        sharedseed = b58d(sharedseed)
        assert len(sharedseed) == 78
        assert sharedseed[:4] == '0142' or sharedseed[:4] == '0143'
    except:
        print("\nInvalid shared seed entered.")
    else:
        sharedseed = b58e(sharedseed)
        break

while True:
    sharedseedxpub = input("\nPlease enter the shared public key:\n")
    sharedseedxpub = normalize_input(sharedseedxpub).replace('\r','').replace('\n','').replace(' ','')
    try:
        assert sharedseedxpub[:4] == 'xpub'
        sharedseedxpub = BIP32(sharedseedxpub).xpub
        assert sharedseedxpub[:4] == 'xpub'
    except:
        print("\nInvalid shared public key entered. It should begin with 'xpub'.")
    else:
        break

while True:
    coinbasexpub = input("\nPlease enter the Coinbase public key:\n")
    coinbasexpub = normalize_input(coinbasexpub).replace('\r','').replace('\n','').replace(' ','')
    try:
        assert coinbasexpub[:4] == 'xpub'
        coinbasexpub = BIP32(coinbasexpub)
        assert coinbasexpub.xpub[:4] == 'xpub'
    except:
        print("\nInvalid Coinbase public key entered. It should begin with 'xpub'.")
    else:
        break

print("\nAlmost finished!")

while True:
    compresscoinbase = input('\nWas your vault created before June 2015? (y/n):  ')
    compresscoinbase = normalize_input(compresscoinbase).replace('\r','').replace('\n','').replace(' ','')
    try:
        if 'y' in compresscoinbase.lower():
            assert 'n' not in compresscoinbase.lower()
            compresscoinbase = False
        elif 'n' in compresscoinbase.lower():
            compresscoinbase = True
        assert compresscoinbase is True or compresscoinbase is False
    except:
        print('\nPlease enter only yes or no.')
    else:
        break

while True:
    password = getpass("\nPlease enter your vault password:  ")
    try:
        password = normalize_input(password,False,True)
        sharedkey = bip38decrypt(password,sharedseed,False)
        assert sharedkey is not False
        sharedkey = privtohex(sharedkey)
        sharedkey = BIP32(sharedkey)
        assert sharedkey.xpub == sharedseedxpub
    except:
        print("\nThe password entered does not decrypt the key properly. Perhaps you mis-typed? Please try again.")
    else:
        break

while True:
    index = input("\nPlease enter the index number for the vault address (0 for first address):  ")
    try:
        index = int(index)
    except:
        print("\nYou must enter only a number.")
    else:
        break

print("\nFantastic! Here is the prerequisite information for making a multisig transaction yourself:\n")

path = "m/" + str(index)
key1 = uncompress(userkey[path].pub)
key2 = uncompress(sharedkey[path].pub)
key3 = coinbasexpub[path].pub
if compresscoinbase is False:
    key3 = uncompress(key3)

keylist = [int(key1,16),int(key2,16),int(key3,16)]
keylist.sort()

redeemscript = "52"

for i in range(len(keylist)):
    key = dechex(keylist[i])
    redeemscript = redeemscript + dechex(len(key)//2) + key

redeemscript = redeemscript + "53ae"

address = b58e("05" + hash160(redeemscript))

print("Address:")
print(address + "\n")

print("Redeem script:")
print(redeemscript + "\n")

print("First multisig signing key:")
print(b58e("80" + privtohex(userkey[path].wif)) + "\n")

print("Second multisig signing key:")
print(b58e("80" + privtohex(sharedkey[path].wif)) + "\n")

print('You can use a site like Coinb.in to make and sign a new multisig transaction.\nhttps://coinb.in/#newTransaction')

print()
exit()

