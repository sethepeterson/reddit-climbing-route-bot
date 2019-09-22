from bs4 import BeautifulSoup
from MountainProjectScraper import MountainProjectScraper
import praw
import re
import sys
import time
import os

class SubmissionHandler:
    # Returns a list containing information on the route in the following format:
    # routeInfo = [routeName, locationChain, ydsRating, avgScore, routeType, firstAccent, description, mountainProjectLink]
    def getRouteInfo(self, submission):
        titleInfoList = self.getTitleInfo(submission)
        if titleInfoList is None:
            return None
        
        mountainProjectScraper = MountainProjectScraper()
        routeInfo = mountainProjectScraper.scrapeRouteInfo(titleInfoList)
        return routeInfo


    # Returns a list of possible names of the route and the route's rating.
    # Returns None if no rating is determined.
    def getTitleInfo(self, submission):
        # Represents the index of the titleWord that contains a rating.
        ratingIndex = 0
        ratings = ['4','5','6','7','8','9','10','11','12','13','14','15']
        ratings.extend(['V0','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10'])
        titleContainsRating = False
        for rating in ratings:
            if rating in submission.title:
                titleContainsRating = True

        if titleContainsRating:
            # Create list of all words with all non-aplhabet chars removed.
            originalSubmisonTitleWords = submission.title.split()
            revisedSubmissionTitleWords = []
            for word in originalSubmisonTitleWords:
                revisedWord = re.sub('[^a-zA-Z]', '', word).strip()
                if revisedWord != '':
                    revisedSubmissionTitleWords.append(revisedWord)

            # Determine rating index.
            ratingIndex = None
            for index,titleWord in enumerate(originalSubmisonTitleWords):
                for rating in ratings:
                    if rating in titleWord:
                        ratingIndex = index

            # Determine possible route names.
            fillerWords = ['test']
            possibleRouteNames = []
            possibleRouteName = ''
            for titleWord in revisedSubmissionTitleWords:
                if (titleWord[0].isupper() and len(titleWord) > 1) or titleWord in fillerWords:
                    possibleRouteName += titleWord + ' '
                elif possibleRouteName != '' and possibleRouteName[0] != 'V':
                    possibleRouteNames.append(possibleRouteName.strip())
                    possibleRouteName = ''

            # Remove extra characters from values if needed... parentheses, whitespace etc.
            for possibleRouteName in possibleRouteNames:
                possibleRouteName = re.sub('([^\s\w]|_)+', '', possibleRouteName).strip()
            rating = submission.title.split()[ratingIndex]
            revisedRating = re.search('((5\.)?\d+[+-]?[a-dA-D]?)|([vV]\d+([/|\-]\d+)?)', originalSubmisonTitleWords[ratingIndex])
            if revisedRating != None:
                rating = revisedRating.group(0)

            ##############
            #Rating fixes#
            ##############
            #Example: V7/8 -> V7-8
            if '\\' in rating or '/' in rating:
                rating = rating[0:2] + '-' + rating[3]

            # Example: v10 -> V10
            if 'v' in rating:
                rating = rating.upper()

            # Example: 11b -> 5.11b
            if not 'V' in rating and not '5.' in rating:
                rating = '5.' + rating

            # Example: 5.10B -> 5.10b
            if 'A' in rating or 'B' in rating or 'C' in rating or 'D' in rating:
                rating = rating.lower()

            print('\n\n\nParsing new submission.')
            print('Subreddit: ', submission.subreddit.display_name)
            print('Submission title: ', submission.title)
            seperator = "--------------------"
            for char in submission.title:
                seperator = seperator + '-'
            print(seperator)
            print('Possible route names:')
            for possibleRouteName in possibleRouteNames:
                print('\t\"' + possibleRouteName + '\"')
            print('Detected rating: ', rating)

            return [possibleRouteNames, rating]

        # No rating found.
        return None

