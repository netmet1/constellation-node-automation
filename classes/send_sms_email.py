import smtplib
from email.message import EmailMessage
import time

class SendAMessage():

    def __init__(self,action,msg_body,config):
        self.config = config
        self.action = action
        self.setup_message()
        self.recipients = self.config.mms_email_recipients
        self.user = self.config.email
        self.password = self.config.token

        for to in self.recipients:
            self.emailObj = EmailMessage()
            self.emailObj['subject'] = self.subject
            self.emailObj['from'] = self.user
            self.emailObj.set_content(msg_body)
            self.emailObj['to'] = to
            # print(f"Sending MMS to: {to}") # console debugging, informative.
            self.enable_smtp_server()
            self.server.send_message(self.emailObj)
            self.quit_server()
            time.sleep(10) # don't upset Gmail
       

    def setup_message(self):
        # check what we need to do
        if self.action == "normal" or self.action == "error":
            self.subject = "CONSTELLATION DARKSTAR"
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