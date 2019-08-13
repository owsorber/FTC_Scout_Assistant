# FTC Scout Assistant
A web application developed with the Django python-based web framework by FTC Team 6032 alum, Owen Sorber.

## Accessing the Site
The most recent version of the FTC Scout Assistant is currently deployed on the PythonAnywhere web hosting service at the following web address:

https://ftcscoutassistant.pythonanywhere.com

## About
This web application is a tool built to help facilitate FTC competition scouting. After scouts input event information and match data, this system runs team performance analysis on the data, including calculation of statistics such as Offensive Power Rating (OPR) for each robot -- as well as common FTC statistics like RP and TBP -- for ranking purposes. The Scout Assistant can help let your team know how well your robot is doing throughout the competition compared to other teams, and can provide information about potential alliance partners during alliance selection. 

Disclaimer: while the FTC Scout Assistant can serve as a useful scouting aid, you are encouraged to also use other means of scouting to understand less computable details such as autonomous compatibility, robot durability/mechanisms, specific robot capabilities, etc. This application is not affiliated with or endorsed by [FIRST® Tech Challenge](https://www.firstinspires.org/robotics/ftc), and was built independently by an FTC alum of [Team 6032 Lightning Hawks](https://github.com/LightningHawks6032) using the Django python-based web framework.

###### This web application is based on my [FTC_OPR_Calculator](https://github.com/owsorber/FTC_OPR_Calculator) repository, which I originally created for the 2018-19 FTC Rover Ruckus season.

## How Robot Performance Statistics Are Calculated
The FTC Scout Assistant calculates two different types of team performance metrics for each team:

1. FTC Competition Ranking Stats
	- RP (Ranking Points)
	- TBP (Tie Breaker Points)
2. Individual Robot Performance Stats
	- Overall OPR (Offensive Power Rating)
	- Autonomous OPR
	- Tele-Op OPR
	- End-Game OPR

[What is OPR?](#what-is-opr)

Data is entered by a user into the Scout Assistant in two places: the **Event Information** page and the **Match Center**. For each team entered into the Event Information page, a Team object is created with a number and name. For each match entered into the Match Center, two Alliance objects are created (red and blue, each with data about autonomous score, tele-op score, end game score, and total score), which are combined to form a Match object. 

This process creates two main data structures:
 * teamsDict -> a dictionary mapping team numbers to their Team objects
 * matches -> a list of Match objects in chronological order

The process for keeping track of each team's RP and TBP only required updating those properties of each Team object immediately after `__init__()` of each Match object. RP was updated based on which alliance's score was higher and TBP was updated based on the opposing alliance's total.

Calculating OPR required organizing the match data into matrices to create a linear system of equations. The following matrices are created from match data:
 * M: a matrix of alliances x teams where each item represents whether or not a team is in the alliance specified by the row.
 * Autos, Teles, Ends, Scores: single-column matrices of alliances x 1 with the scores of each alliance (Scores), and specific components of the scores of each alliance (Autos, Teles, Ends).

Finding the OPRs for each robot sets up a system of equations, `Mx = S`, where `M` is the the aforementioned matrix M, `x` is a single-column matrix of teams x 1 containing the OPRs being solved for, and `S` is a single-column matrix with the scores of each alliance (either Autos, Teles, Ends, or Scores depending on the OPR type).

Since the system is overdetermined, the numpy `pinv` function is used to find the pseudoinverse of M which is multiplied with one of the scores matrices to find the OPRs. Each Team object's OPR property is then updated with its corresponding OPR from the matrix.

To see the python modules I created for match and performance data storage, visit [application/utils](https://github.com/owsorber/FTC_Scout_Assistant/tree/master/application/utils).

## What is OPR?
OPR, or Offensive Power Rating, is an attempt to uncover the average individual scoring contribution of each robot in an FTC competition. Since each match is played alliance vs alliance, with one number for the total score of the entire alliance, it can be difficult to distinguish which team carried more load or contributed more to their alliance's score. The goal of OPR is to draw together all match data to predict how much a robot can score per match. OPR can be broken down into sub-OPRs by portion of match (autonomous, tele-op, and end game). Although not a perfect statistic, as things like an alliance partner underperforming compared to their usual ability can hinder a robot's OPR, OPR can indicate some of the following things that can be difficult to detect with only raw match data:
 * High OPR can mean a robot is efficient at scoring or helps its partners score by being compatible on the match field.
 * Low OPR can mean a robot scores few points or gets in the way of its partners' scoring efforts.

Overall, while minor differences in OPR between teams can often be ignored, more significant differences may indicate the things noted above.

## TODO
 * Complete Rankings Page
 * Enable Surrogate Match Feature
 * Code cleanup
 * Styling, better UI?
