from source.submission_handler import SubmissionHandler
from source.extensions import Extensions
from source.ui_manager import UiManager
from source.email_manager import EmailManager
import praw
import pdb
import re
import os
import time
import sys
import traceback
from datetime import datetime, timedelta


class ClimbingRouteBot:
    REPLIED_SUBMISSIONS_PATH = os.path.dirname( __file__) + '\\..\\tools\\replied_submissions.txt'
    REDDIT_CREDENTIALS_PATH = os.path.dirname(__file__) + '\\..\\..\\..\\reddit_api_credentials.txt'

    TEST_MODE = False
    OTHER_BOTS = ['MountainProjectBot']
    SUBREDDITS = 'climbing+Bouldering+socalclimbing+ClimbingPorn+ClimbingVids'
    TESTING_SUBREDDIT = 'testingground4bots'
    TEN_MINUTES_IN_SECONDS = 600

    def __init__(self):
        # Create list of replied submission IDs.
        with open(self.REPLIED_SUBMISSIONS_PATH, 'r') as file:
            submissionIDs = file.read().split('\n')
        self.repliedSubmissions = list(filter(None, submissionIDs))
        self.checkedSubmissionsBuffer = []

        # Create Reddit instance.
        with open(self.REDDIT_CREDENTIALS_PATH, "r") as file:
            credentials = file.read().split()
            reddit = praw.Reddit(client_id=credentials[0],
                                 client_secret=credentials[1],
                                 username=credentials[2],
                                 password=credentials[3],
                                 user_agent=credentials[4])

            if self.TEST_MODE:
                self.subreddits = reddit.subreddit(self.TESTING_SUBREDDIT)
            else:  
                self.subreddits = reddit.subreddit(self.SUBREDDITS)

        # Create utility instances.
        self.submissionHandler = SubmissionHandler()
        self.emailManager = EmailManager()


    def start(self):
        # Clear screen.
        os.system('cls' if os.name == 'nt' else 'clear')

        # Execute script.
        while True:
            for submission in self.subreddits.new(limit = 20):
                try:
                    if self.isSubmissionValid(submission):
                        self.checkedSubmissionsBuffer.append(submission.id)
                        routes = self.submissionHandler.getRoutes(submission)

                        if Extensions.isNotEmpty(routes):
                            UiManager.notifyForRouteMatch(submission)

                            if len(routes) == 1:
                                self.postComment(submission, routes[0])
                                    
                            else:
                                self.emailManager.sendApprovalWaitingEmail()

                                selection = UiManager.getRouteChoice(routes)     
                                if selection != len(routes):
                                    self.postComment(submission, routes[selection])

                except:
                    traceback.print_exc()
                    UiManager.wait('Exception occured.', 30, True)

            UiManager.wait('Batch parsed...', 30, False)


    def isSubmissionValid(self, submission) -> bool:
        # Check for non-text submission.
        if submission.is_self:
            return False

        # Check for non-check submission.
        if submission.id in self.checkedSubmissionsBuffer:
            return False
        
        # Check for non-replied submission.
        if submission.id in self.repliedSubmissions:
            return False

        # Check for new submission.
        if time.time() - submission.created_utc > self.TEN_MINUTES_IN_SECONDS:
            return False

        # Check for reply from competing bots.
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            if comment.author.name in self.OTHER_BOTS:
                return False
        
        return True


    def postComment(self, submission, route):
        # Post comment.
        submission.reply(route.toComment())

        # Notify via email.
        self.emailManager.sendCommentPostedEmail(submission)

        # Update replied_submissions.txt.
        self.repliedSubmissions.append(submission.id)
        with open(self.REPLIED_SUBMISSIONS_PATH, 'w+') as file:
            for postID in self.repliedSubmissions:
                file.write(postID + '\n')
            file.close()
