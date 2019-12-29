# data.py
# a python module storing data collected from the Scout Assistant app

from application.utils.competition import *
import json

teamsDict = {} # to map team nums (String) to Team objects
matches = [] # list of Match objects


# builds teamsDict from a string of teams
def buildTeamsDict(str):
	teamsList = str.split("\n")
	print(teamsList)
	prevTeamsDict = teamsDict # temp storage
	teamsDict.clear() # empty up teamsDict
	
	for team_str in teamsList:
		if team_str != "":
			num, name = team_str.split(", ")
			if name[len(name) - 2:] == "\r":
				name = name[0:len(name) - 1] # gets rid of \r
			
			if num in prevTeamsDict:
				# team previously existed, only change name if needed
				teamsDict[num] = prevTeamsDict[num]
				teamsDict[num].setName(name) # if name different
			else:
				# team never existed, so we instantiate new team
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

def clearTeamsDict():
	teamsDict.clear()

def updateFromLocalStorage(teamsDOM, matchesDOM):
	# setup teams
	clearTeamsDict()
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
		red = Alliance("red", red1, red2, int(matchData[2]), int(matchData[3]), int(matchData[4]), int(matchData[5]), [not bool(matchData[12]), not bool(matchData[13])])
		blue = Alliance("blue", blue1, blue2, int(matchData[8]), int(matchData[9]), int(matchData[10]), int(matchData[11]), [not bool(matchData[14]), not bool(matchData[15])])
		addMatch(Match(matchNum, red, blue))

# takes in a sortedList of team numbers, puts team objects into list and converts to json
def jsonify_sortedTeams(sortedList):
	teams = [] # a list of team dictionaries (later to be converted to json)
	for team in sortedList:
		teams.append(teamsDict[team].convertToDict()) # converts each team into dictionary (needed for json.dumps())

	return json.dumps(teams)


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

def str_to_bool(str):
	return True if str == "true" else False

def rankDisplay(num):
	return str(num) + ordinalNumSuffix(num)

# for debugging
def displayTeamStats():
	for teamnum in teamsDict:
		team = teamsDict[teamnum]
		print(team.__str__(), "-->", "RP =", team.RP, "and TBP =", team.TBP)


