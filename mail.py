import smtplib

def prompt(prompt):
    return raw_input(prompt).strip()



def email(to):

	fromaddr = "matt.karnick@gmail.com"
	toaddrs  = to
	print "Enter message, end with ^D (Unix) or ^Z (Windows):"

	# Add the From: and To: headers at the start!
	msg = "This is the message"
	while 1:
	    try:
	        line = raw_input()
	    except EOFError:
	        break
	    if not line:
	        break
	    msg = msg + line

	print "Message length is " + repr(len(msg))

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.login('matt.karnick@gmail.com','103350855')
	server.set_debuglevel(1)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()