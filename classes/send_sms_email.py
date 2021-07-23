import smtplib
from email.message import EmailMessage, MIMEPart
import time

class SendAMessage():

    def __init__(self,action,msg_body,config,attach=None):
        self.config = config
        self.action = action
        self.setup_message()
        self.recipients = self.config.mms_email_recipients
        self.user = self.config.email
        self.password = self.config.token

        if self.config.csv:
            self.recipients = [self.config.csv]
        for to in self.recipients:
            self.emailObj = EmailMessage()
            self.emailObj['subject'] = self.subject
            self.emailObj['from'] = self.user
            self.emailObj.set_content(msg_body)
            self.emailObj['to'] = to

            if self.config.csv:
                with open(attach, 'rb') as content_file:
                    content = content_file.read()
                    self.emailObj.add_attachment(content, maintype='application', subtype='pdf', filename=attach)

            # print(f"Sending MMS to: {to}") # console debugging, informative.
            self.enable_smtp_server()
            self.server.send_message(self.emailObj)
            self.quit_server()
            time.sleep(10) # don't upset Gmail
       

    def setup_message(self):
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