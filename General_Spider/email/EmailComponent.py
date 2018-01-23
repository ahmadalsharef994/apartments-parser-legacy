from quickstart import *
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors

class EmailComponent:

    #@staticmethod
    #def sendEmail(messageBody, subject):
        #from time import gmtime, strftime
        #timeForSubject = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        #subject = subject + " "+timeForSubject
        #import smtplib
        #fromaddr = "scrapy.vmp.project@gmail.com"
        #toaddrs  = 'bashar@voicempower.com'
        #cc = "wkinaan@voicempower.com"
        #message = (
        #"From: %s\r\n" % fromaddr
        #+ "To: %s\r\n" % toaddrs
        #+ "CC: %s\r\n" % cc
        #+ "Subject: %s\r\n" % subject
        #+ "\r\n" 
        #+ messageBody
        #)
        #username = 'scrapy.vmp.project@gmail.com'
        #password = 'vmp@ScT12*23&*'
        #server = smtplib.SMTP('smtp.gmail.com:587')
        #server.ehlo()
        #server.starttls()
        #server.login(username,password)
        #server.sendmail(fromaddr, toaddrs, message)
        #server.quit()

    @staticmethod
    def sendEmail(messageBody, subject):
        message = MIMEText(messageBody)
        message['to'] = 'wkinaan@voicempower.com,bashar@voicempower.com'
        message['from'] = 'scrapy.vmp.project@gmail.com'
        message['subject'] = subject
        messageRow = {'raw': base64.urlsafe_b64encode(message.as_string())}
        #EmailComponent.send_message("me", messageRow)

    @staticmethod
    def send_message(user_id, message):
        try:
            credentials = get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('gmail', 'v1', http=http)

            message = (service.users().messages().send(userId=user_id, body=message).execute())
            print 'Message Id: %s' % message['id']
            #return message
        except errors.HttpError, error:
            print 'An error occurred: %s' % error


#EmailComponent.sendEmail("No Totti no party, we invite you to watch a game", "Francesco Totti")