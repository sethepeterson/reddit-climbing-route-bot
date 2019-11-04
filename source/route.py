import math


class Route:
    REDDIT_NEW_LINE = '\n\n'
    NEW_LINE = '\n'

    def __init__(self):
        self.name = None
        self.location = None
        self.grade = None
        self.info = None
        self.rating = None
        self.firstAccent = None
        self.description = None
        self.protection = None

        self.url = None
        self.descriptionUrl = None
        self.protectionUrl = None

    def toComment(self):
        # Route header.
        comment = '### [' + self.name + \
            '](' + self.url + ' \"Mountain Project\")'

        # Horizontal divider.
        # comment += self.REDDIT_NEW_LINE + '***'

        # Table Format.
        # Legend row.
        comment += self.NEW_LINE + '|Grade|Rating|Location|Info|'

        if self.firstAccent is not None:
            comment += 'First Accent|'

        # Allignment.
        comment += self.NEW_LINE + '|:-|:-|:-|:-|'

        if self.firstAccent is not None:
            comment += ':-|'

        # Grade
        comment += self.NEW_LINE + '|' + self.grade + '|'

        # Rating
        # Round star to nearest whole integer.
        starCount = self.rating
        if starCount % 1 >= 0.5:
            starCount = math.ceil(self.rating)
        else:
            starCount = math.floor(self.rating)

        for _ in range(starCount):
            comment += '★'

        for _ in range(4 - starCount):
            comment += '☆'

        # Location
        comment += '|' + self.location + '|'

        # Info
        comment += self.info + '|'

        # First Accent
        if self.firstAccent is not None:
            comment += self.firstAccent + '|'

        # Description of the route.
        if self.description is not None:
            comment += self.REDDIT_NEW_LINE + '>' + self.description

        # Signature.
        comment += self.REDDIT_NEW_LINE + \
            '[Feedback](https://np.reddit.com/message/compose?to=ClimbingRouteBot \"PM\'s and comments are monitored! Feedback is welcome.\")'
        comment += '  |  [GitHub](https://github.com/sethepeterson/climbing-route-bot \"Source Code\")'
        # comment += '  |  ^(I am a bot, beep boop.)'

        return comment
