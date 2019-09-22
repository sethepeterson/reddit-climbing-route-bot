# Reddit Climbing Route Bot

## Summary 
A Reddit bot that identifies submissions containing pictures of rock climbing routes and publishes comments with information about the corresponding route.

#### Requirements

- Windows 10 Operating System
- Google Chrome Version 77.0.3865.90

#### Dependencies

- [PRAW](https://github.com/praw-dev/praw "GitHub") </br>
- [Selenium](https://github.com/seleniumbase/SeleniumBase "GitHub") </br>
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/ "Documentation")



</br></br>
## Results

#### Submission Title
Got the flash on Hanging Judge 11b in Clear Creek, CO

#### Generated Comment
>## [Hanging Judge](https://www.mountainproject.com/route/105752059/hanging-judge?search=1&type=route&method=resultsPage&query=Hanging%20Judge "Mountain Project")
>
>Colorado -> Golden -> Clear Creek Canyon -> Wall of Justice
>
>***
>
>Rating: 5.11b YDS
>
>Score Avg: 3.2 from 230 votes
>
>Type: Sport
>
>FA: Alan Nelson, '94
>
>Description:
>
>>Hanging Judge escapes left from the route The Great Escape. Clip two of the same bolts before heading into a long left reach to jugs and fun, thuggy moves pulling over the lip. This is a nice taste of Justice. It has good rock, good moves, and is a bit longer than Officer Friendly, but it is still a short route.
>
>Protection:
>
>>Per Jeff Welch: "5 bolts, fixed draws on all, and fixed lowering biners at the anchors above the lip."
>
>I am a bot, beep boop.
>
>[Feedback](https://np.reddit.com/message/compose?to=ClimbingRouteBot "PM's and comments are monitored! Feedback is welcome.")

Above is an example of a generated comment. 94 comments have been posted as of May 2019. Route identification accuracy on those comments is ~95%.
</br>This can definitely be improved, as well as the volume of comments posted.
Only sumbmissions with titles fitting a generic format are considered at the moment.
Broadening the scope of the format is a needed improvement, but will be difficult because Reddit's submission titles tend to be diverse.




</br></br>
## Execution
To execute the script you must [sign up](https://www.reddit.com/prefs/apps "Sign up for Reddit API account") for a Reddit API account.
Then create a text file that holds the API account credentials.
The text file must be located at the following path (which is relative to rClimbingBot.py):
> \\..\\..\\ClimbingRouteBotInfo.txt

The file must be in the format:
> <1> <2> <3> <4> <5>


</br> With the passholders replaced in this order:
1. client ID
2. client secret
3. username
4. password
5. user agent

Example:

> LVpgepkZY8W9kb 834ts3692jIxsRQO0_qH_Vq6zeG20 YourUserName YourPassword YourUserAgent

After this is completed, execute rClimbingBot.py.





</br></br>
## To Do
🗹 Refactor scraping functionality to seperate class.
</br>🗹 Redesign comment format to include a table.
</br>☐ Improve route detection accuracy.
</br>☐ Implement Yosemite Decimal System to other grading systems conversion.
</br>☐ Implement check to determine if a submission has already been considered.
