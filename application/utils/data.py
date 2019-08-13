# data.py
# a python module storing data collected from the Scout Assistant app

from application.utils.competition import *
import json

teamsDict = {} # to map team nums (String) to Team objects
matches = [] # list of Match objects


# builds teamsDict from a string of teams
def buildTeamsDict(str):
	teamsList = str.split("\n")
	
	for team_str in teamsList:
		if team_str != "":
			num, name = team_str.split(", ")
			name = name[0:len(name) - 1] # gets rid of \r
			teamsDict[num] = Team(num, name)

def addMatch(match):
	if match.num > len(matches):
		matches.append(match) # add
		match.applyResult()
	else:
		matches[match.num - 1].unapplyResult()
		matches[match.num - 1] = match # replace
		match.applyResult()

def addTeam(num, obj):
	teamsDict[num] = obj

def updateFromLocalStorage(teamsDOM, matchesDOM):
	# setup teams
	teams = json.loads(teamsDOM)
	for teamNum in teams:
		addTeam(teamNum, Team(teamNum, teams[teamNum]))

	# setup matches
	matchesList = json.loads(matchesDOM)
	for i in range(0, len(matchesList)):
		matchNum = i + 1
		matchData = matchesList[i]

		red1 = teamsDict[matchData[0]]
		red2 = teamsDict[matchData[1]]
		blue1 = teamsDict[matchData[6]]
		blue2 = teamsDict[matchData[7]]
		red = Alliance("red", red1, red2, int(matchData[2]), int(matchData[3]), int(matchData[4]), int(matchData[5]))
		blue = Alliance("blue", blue1, blue2, int(matchData[8]), int(matchData[9]), int(matchData[10]), int(matchData[11]))
		addMatch(Match(matchNum, red, blue))



# Returns the two letters at the end of an ordinal number (e.g. 'st' for 1 because 1st)
# -> used for rank display
def ordinalNumSuffix(number):
	if number % 10 == 1 and number != 11:
   		return "st"
	elif number % 10 == 2 and number != 12:
   		return "nd"
	elif number % 10 == 3 and number != 13:
   		return "rd"      
	return "th"

def rankDisplay(num):
	return str(num) + ordinalNumSuffix(num)

# for debugging
def displayTeamStats():
	for teamnum in teamsDict:
		team = teamsDict[teamnum]
		print(team.__str__(), "-->", "RP =", team.RP, "and TBP =", team.TBP)


