from source.route import Route
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re


class MountainProjectScraper:

    def __init__(self):
        self.MTN_PROJECT_BASE_URL = 'https://www.mountainproject.com'
        self.MTN_PROJECT_SEARCH_URL = 'https://www.mountainproject.com/search?q='

        options = Options()
        options.headless = True
        options.add_argument('--log-level-3')
        chromeDriverPath = os.path.dirname(__file__) + '\\..\\tools\\chromedriver.exe'
        self.browser = webdriver.Chrome(chrome_options=options, executable_path=chromeDriverPath)

    def __del__(self):
        self.browser.quit()


    def getPossibleRoutes(self, possibleNames, possibleGrades):

        possibleRoutes = []
        for possibleName in possibleNames:

            # Create a list of Routes by searching mountain project.
            searchResults = self.searchMountainProject(possibleName)

            for possibleGrade in possibleGrades:

                # Check if any combination of the name and grades matches a search result.
                possibleRoute = Route(name=possibleName,
                                      grade=possibleGrade)

                # Check for matches within combinations.
                for possibleRouteMatch in searchResults:
                    if possibleRoute.matches(possibleRouteMatch):
                        possibleRoutes.append(possibleRouteMatch)

        routes = possibleRoutes.copy()
        possibleRoutes.clear()
        for route in routes:
            possibleRoutes.append(self.scrapeRouteInfo(route.url))

        return possibleRoutes

    
    def searchMountainProject(self, routeName):
        results = []

        # Determine Mountain Project search url for route.
        searchURL = self.MTN_PROJECT_SEARCH_URL
        for word in routeName.split():
            searchURL += word + '%20'
        searchURL = searchURL[:-3]  # Remove extra "%20".
        print('Determined search URL: ', searchURL)

        # Use selenium webdriver to load HTML to BeautifulSoup.
        searchPageSoup = self.getUrlSoup(searchURL)
        print('\rSelenium/BeautifulSoup HTML loaded.')

        # Find HTML containers with routes returned by search page.
        resultsDivSoup = searchPageSoup.find(
            'div', {'class': 'results-container has-sort'})
        if resultsDivSoup is None:
            print('No Mountain Project search results.')
            return results

        # Ensure search had results.
        containerHeader = resultsDivSoup.find('h2', {'class': 'float-xs-left'})
        if containerHeader.text != 'Routes':
            print('No Mountain Project search results.')
            return results

        # Store all results as a Route list.
        routesSectionsSoup = resultsDivSoup.find_all('tr', {'class': 'top'})
        for routeSection in routesSectionsSoup:
            linkAndNameDiv = routeSection.find('a')
            gradeDiv = routeSection.find('div', {'class': 'hidden-md-down'})

            route = Route(name=linkAndNameDiv.text,
                          grade=gradeDiv.text.split()[0],
                          url=self.MTN_PROJECT_BASE_URL + linkAndNameDiv.get('href'))
            results.append(route)
        
        # Return results.
        return results


    # Returns a list containing information on the route in the following format:
    # routeInfo = [routeName, locationChain, ydsRating, avgScore, routeType, firstAccent, description, mountainProjectLink]
    def scrapeRouteInfo(self, url):

        route = Route(url=url)

        # Use selenium webdriver to load HTML to BeautifulSoup.
        routePageSoup = self.getUrlSoup(url)
        print('\rSelenium/BeautifulSoup HTML loaded.')

        #############################
        ##### Gather route data #####
        #############################

        # Name
        route.name = routePageSoup.select('h1')[0].text.strip()

        # Location
        locationsLinks = list(routePageSoup.find('div', {'class': 'mb-half small text-warm'}).find_all('a'))
        area = None
        subarea = None
        if 'International' in locationsLinks[1].text:
            if 'Australia' in locationsLinks[2].text:
                area = self.getLocationName(locationsLinks[2])
                subarea = self.getLocationName(locationsLinks[3])
            else:
                area = self.getLocationName(locationsLinks[3])
                subarea = self.getLocationName(locationsLinks[4])
        else:
            area = self.getLocationName(locationsLinks[1])          # Examples: Nevada
            if area in locationsLinks[2].text:                      # Examples: East Nevada
                subarea = self.getLocationName(locationsLinks[3])
            else:
                subarea = self.getLocationName(locationsLinks[2])
        route.location = subarea + ', ' + area

        # Grade
        route.grade = routePageSoup.find('span', {'class': 'rateYDS'}).text.split()[0]

        # Rating
        avgScoreContainer = routePageSoup.find('span', {'id': re.compile('starsWithAvgText-*')})
        scoreText = avgScoreContainer.text.strip().split()[1]
        if '.' in scoreText:
            route.rating = float(scoreText)
        else:
            route.rating = int(scoreText)

        # Info
        typeText = routePageSoup.find(text="Type:").findNext('td').contents[0].strip()
        if typeText is not None:
            route.info = typeText
        
        # First accent
        firstAccent = routePageSoup.find(text="FA:").findNext('td').contents[0].strip()
        if 'unknown' not in firstAccent.lower():
            route.firstAccent = firstAccent

        # Description & Protection
        routeInfoParagraphHeaders = routePageSoup.find_all('div', {'class': 'mt-2'})
        routeInfoParagraphs = routePageSoup.find_all('div', {'class': 'fr-view'})
        paragraphIndex = 0
        for paragraphHeader in routeInfoParagraphHeaders:
            if 'Description' in paragraphHeader.text:
                route.descriptionUrl = route.url + '#' + paragraphHeader.find('a', recursive=False)['name']
                route.description = routeInfoParagraphs[paragraphIndex].text.replace('"', '')
            if 'Protection' in paragraphHeader.text:
                route.protectionUrl = route.url + '#' + paragraphHeader.find('a', recursive=False)['name']
                route.protection = routeInfoParagraphs[paragraphIndex].text.replace('"', '')
            paragraphIndex = paragraphIndex + 1

        print('HTML data scraped.')
        return route


    def getLocationName(self, locationLink):
        if '…' in locationLink.text:
            locationPageSoup = self.getUrlSoup(locationLink['href'])
            return locationPageSoup.select('h1')[0].text.strip()[:-9]

        else:
            return locationLink.text


    def getUrlSoup(self, url):
        self.browser.get(url)
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        return soup


