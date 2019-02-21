from SubmissionHandler import SubmissionHandler
import praw
import pdb
import re
import os
import time
import sys
from datetime import datetime, timedelta

#Clear screen.
os.system('cls' if os.name == 'nt' else 'clear')

#Create list of replied post IDs from repliedPosts.txt.
repliedPosts = []
with open('repliedPosts.txt', 'r') as file:
    repliedPosts = file.read()
    repliedPosts = repliedPosts.split('\n')
    repliedPosts = list(filter(None, repliedPosts))

# Create the Reddit instance and log in.
reddit = praw.Reddit(client_id = 'LMxeepkXA8W5kg',
                     client_secret = '834ts23jIxsRQO0_qH_Vq9eeGY0',
                     username = 'ClimbingRouteBot',
                     password = '$4Bluiloveyou',
                     user_agent = 'Seth Peterson 2019')
subreddit = reddit.subreddit('climbing+Bouldering+ClimbingPorn+ClimbingVids')

while True:
    for submission in subreddit.new(limit=100):
        # if not submission.is_self:
        #
        #     if submission.id not in repliedPosts:
        #         submissionHandler = SubmissionHandler(submission)
        #         titleInfoList = submissionHandler.getTitleInfo()
        #
        #         if titleInfoList is not None and titleInfoList[0] != '' and titleInfoList[1] != '':
        #             #routeInfo = [routeName, locationChain, ydsRating, avgScore, routeType, firstAccent, description, mountainProjectLink]
        #             routeInfo = submissionHandler.getRouteInfo(titleInfoList)
        #
        #             if routeInfo is not None:
        #                 #Route header.
        #                 comment = '## [' + routeInfo[0] + '](' + routeInfo[8] +' \"Mountain Project\")\n\n'
        #                 comment += routeInfo[1] + '\n\n'
        #
        #                 #Table of info.
        #                 comment += '***\n\n'
        #                 comment += 'Rating: ' + routeInfo[2] + '\n\n'
        #                 comment += 'Score ' + routeInfo[3] + '\n\n'
        #                 comment += 'Type: ' + routeInfo[4] + '\n\n'
        #                 comment += 'FA: ' + routeInfo[5] + '\n\n'
        #
        #                 #Description of the route.
        #                 if routeInfo[6] is not None:
        #                     comment += 'Description:\n\n'
        #                     comment += '>' + routeInfo[6]
        #
        #                 #Protection of the route.
        #                 if routeInfo[7] is not None:
        #                     comment += '\n\nProtection:\n\n'
        #                     comment += '>' + routeInfo[7]
        #
        #                 #Signature.
        #                 comment += '\n\nI am a bot, beep boop.'
        #
        #                 submission.reply(comment)
        #                 repliedPosts.append(submission.id)
        #
        #                 #Update repliedPosts.txt
        #                 with open('repliedPosts.txt', 'w+') as file:
        #                     for postID in repliedPosts:
        #                         file.write(postID + '\n')
        #
        #                 print()
        #                 timer = 400
        #                 while timer is not 0:
        #                     seconds = timedelta(seconds=timer)
        #                     dateTime = datetime(1,1,1) + seconds
        #                     sys.stdout.write('\rComment Posted. Continuing in: %s:%s' % (dateTime.minute, dateTime.second))
        #                     sys.stdout.flush()
        #                     time.sleep(1)
        #                     timer = timer - 1
        try:
            if not submission.is_self:

                if submission.id not in repliedPosts:
                    submissionHandler = SubmissionHandler(submission)
                    titleInfoList = submissionHandler.getTitleInfo()

                    if titleInfoList is not None and titleInfoList[0] != '' and titleInfoList[1] != '':
                        #routeInfo = [routeName, locationChain, ydsRating, avgScore, routeType, firstAccent, description, mountainProjectLink]
                        routeInfo = submissionHandler.getRouteInfo(titleInfoList)

                        if routeInfo is not None:
                            #Route header.
                            comment = '## [' + routeInfo[0] + '](' + routeInfo[8] + ' \"Mountain Project\")\n\n'
                            comment += routeInfo[1] + '\n\n'

                            #Table of info.
                            comment += '***\n\n'
                            comment += 'Rating: ' + routeInfo[2] + '\n\n'
                            comment += 'Score ' + routeInfo[3] + '\n\n'
                            comment += 'Type: ' + routeInfo[4] + '\n\n'
                            comment += 'FA: ' + routeInfo[5] + '\n\n'

                            #Description of the route.
                            if routeInfo[6] is not None:
                                comment += 'Description:\n\n'
                                comment += '>' + routeInfo[6]

                            #Protection of the route.
                            if routeInfo[7] is not None:
                                comment += '\n\nProtection:\n\n'
                                comment += '>' + routeInfo[7]

                            #Signature.
                            comment += '\n\nI am a bot, beep boop.\n\n'
                            comment += '[Feedback](https://np.reddit.com/message/compose?to=ClimbingRouteBot \"PM\'s and comments are monitored! Feedback is welcome.\")'

                            submission.reply(comment)
                            repliedPosts.append(submission.id)

                            #Update repliedPosts.txt
                            with open('repliedPosts.txt', 'w+') as file:
                                for postID in repliedPosts:
                                    file.write(postID + '\n')

                            print()
                            timer = 400
                            while timer is not 0:
                                seconds = timedelta(seconds=timer)
                                dateTime = datetime(1,1,1) + seconds
                                sys.stdout.write('\rComment Posted. Continuing in: %s:%s' % (dateTime.minute, dateTime.second))
                                sys.stdout.flush()
                                time.sleep(1)
                                timer = timer - 1
        except:
            print('\nAn exception occured.\n')


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
