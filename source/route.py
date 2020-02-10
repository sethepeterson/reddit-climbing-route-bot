import math


class Route:
    REDDIT_NEW_LINE = '\n\n'
    NEW_LINE = '\n'

    def __init__(self, name = None, grade = None, url = None):
        self.name = name
        self.location = None
        self.grade = grade
        self.info = None
        self.rating = None
        self.firstAccent = None
        self.description = None
        self.protection = None

        self.url = url
        self.descriptionUrl = None
        self.protectionUrl = None

    def toComment(self) -> str:
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
            comment += self.REDDIT_NEW_LINE + 'Description:'
            comment += self.REDDIT_NEW_LINE + '>' + self.description

        # Signature.
        comment += self.REDDIT_NEW_LINE + \
            '[Feedback](https://np.reddit.com/message/compose?to=ClimbingRouteBot \"PM\'s and comments are monitored! Feedback is welcome.\")'
        comment += '  |  [GitHub](https://github.com/sethepeterson/climbing-route-bot \"Source Code\")'
        # comment += '  |  ^(I am a bot, beep boop.)'

        return comment

    def matches(self, other) -> bool:

        # Name
        if self.name.lower() == other.name.lower():

            # Direct match.
            if self.grade == other.grade:
                return True

            # If self's grade is varied. Example: V7-8
            elif 'V' in self.grade and '-' in self.grade:
                #If other's grade equals either option. Example: other's grade = V7 or V8
                if self.grade[0:2] == other.grade[1] or self.grade[0] + self.grade[3] == other.grade:
                    return True

            # If other's grade is varied. Example: V7-8
            elif 'V' in other.grade and '-' in other.grade:
                #If self's grade equals either option. Example: self's grade = V7 or V8
                if other.grade[0:2] == self.grade[1] or other.grade[0] + other.grade[3] == self.grade:
                    return True

            # If self's grade is varied. Example: 5.10a/b
            elif '/' in self.grade:
                # If other's grade equals either option. Example: other's grade = 5.10a or 5.10b
                if other.grade == self.grade[0:5] or other.grade == self.grade[0:4] + self.grade[6]:
                    return True

            # If other's grade is varied. Example: 5.10a/b
            elif '/' in other.grade:
                # If self's grade equals either option. Example: self's grade = 5.10a or 5.10b
                if self.grade == other.grade[0:5] or self.grade == other.grade[0:4] + other.grade[6]:
                    return True
            
        # No match.
        return False

