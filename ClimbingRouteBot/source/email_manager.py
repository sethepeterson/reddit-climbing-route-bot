from source.extensions import Extensions
import smtplib
import os


class EmailManager:
    GMAIL_SERVER = 'smtp.gmail.com'
    PORT = 587
    GMAIL_CREDENTIALS_PATH = os.path.dirname(__file__) + '\\..\\..\\..\\gmail_credentials.txt'
    
    COMMENT_POSTED_MESSAGE = 'Cimbing Route Bot is posted a comment.\n\nCheck: {}'
    APPROVAL_WAIT_MESSAGE = 'Cimbing Route Bot is waiting for approval.'

    def __init__(self):
        # Create Gmail instance.
        with open(self.GMAIL_CREDENTIALS_PATH, "r") as file:
            credentials = file.read().split()
            self.emailAddress = credentials[0]
            emailPassword = credentials[1]

            self.gmail = smtplib.SMTP(self.GMAIL_SERVER, self.PORT)
            self.gmail.starttls()
            self.gmail.login(self.emailAddress, emailPassword)

    def sendApprovalWaitingEmail(self):
        self.gmail.sendmail(self.emailAddress, self.emailAddress,
                            self.APPROVAL_WAIT_MESSAGE)

    def sendCommentPostedEmail(self, submission):
        submissionUrl = Extensions.getSubmissionUrl(submission)
        self.gmail.sendmail(self.emailAddress, self.emailAddress,
                            self.COMMENT_POSTED_MESSAGE.format(submissionUrl))
