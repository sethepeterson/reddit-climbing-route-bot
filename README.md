# Reddit Climbing Route Bot

## Summary 
A Reddit bot that identifies submissions containing pictures of rock climbing routes and publishes comments with information about the corresponding route that is scraped from Mountain Project.

#### Requirements

- Python 3
- Google Chrome Version 77.0.3865.90

#### Dependencies

- [PRAW](https://github.com/praw-dev/praw "GitHub") </br>
- [Selenium](https://github.com/seleniumbase/SeleniumBase "GitHub") </br>
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/ "Documentation")



</br></br>
## Execution
To execute the script you must [sign up](https://www.reddit.com/prefs/apps "Sign up for Reddit API account") for a Reddit API account.
Then create a text file that holds the API account credentials.
The text file must be located at the following path (which is relative to ClimbingRouteBot.py):
> \\..\\..\\reddit_api_credentials.txt

The file must be in the format:
> <1> <2> <3> <4> <5>

With the passholders replaced by:
1. client ID
2. client secret
3. username
4. password
5. user agent

Example:

> LVpgepkZY8W9kb 834ts3692jIxsRQO0_qH_Vq6zeG20 YourUserName YourPassword YourUserAgent

After this is completed, execute ClimbingRouteBot.py.



</br></br>
## Results

#### Submission
![Submission Example](https://github.com/sethepeterson/climbing-route-bot/blob/master/media/SubmissionExample.PNG)

#### Comment
![Comment Example](https://github.com/sethepeterson/climbing-route-bot/blob/master/media/CommentExample.PNG)
