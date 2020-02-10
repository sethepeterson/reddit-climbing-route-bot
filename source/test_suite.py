from source.submission_handler import SubmissionHandler

class TestSuite:

    def __init__(self):
        self.submissionHandler = SubmissionHandler()

        # Test cases will be tripule ->
        #   First: submission title
        #   Second: possible title list
        #   Third: possible grade list
        self.testCases = []
        self.testCases.append(
            ('Austin, TX is a great city for accessible climbing! "Diving For Rocks" 5.10d located 15 minutes from downtown. [OC]',
            ['Austin TX','Diving For Rocks', 'OC'],
            ['5.10d','5.15'])
        )
        self.testCases.append(
            ('Me on Here Come the Snakes, 12c at Jackson Falls, IL',
            ['Me','Here Come the Snakes','Jackson Falls IL'],
            ['5.12c'])
        )
        self.testCases.append(
            ('Me on Here Come the Snakes the, 12c at Jackson Falls, IL',
             ['Me', 'Here Come the Snakes', 'Jackson Falls IL'],
             ['5.12c'])
        )
    
    def start(self):
        for index, testCase in enumerate(self.testCases):
            names = self.submissionHandler.getPossibleRouteNames(testCase[0])
            grades = self.submissionHandler.getPossibleRouteGrades(testCase[0])

            if names != testCase[1] or grades != testCase[2]:
                print('\nTest case {}: FAILED'.format(index))
                print('\t\tnames = {}'.format(names))
                print('\t\tgrades = {}'.format(grades))


            else:
                print('\nTest case {}: PASSED'.format(index))

