import praw
import os
import sys
import re

class DataEntry:

    def __init__(self, submissionTitle: str, routeName: str, commentFullName: str):
        self.submissionTitle = submissionTitle
        self.routeName = routeName
        self.commentFullName = commentFullName

    def toString(self) -> str:
        return '{}|{}|{}'.format(self.submissionTitle, self.routeName, self.commentFullName)

class DataMiner:

    def __init__(self):
        # Update user.
        print('\n\nInitializing...')

        # Define path constants.
        directoryPath = os.path.dirname(__file__)
        REDDIT_CREDENTIALS_PATH = directoryPath + '\\..\\..\\reddit_api_credentials.txt'
        self.DATA_FILE_PATH = directoryPath + '\\data.txt'

        # Create Reddit instance.
        with open(REDDIT_CREDENTIALS_PATH, "r") as file:
            credentials = file.read().split()
        self.reddit = praw.Reddit(client_id=credentials[0],
                             client_secret=credentials[1],
                             username=credentials[2],
                             password=credentials[3],
                             user_agent=credentials[4])

        # Open current data file and create list of previously mined data entries.
        # The list will be utilized to avoid duplicate data entries.
        self.dataEntries = {} # Key -> comment fullname, Value -> DataEntry
        with open(self.DATA_FILE_PATH, 'r', encoding='utf-8') as file:
            lines = file.read().split('\n')
        for line in lines:
            if len(line) != 0:
                submissionTitle, routeName, commentID = line.split('|')
                dataEntry = DataEntry(submissionTitle, routeName, commentID)
                self.dataEntries[dataEntry.commentFullName] = dataEntry

    
    def start(self):
        # Mine data.
        self.mineComments('ClimbingRouteBot')
        self.mineComments('MountainProjectBot')

        # Save data.
        print('\n\nSaving...')
        with open(self.DATA_FILE_PATH, 'w+', encoding='utf-8') as file:
            for _, dataEntry in self.dataEntries.items():
                file.write(dataEntry.toString() + '\n')


    def mineComments(self, username):
        print('\n\nChecking {}:'.format(username))

        # Get comments.
        comments = []
        for comment in self.reddit.redditor(username).comments.new(limit=None):
            comments.append(comment)

        # Mine comments.
        currentCommentCount = 0
        for comment in comments:

            if comment.fullname not in self.dataEntries.keys():
                routeName = self.determineRouteName(comment, username)
                if routeName is not None:
                    newDataEntry = DataEntry(self.cleanData(comment.submission.title),
                                             self.cleanData(routeName),
                                             comment.fullname)
                    self.dataEntries[comment.fullname] = newDataEntry

            currentCommentCount += 1
            sys.stdout.write('\r{}/{} comments mined.'.format(currentCommentCount, len(comments)))
            sys.stdout.flush()


    def determineRouteName(self, comment, username: str) -> str:
        routeName = None

        # Case: u/ClimbingRouteBot
        if username == 'ClimbingRouteBot':

            # Filter non-automated comments.
            if comment.body[0] == '#':
                for char in comment.body:

                    if routeName is None:
                        if char.isalpha():
                            routeName = char

                    else:
                        if char.isalpha() or char.isspace() or char == "'":
                            routeName += char
                        else:
                            break

        # Case: u/MountainProjectBot
        elif username == 'MountainProjectBot':

            # Filter non-toplevel comments.
            if comment.parent_id.startswith('t3'):

                # Filter non-automated comments.
                if comment.body[0] == '*':
                    routeName = comment.body.split('**')[1]

        return routeName


    def cleanData(self, data: str) -> str:
        data = re.sub(r'[^A-Za-z ]+', '', data)
        data = data.lower()
        dataTerms = data.split()
        data = ''
        for term in dataTerms:
            data += term + ' '
        data = data.strip()
        return data



DataMiner().start()

