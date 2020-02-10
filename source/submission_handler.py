from source.moutain_project_scraper import MountainProjectScraper
from source.ui_manager import UiManager
from source.extensions import Extensions
import re


class SubmissionHandler:

    def __init__(self):
        self.mountainProjectScraper = MountainProjectScraper()
        self.titleFillerWords = ['of', 'to', 'in', 'the']


    # Returns a Route object corresponding to the submission.
    def getRoutes(self, submission):

        possibleNames = self.getPossibleRouteNames(submission.title)
        possibleGrades = self.getPossibleRouteGrades(submission.title)

        if Extensions.isNotEmpty(possibleNames) and Extensions.isNotEmpty(possibleGrades):
            UiManager.notifyForSubmissionParsed(submission, possibleNames, possibleGrades)
            return self.mountainProjectScraper.getPossibleRoutes(possibleNames, possibleGrades)
        
    
    def getPossibleRouteNames(self, submissionTitle):

        # Create list of all words with all non-aplhabet chars removed.
        revisedSubmissionTitleWords = []
        for word in submissionTitle.split():
            revisedWord = re.sub('[^a-zA-Z]', '', word).strip()
            if revisedWord != '':
                revisedSubmissionTitleWords.append(revisedWord)

        # Determine possible route names.
        possibleRouteNames = []
        possibleRouteName = ''
        for index, titleWord in enumerate(revisedSubmissionTitleWords):

            # Case: the title word is not an emtpy string.
            if Extensions.isNotEmpty(titleWord):

                # Case: the title word is marked as a pronoun.
                if Extensions.startsWithUpper(titleWord):
                    possibleRouteName += titleWord + ' '
                    
                # Case: the title word is a filler word and the current route name is not empty.
                elif titleWord in self.titleFillerWords and Extensions.isNotEmpty(possibleRouteName):

                    # Check if the filler word is bounded by an upper-cased term.
                    boundedByUpperCase = False
                    for followingTerm in revisedSubmissionTitleWords[index + 1:]:

                        # Case: the following term is upper-cased.
                        if Extensions.startsWithUpper(followingTerm):
                            boundedByUpperCase = True

                        # Case: the following term is a filler-word.
                        elif followingTerm in self.titleFillerWords:
                            continue
                            
                        # Case: the following term is neither upper-case or a filler-word.
                        else:
                            break
                    
                    if boundedByUpperCase:
                        possibleRouteName += titleWord + ' '

                # Case: the current route name is not empty.
                elif Extensions.isNotEmpty(possibleRouteName):
                    possibleRouteNames.append(possibleRouteName.strip())
                    possibleRouteName = ''

        # Append current route name in the case of route title being in the end of the title.
        if Extensions.isNotEmpty(possibleRouteName):
            possibleRouteNames.append(possibleRouteName.strip())

        # Check for unbounded filler words in possible route names.
        return possibleRouteNames

        # # Remove extra characters from possible route titles... parentheses, whitespace etc.
        # for possibleRouteName in possibleRouteNames:
        #     possibleRouteName = re.sub(
        #         '([^\s\w]|_)+', '', possibleRouteName).strip()


    def getPossibleRouteGrades(self, submissionTitle):

        possibleGrades = []
        for titleWord in submissionTitle.split():

            # Case: the title word contains a numeric character.
            containsNumericChar = False
            for char in titleWord:
                if char.isdigit():
                    containsNumericChar = True
                    break
            if containsNumericChar:
                gradeSearch = re.search(
                    '((5\.)?\d+[+-]?[a-dA-D]?)|([vV]\d+([/|\-]\d+)?)', titleWord)

                # Case: the title word matches a grade pattern.
                if gradeSearch != None:
                    grade = gradeSearch.group(0)
                    possibleGrades.append(self.fixPossibleGrade(grade))

        return possibleGrades


    def fixPossibleGrade(self, grade):

        # Example: V7/8 -> V7-8
        if '\\' in grade or '/' in grade:
            grade = grade[0:2] + '-' + grade[3]

        # Example: v10 -> V10
        if 'v' in grade:
            grade = grade.upper()

        # Example: 11b -> 5.11b
        if not 'V' in grade and not '5.' in grade:
            grade = '5.' + grade

        # Example: 5.10B -> 5.10b
        if 'A' in grade or 'B' in grade or 'C' in grade or 'D' in grade:
            grade = grade.lower()

        return grade


