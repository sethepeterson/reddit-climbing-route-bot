from source.extensions import Extensions
import sys
import time


class UiManager:

    @staticmethod
    def notifyForSubmissionParsed(submission, possibleNames: list, possibleGrades: list):
        print('\n\nSubmission parsed.')
        print('\t\tTitle: {}'.format(submission.title))
        print('\t\tSubreddit: {}'.format(submission.subreddit))

        print('\t\tPossible route names:')
        for name in possibleNames:
            print('\t\t\t{}'.format(name))
        
        print('\t\tPossible route grades:')
        for grade in possibleGrades:
            print('\t\t\t{}'.format(grade))

    @staticmethod
    def notifyForRouteMatch(submission):
        print('\n\nRoutes matched!')
        print('Reddit url: {}'.format(Extensions.getSubmissionUrl(submission)))
        print('Submission title: {}'.format(submission.title))

    @staticmethod
    def getRouteChoice(routes: list) -> int:
        # Print options.
        print('\nRoute options:')
        for index, route in enumerate(routes):
            print('Option {}\t\tName: {}'.format(index, route.name))
            print('\t\t\tGrade: {}'.format(route.grade))
            print('\t\t\tUrl: {}\n'.format(route.url))
        print('Option {}\t\tNONE'.format(len(routes)))

        # Get input.
        while True:
            try:
                selection = int(input('Select an option: '))
                if selection >= 0 or selection <= len(routes):
                    return selection
            except ValueError:
                continue

    @staticmethod
    def wait(message: str, timeToWait: int, newLine: bool):
        if newLine:
            print()

        while timeToWait is not -1:
            minutes = int(timeToWait / 60)
            seconds = int(timeToWait - (minutes * 60))
            if seconds < 10:
                seconds = '0{}'.format(seconds)
            sys.stdout.write('\r{} Continuing in: {}:{}'.format(message, minutes, seconds))

            sys.stdout.flush()
            time.sleep(1)
            timeToWait -= 1
