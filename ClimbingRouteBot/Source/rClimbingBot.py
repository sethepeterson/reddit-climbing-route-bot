from SubmissionHandler import SubmissionHandler
import praw
import pdb
import re
import os
import time
import sys
import traceback
from datetime import datetime, timedelta

# Clear screen.
os.system('cls' if os.name == 'nt' else 'clear')

# Create list of replied post IDs from repliedPosts.txt.
repliedPosts = []
with open(os.path.dirname(__file__) + '\\..\\Logging\\repliedPosts.txt', 'r') as file:
    repliedPosts = file.read()
    repliedPosts = repliedPosts.split('\n')
    repliedPosts = list(filter(None, repliedPosts))
    file.close()

# Read credentialsFile and create the Reddit instance.
with open(os.path.dirname(__file__) + "\\..\\..\\..\\ClimbingRouteBotInfo.txt", "r") as file:
    credentials = file.read().split()
    reddit = praw.Reddit(client_id = credentials[0],
                        client_secret = credentials[1],
                        username = credentials[2],
                        password = credentials[3],
                        user_agent = credentials[4])
    subreddit = reddit.subreddit('climbing+Bouldering+socalclimbing+ClimbingPorn+ClimbingVids')
    file.close()

# Execute script.
REDDIT_NEW_LINE = '\n\n'
NEW_LINE = '\n'
submissionHandler = SubmissionHandler()
while True:
    for submission in subreddit.new(limit=100):

        try:
            if not submission.is_self:
                if submission.id not in repliedPosts:

                    # routeInfo = [routeName, locationChain, ydsRating, avgScore, routeType, firstAccent, description, mountainProjectLink]
                    routeInfo = submissionHandler.getRouteInfo(submission)

                    if routeInfo is not None:
                            # Route header.
                            comment = '## [' + routeInfo[0] + \
                                '](' + routeInfo[8] + \
                                ' \"Mountain Project\")' + REDDIT_NEW_LINE
                            comment += routeInfo[1] + REDDIT_NEW_LINE

                            # Table of info.
                            comment += '***\n\n'
                            # comment += 'Rating: ' + routeInfo[2] + '\n\n'
                            # comment += 'Score ' + routeInfo[3] + '\n\n'
                            # comment += 'Type: ' + routeInfo[4] + '\n\n'
                            # comment += 'FA: ' + routeInfo[5] + '\n\n'

                            comment += '|||' + NEW_LINE
                            comment += '|:-|:-:|' + NEW_LINE
                            comment += '|Rating| ' + routeInfo[2] +'|' + NEW_LINE
                            comment += '|Average Score| ' + routeInfo[3] + '|' + NEW_LINE
                            comment += '|Type| ' + routeInfo[4] + '|' + NEW_LINE
                            comment += '|First Ascent| ' + routeInfo[5] + '|' + REDDIT_NEW_LINE

                            # Description of the route.
                            if routeInfo[6] is not None:
                                comment += 'Description:\n\n'
                                comment += '>' + routeInfo[6]

                            # Protection of the route.
                            if routeInfo[7] is not None:
                                comment += '\n\nProtection:\n\n'
                                comment += '>' + routeInfo[7]

                            # Signature.
                            comment += '\n\nI am a bot, beep boop.\n\n'
                            comment += '[Feedback](https://np.reddit.com/message/compose?to=ClimbingRouteBot \"PM\'s and comments are monitored! Feedback is welcome.\")'

                            submission.reply(comment)
                            repliedPosts.append(submission.id)

                            # Update repliedPosts.txt
                            with open('repliedPosts.txt', 'w+') as file:
                                for postID in repliedPosts:
                                    file.write(postID + '\n')
                                file.close()

                            print()
                            timer = 400
                            while timer is not 0:
                                seconds = timedelta(seconds=timer)
                                dateTime = datetime(1, 1, 1) + seconds
                                sys.stdout.write('\rComment Posted. Continuing in: %s:%s' % (
                                    dateTime.minute, dateTime.second))
                                sys.stdout.flush()
                                time.sleep(1)
                                timer = timer - 1
        except:
            traceback.print_exc()
            time.sleep(1000)


print()
timer = 599
while timer is not 0:
    seconds = timedelta(seconds=timer)
    dateTime = datetime(1,1,1) + seconds
    sys.stdout.write('\rChecking for new submissions in: %s:%s' % (dateTime.minute, dateTime.second))
    sys.stdout.flush()
    time.sleep(1)
    timer = timer - 1

#Ideas
#-Need to improve submission title detection
    #remove all non uppercase words and group them, then search
    #beed to include bouldering
    #Remove all extra characters

#-Add checked submissions file
#-Add ★ for scores
#-Crawl more climbing subreddits
#-Add protection routeSection
#-Add !ClimbingRouteBot comment calling
#-Add readMe link

#Project Ideas
#-Mtb Trail bot
#-14er Bot
