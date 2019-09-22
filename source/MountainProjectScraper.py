from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re

class MountainProjectScraper:

    # Scrapes the Mountain Project search page with the input as the possibleRouteName.
    # Checks all resulting routes against redditRouteRating, if found it returns the URL to the route page.
    def determineMountainProjectURL(self, possibleRouteName, redditRouteRating):
        # Determine Mountain Project search url for route.
        searchURL = 'https://www.mountainproject.com/search?q='
        for word in possibleRouteName.split(
        ): searchURL = searchURL + word + '%20'
        searchURL = searchURL[:-3]  # Remove extra "%20".
        print('Determined search URL: ', searchURL)

        # Use selenium webdriver to load HTML to BeautifulSoup.
        chromeDriverPath = os.path.dirname( __file__) + '\\..\\tools\\chromedriver.exe'
        options = Options()
        options.headless = True
        options.add_argument('--log-level-3')
        browser = webdriver.Chrome(
            chrome_options=options, executable_path=chromeDriverPath)

        browser.get(searchURL)
        searchPageHtml = browser.page_source
        browser.quit()
        searchPageSoup = BeautifulSoup(searchPageHtml, 'html.parser')
        print('\rSelenium/BeautifulSoup HTML loaded.')

        # Find HTML containers with routes returned by search page.
        resultsDivSoup = searchPageSoup.find(
            'div', {'class': 'results-container has-sort'})
        if resultsDivSoup is None:
            print('No Mountain Project search results.')
            return None

        # Ensure search had results.
        containerHeader = resultsDivSoup.find('h2', {'class': 'float-xs-left'})
        if containerHeader.text != 'Routes':
            print('No Mountain Project search results.')
            return None

        # Store all routes' info as a tripule list... (name, rating, link).
        routesSectionsSoup = resultsDivSoup.find_all('tr', {'class': 'top'})
        mtnProjectRoutes = []
        for routeSection in routesSectionsSoup:
            routeLinkAndName = routeSection.find('a')
            routeGrade = routeSection.find('div', {'class': 'hidden-md-down'})
            mtnProjectRoutes.append((routeLinkAndName.text, routeGrade.text.split()[
                                    0], routeLinkAndName.get('href')))

        # Each route displayed on the search page is now stored as a tuple in mtnProjectRoutes... (name, rating, link).
        # Determine a route and submission info match.
        for mtnProjectRoute in mtnProjectRoutes:
            if possibleRouteName == mtnProjectRoute[0]:
                if redditRouteRating == mtnProjectRoute[1]:
                    return 'https://www.mountainproject.com' + mtnProjectRoute[2]

                # If redditRoute rating is varied. Example: V7-8
                if 'V' in redditRouteRating and '-' in redditRouteRating:
                    #If mtnProjectRoute equals either option. Example: mtnProjectRoute = V7 or V8
                    if redditRouteRating[0:2] == mtnProjectRoute[1] or redditRouteRating[0] + redditRouteRating[3] == mtnProjectRoute[1]:
                        return 'https://www.mountainproject.com' + mtnProjectRoute[2]

                # If mtnProjectRoute rating is varied. Example: 5.10a/b
                if '/' in mtnProjectRoute[1]:
                    # If redditRouteRating equal either option. Example: redditRouteRating = 5.10a or 5.10b
                    if redditRouteRating == mtnProjectRoute[1][0:5] or redditRouteRating == mtnProjectRoute[1][0:4] + mtnProjectRoute[1][6]:
                        return 'https://www.mountainproject.com' + mtnProjectRoute[2]

    # Calls determineMountainProjectURL() until a matching route is found.
    # Returns the URL of the matching route page if found. Returns None otherwise.
    def getRouteWebAddress(self, titleInfoList):
        # Determine route info from Reddit submission.
        redditPossibleRouteNames = titleInfoList[0]
        redditRouteRating = titleInfoList[1]

        for possibleRouteName in redditPossibleRouteNames:
            print(possibleRouteName)
            matchingRouteInfo = self.determineMountainProjectURL(possibleRouteName, redditRouteRating)
            if matchingRouteInfo is not None:
                return [possibleRouteName, matchingRouteInfo]

        # If no match found.
        print('No matching route found.')
        return None

    # Returns a list containing information on the route in the following format:
    # routeInfo = [routeName, locationChain, ydsRating, avgScore, routeType, firstAccent, description, mountainProjectLink]
    def scrapeRouteInfo(self, titleInfoList):
        routeNameAndWebAddress = self.getRouteWebAddress(titleInfoList)
        if routeNameAndWebAddress is None:
            return None
        routeName = routeNameAndWebAddress[0]
        routeWebAddress = routeNameAndWebAddress[1]
        print('Determined matching route URL: ', routeWebAddress)

        # Use selenium webdriver to load HTML to BeautifulSoup.
        options = Options()
        options.headless = True
        options.add_argument('--log-level-3')
        chromeDriverPath = os.path.dirname(__file__) + '\\..\\tools\\chromedriver.exe'
        browser = webdriver.Chrome(chrome_options=options, executable_path=chromeDriverPath)
        browser.get(routeWebAddress)
        routePageHtml = browser.page_source
        browser.quit()
        routePageSoup = BeautifulSoup(routePageHtml, 'html.parser')
        print('\rSelenium/BeautifulSoup HTML loaded.')

        #############################
        ######Gather route data######
        #############################
        # Location chain
        locationsLinks = routePageSoup.find('div', {'class': 'mb-half small text-warm'}).find_all('a')
        locationChain = ""
        for locationLink in locationsLinks:
            locationChain += locationLink.text + ' -> '
        locationChain = locationChain.replace('All Locations -> ', '') # Remove header.
        locationChain = locationChain[:-4] # Remove extra ' -> '.

        # YDS rating
        ydsRating = routePageSoup.find('span', {'class': 'rateYDS'}).text

        # Average score
        avgScoreContainer = routePageSoup.find('span', {'id': re.compile('starsWithAvgText-*')})
        avgScore = re.sub(' +', ' ', avgScoreContainer.text.strip().replace('\n',''))
        avgScore = avgScore[5:] # Remove "Avg: "

        # Route type
        routeType = routePageSoup.find(text="Type:").findNext('td').contents[0].strip()

        # First accent
        firstAccent = routePageSoup.find(text="FA:").findNext('td').contents[0].strip()

        # Description & Protection
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
