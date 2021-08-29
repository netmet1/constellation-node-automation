import smtplib
from email.message import EmailMessage, MIMEPart
import time
from typing import Tuple

class SendAMessage():

    def __init__(self,action,msg_body,config,attach=None):
        self.config = config
        self.msg_body = msg_body
        self.attach = attach
        self.action = action
        self.setup_message_subject()
        self.recipients = self.config.mms_recipients
        self.user = self.config.email
        self.password = self.config.token

        if self.config.csv:
            self.recipients = [self.config.csv]
            with open(self.attach, 'rb') as content_file:
                self.content = content_file.read()
            self.build_and_send_msg()
        else:
            if self.config.mms_enabled:
                self.recipients = self.config.mms_recipients
                if not self.config.mms_subject:
                    self.build_subject = False
                self.build_and_send_msg()
            if self.config.email_enabled:
                self.build_subject = True
                if self.config.mms_enabled:
                    time.sleep(5)
                self.recipients = self.config.email_recipients
                self.build_and_send_msg()

       
    def build_and_send_msg(self):
        self.emailObj = EmailMessage()

        if self.config.csv:
            self.emailObj.add_attachment(self.content, maintype='application', subtype='pdf', filename=self.attach)

        if self.build_subject:
            self.emailObj['subject'] = self.subject

        self.emailObj['from'] = self.user
        self.emailObj.set_content(self.msg_body)
        self.emailObj['to'] = self.user
        self.emailObj['bcc'] = self.recipients

        # print(f"Sending MMS to: {to}") # console debugging, informative.
        self.enable_smtp_server()
        self.server.send_message(self.emailObj)
        self.quit_server()


    def setup_message_subject(self):
        # check what we need to do
        if self.action == "normal" or self.action == "auto" or self.action == "error":
            self.subject = f"CONSTELLATION {self.config.node_name}"
        elif self.action == "health":
            self.subject = f"HEALTH CHECK {self.config.node_name}"
        # come back to re-enable this later...
        # if self.action == "error":
        #     self.subject = "ERROR CONST DARSTAR"
            

    def enable_smtp_server(self):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login(self.user, self.password)
    

    def quit_server(self):
        self.server.quit()


if __name__ == "__main__":
    print("This class module is not designed to be run independently, please refer to the documentation")