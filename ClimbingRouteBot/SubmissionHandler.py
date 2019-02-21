from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import praw
import re
import sys
import time
import os

#cd C:\Users\sethe\OneDrive\Documents\Projects\rClimbingRedditBot\ClimbingRouteBot
#./rClimbingBot.py

class SubmissionHandler:
    submission = None

    def __init__(self, submission):
        self.submission = submission

    def getTitleInfo(self):
        #Represents current titleWord index.
        titleWordIndex = -1
        #Represents the index of the titleWord that contains a rating.
        ratingIndex = 0

        #Split submission title into list of submissionTitleWords.
        submissionTitleWords = self.submission.title.split()
        for titleWord in submissionTitleWords:
            titleWordIndex = titleWordIndex + 1

            #If current titleWord contains any rating  -->  note current index in ratingIndex.
            ratings = ['4','5','6','7','8','9','10','11','12','13','14','15']
            ratings.extend(['VB','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10'])
            if any (rating in titleWord for rating in ratings):
                ratingIndex = titleWordIndex

                #The following lines of code determines the probable name of the route:
                routeName = ''
                titleWordIndex = titleWordIndex - 1 #Set index to titleWord before rating.
                while titleWordIndex > -1  and (submissionTitleWords[titleWordIndex][0].isupper() or submissionTitleWords[titleWordIndex][1].isupper()): #If substirng is a pronoun, add to routeName.
                    routeName = submissionTitleWords[titleWordIndex] + ' ' + routeName
                    titleWordIndex = titleWordIndex - 1

                #Remove extra characters from values if needed... parentheses, whitespace etc.
                routeName = re.sub('([^\s\w]|_)+', '', routeName).strip()
                rating = re.search('((5\.)?\d+[+-]?[a-dA-D]?)|([vV]\d+([/|\-]\d+)?)', submissionTitleWords[ratingIndex]).group(0)

                ##############
                #Rating fixes#
                ##############
                #Example: V7/8 -> V7-8
                if '\\' in rating or '/' in rating:
                    rating = rating[0:2] + '-' + rating[3]

                #Example: v10 -> V10
                if 'v' in rating:
                    rating = rating.upper()

                #Example: 11b -> 5.11b
                if not 'V' in rating and not '5.' in rating:
                    rating = '5.' + rating

                #Example: 5.10B -> 5.10b
                if 'A' in rating or 'B' in rating or 'C' in rating or 'D' in rating:
                    rating = rating.lower()

                # submissionTitleUpperWords = []
                # for titleWord in submissionTitleWords:
                #     if titleWord[0].isupper():
                #         submissionTitleUpperWords.append(titleWord)
                #     else:
                #         submissionTitleUpperWords.append('|')
                #
                # possibleRouteTitles = []
                # possibleRouteTitle = ""
                # for upperWord in submissionTitleUpperWords:
                #     if upperWord != '|':
                #         possibleRouteTitle = possibleRouteTitle + upperWord + ' '
                #     else:
                #         if possibleRouteTitle != "":
                #             possibleRouteTitles.append(possibleRouteTitle)
                #         possibleRouteTitle = ""


                time.sleep(10)
                print('\n\n\nParsing new submission.')
                print('Subreddit: ', self.submission.subreddit.display_name)
                print('Submission title: ', self.submission.title)
                seperator = "--------------------"
                for char in self.submission.title:
                    seperator = seperator + '-'
                print(seperator)
                #print('Possible Route Titles')
                # for word in possibleRouteTitles:
                #     print(word)
                print('Detected route name: ', routeName)
                print('Detected rating: ', rating)

                return [routeName,rating]


    def getRouteWebAddress(self, titleInfoList):
        #Determine route info from Reddit submission.
        redditRouteName = titleInfoList[0]
        redditRouteRating = titleInfoList[1]

        #Determine Mountain Project search url for route.
        searchURL = 'https://www.mountainproject.com/search?q='
        for word in redditRouteName.split(): searchURL = searchURL + word + '%20'
        searchURL = searchURL[:-3] #Remove extra "%20".
        print('Determined search URL: ', searchURL)

        #Use selenium webdriver to load HTML to BeautifulSoup.
        options = Options()
        options.headless = True
        options.add_argument('--log-level-3')
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(searchURL)
        searchPageHtml = browser.page_source
        browser.quit()
        searchPageSoup = BeautifulSoup(searchPageHtml, 'html.parser')
        print('\rSelenium/BeautifulSoup HTML loaded.')

        #Find HTML containers with routes returned by search page.
        resultsDivSoup = searchPageSoup.find('div', {'class': 'results-container has-sort'})
        if resultsDivSoup is None:
            print('No Mountain Project search results.')
            return None

        #Ensure search had results.
        containerHeader = resultsDivSoup.find('h2', {'class': 'float-xs-left'})
        if containerHeader.text != 'Routes':
            print('No Mountain Project search results.')
            return None

        #Store all routes' info as a tripule list... (name, rating, link).
        routesSectionsSoup = resultsDivSoup.find_all('tr', {'class': 'top'})
        mtnProjectRoutes = []
        for routeSection in routesSectionsSoup:
            routeLinkAndName = routeSection.find('a')
            routeGrade = routeSection.find('div', {'class': 'hidden-md-down'})
            mtnProjectRoutes.append((routeLinkAndName.text, routeGrade.text.split()[0], routeLinkAndName.get('href')))

        #Each route displayed on the search page is now stored as a tuple in mtnProjectRoutes... (name, rating, link).
        #Determine a route and submission info match.
        for mtnProjectRoute in mtnProjectRoutes:
            if redditRouteName == mtnProjectRoute[0]:
                if redditRouteRating == mtnProjectRoute[1]:
                    return 'https://www.mountainproject.com' + mtnProjectRoute[2]

                #If redditRoute rating is varied. Example: V7-8
                if 'V' in redditRouteRating and '-' in redditRouteRating:
                    #If mtnProjectRoute equals either option. Example: mtnProjectRoute = V7 or V8
                    if redditRouteRating[0:2] == mtnProjectRoute[1] or redditRouteRating[0] + redditRouteRating[3] == mtnProjectRoute[1]:
                        return 'https://www.mountainproject.com' + mtnProjectRoute[2]

                #If mtnProjectRoute rating is varied. Example: 5.10a/b
                if '/' in mtnProjectRoute[1]:
                    #If redditRouteRating equal either option. Example: redditRouteRating = 5.10a or 5.10b
                    if redditRouteRating == mtnProjectRoute[1][0:5] or redditRouteRating == mtnProjectRoute[1][0:4] + mtnProjectRoute[1][6]:
                        return 'https://www.mountainproject.com' + mtnProjectRoute[2]

        #If no match found.
        print('No matching route found.')
        return None


    def getRouteInfo(self, titleInfoList):
        routeWebAddress = self.getRouteWebAddress(titleInfoList)
        if routeWebAddress is None:
            return None
        print('Determined matching route URL: ', routeWebAddress)

        #Use selenium webdriver to load HTML to BeautifulSoup.
        options = Options()
        options.headless = True
        options.add_argument('--log-level-3')
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(routeWebAddress)
        routePageHtml = browser.page_source
        browser.quit()
        routePageSoup = BeautifulSoup(routePageHtml, 'html.parser')
        print('\rSelenium/BeautifulSoup HTML loaded.')

        #############################
        ######Gather route data######
        #############################
        #Name
        routeName = titleInfoList[0]

        #Location chain
        locationsLinks = routePageSoup.find('div', {'class': 'mb-half small text-warm'}).find_all('a')
        locationChain = ""
        for locationLink in locationsLinks:
            locationChain += locationLink.text + ' -> '
        locationChain = locationChain.replace('All Locations -> ', '') #Remove header.
        locationChain = locationChain[:-4] #Remove extra ' -> '.

        #YDS rating
        ydsRating = routePageSoup.find('span', {'class': 'rateYDS'}).text

        #Average score
        avgScoreContainer = routePageSoup.find('span', {'id': re.compile('starsWithAvgText-*')})
        avgScore = re.sub(' +', ' ', avgScoreContainer.text.strip().replace('\n',''))

        #Route type
        routeType = routePageSoup.find(text="Type:").findNext('td').contents[0].strip()

        #First accent
        firstAccent = routePageSoup.find(text="FA:").findNext('td').contents[0].strip()

        #Description & Protection
        routeInfoParagraphHeaders = routePageSoup.find_all('div', {'class': 'mt-2'})
        routeInfoParagraphs = routePageSoup.find_all('div', {'class': 'fr-view'})
        description = None
        protection = None
        paragraphIndex = 0
        for paragraphHeader in routeInfoParagraphHeaders:
            if 'Description' in paragraphHeader.text:
                description = routeInfoParagraphs[paragraphIndex].text
            if 'Protection' in paragraphHeader.text:
                protection = routeInfoParagraphs[paragraphIndex].text
            paragraphIndex = paragraphIndex + 1

        print('HTML data scraped.')
        return [routeName, locationChain, ydsRating, avgScore, routeType, firstAccent, description, protection, routeWebAddress]
