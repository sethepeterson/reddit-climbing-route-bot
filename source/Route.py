from enum import Enum, auto
import math

# class Type(Enum):
#     SPORT = auto()
#     TRAD = auto()
#     BOULDER = auto()

class Route:
    REDDIT_NEW_LINE = '\n\n'
    NEW_LINE = '\n'

    def __init__(self):
        self.name = None
        self.location = None
        self.rating = None
        self.type = None
        self.score = None
        self.firstAccent = None
        self.description = None
        self.protection = None

        self.url = None
        self.descriptionUrl = None
        self.protectionUrl = None

    def toComment(self):
        # Route header.
        comment = '## [' + self.name + '](' + self.url + ' \"Mountain Project\")'
        comment += self.REDDIT_NEW_LINE + self.location

        # Horizontal divider.
        comment += self.REDDIT_NEW_LINE + '***'

        # Table Format.
        # Column count.
        comment += self.REDDIT_NEW_LINE + '||||'

        if self.firstAccent is not None:
            comment += '|'

        if self.description is not None:
            comment += '|'

        if self.protection is not None:
            comment += '|'

        # Allignment.
        comment += self.NEW_LINE + '|:-|:-|:-|'

        if self.firstAccent is not None:
            comment += ':-|'

        if self.description is not None:
            comment += ':-|'

        if self.protection is not None:
            comment += ':-|'

        # Legend row.
        comment += self.NEW_LINE + '|Rating|Score|Type|'

        if self.firstAccent is not None:
            comment += 'First Accent|'

        if self.description is not None:
            comment += 'Description|'

        if self.protection is not None:
            comment += 'Protection|'

        # Rating
        comment += self.NEW_LINE + '|' + self.rating + '|'

        # Score
        # Round star to nearest whole integer.
        starCount = self.score
        if starCount % 1 >= 0.5:
            starCount = math.ceil(self.score)
        else:
            starCount = math.floor(self.score)

        for _ in range(starCount):
            comment += '★'

        for _ in range(4 - starCount):
            comment += '☆'

        # Type
        comment += '|' + self.type + '|'

        # First Accent
        if self.firstAccent is not None:
            comment += self.firstAccent + '|'

        # Description of the route.
        if self.description is not None:
            comment += '[████████](' + self.descriptionUrl + ' \"' + self.description + '\")' + '|'

        # Protection of the route.
        if self.protection is not None:
            comment += '[███████](' + self.protectionUrl + ' \"' + self.protection + '\")' + '|'

        # Signature.
        comment += self.REDDIT_NEW_LINE + 'I am a bot, beep boop.'
        comment += self.REDDIT_NEW_LINE + '[Feedback](https://np.reddit.com/message/compose?to=ClimbingRouteBot \"PM\'s and comments are monitored! Feedback is welcome.\")'
        comment += '  |  [GitHub](https://github.com/sethepeterson/climbing-route-bot \"Source Code\")'

        return comment


