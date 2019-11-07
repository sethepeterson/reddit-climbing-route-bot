
class Extensions:

    @staticmethod
    def isEmpty(obj: object) -> bool:
        return obj is not None and len(obj) == 0

    @staticmethod
    def isNotEmpty(obj) -> bool:
        return obj is not None and len(obj) != 0

    @staticmethod
    def startsWithUpper(string: str) -> bool:
        if len(string) == 0:
            return False

        return string[0].isupper()

    @staticmethod
    def startsWithLower(string: str) -> bool:
        if len(string) == 0:
            return False

        return string[0].islower()

    @staticmethod
    def getSubmissionUrl(submission) -> str:
        return 'https://www.reddit.com{}'.format(submission.permalink)
