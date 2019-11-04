from source.submission_handler import SubmissionHandler
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
    CREDENTIALS_PATH = os.path.dirname(__file__) + "\\..\\..\\reddit_api_credentials.txt"
    TEST_MODE = False
    SUBREDDITS = 'climbing+Bouldering+socalclimbing+ClimbingPorn+ClimbingVids'
    TESTING_SUBREDDIT = 'testingground4bots'

    def __init__(self):
        # Create list of replied submission IDs.
        with open(self.REPLIED_SUBMISSIONS_PATH, 'r') as file:
            self.repliedSubmissions = file.read()
            self.repliedSubmissions = self.repliedSubmissions.split('\n')
            self.repliedSubmissions = list(
                filter(None, self.repliedSubmissions))
            file.close()

            self.checkedSubmissionsBuffer = []

        # Create Reddit instance.
        with open(self.CREDENTIALS_PATH, "r") as file:
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
            file.close()

        # Create SubmissionHandler instance.
        self.submissionHandler = SubmissionHandler()


    def start(self):
        # Clear screen.
        os.system('cls' if os.name == 'nt' else 'clear')

        # Execute script.
        while True:
            for submission in self.subreddits.new(limit = 100):
                try:
                    if not submission.is_self and submission.id not in self.repliedSubmissions and submission.id not in self.checkedSubmissionsBuffer:
                        if time.time() - submission.created_utc < 7200:
                            self.checkedSubmissionsBuffer.append(submission.id)
                            route = self.submissionHandler.getRoute(submission)

                            if route is not None:
                                submission.reply(route.toComment())
                                self.updateRepliedSubmissions(submission)
                                self.wait('Comment posted.', 60)

                except:
                    traceback.print_exc()
                    self.wait('Exception occured.', 30)
            self.wait('Batch parsed...', 180)

    def updateRepliedSubmissions(self, submission):
        self.repliedSubmissions.append(submission.id)
        with open(self.REPLIED_SUBMISSIONS_PATH, 'w+') as file:
            for postID in self.repliedSubmissions:
                file.write(postID + '\n')
            file.close()

    def wait(self, message, timeToWait):
        print()
        while timeToWait is not 0:
            minutes = timeToWait % 60
            seconds = timeToWait - (minutes * 60)
            if seconds < 10:
                seconds = '0{}'.format(seconds)

            sys.stdout.write('\r' + message + ' Continuing in: {}:{}'.format(minutes, seconds))
            sys.stdout.flush()
            time.sleep(1)
            timeToWait = timeToWait - 1
