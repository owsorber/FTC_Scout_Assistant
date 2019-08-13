# data.py
# a python module for calculating team performance and ranking sorting

from application.utils.competition import *
import numpy

""" Helper functions """

# Returns a list from single column matrix, assumes all data are floats
def convertToList(singleColMat):
	li = []
	for item in singleColMat:
		li.append(round(float(item), 2))

	return li

def avg(list):
	count = 0
	for item in list:
		count += item

	return count / len(list)


""" 
PerformanceCalculator class
Defines a PerformanceCalculator that has teams (dict) and matches (list of Match objects)
as attributes and makes matrix-based performance calculations.
"""
class PerformanceCalculator:
	def __init__(self):
		self.teams = None
		self.matches = None
		self.teamBias = "6032" # for ties, prioritizes this team

	def setMatches(self, matches):
		self.matches = matches

	def setTeams(self, teams):
		self.teams = teams

	# updates the performance calculator with newest match and team data
	def update(self, teams, matches):
		self.setTeams(teams)
		self.setMatches(matches)

	# is team performance calculation possible? (at least 1 match must be entered)
	def is_valid(self):
		return len(self.matches) > 0

	# return True if all teams have played
	def all_teams_played(self):
		for team in self.teams:
			if self.teams[team].matchesPlayed == 0:
				return 0
		return 1

	# returns a tuple of length five of matrices needed for OPR calculation
	def statMatrices(self):
		M = [] # matrix to return
		Autos = []
		Teles = []
		Ends = []
		Scores = []
		
		for match in self.matches:
			r = []
			b = []
			for teamNum in self.teams:
				team = self.teams[teamNum]
				if match.redAlliance.hasTeam(team):
					r.append(1)
				else:
					r.append(0)

				if match.blueAlliance.hasTeam(team):
					b.append(1)
				else:
					b.append(0)

			M.append(r)
			M.append(b)

			Autos.append([match.redAlliance.auto])
			Autos.append([match.blueAlliance.auto])
			Teles.append([match.redAlliance.tele])
			Teles.append([match.blueAlliance.tele])
			Ends.append([match.redAlliance.end])
			Ends.append([match.blueAlliance.end])
			Scores.append([match.redAlliance.total])
			Scores.append([match.blueAlliance.total])

		return numpy.matrix(M), numpy.matrix(Autos), numpy.matrix(Teles), numpy.matrix(Ends), numpy.matrix(Scores)

	# uses numpy to find the pseudoinverse of M and multiply by results matrix to return OPR matrix
	def OPR_matrix(self, OPR_type):
		M, Autos, Teles, Ends, Scores = self.statMatrices()
		M_pseudoinverse = numpy.linalg.pinv(M)
		if OPR_type == "auto":
			return numpy.matmul(M_pseudoinverse, Autos)
		elif OPR_type == "tele":
			return numpy.matmul(M_pseudoinverse, Teles)
		elif OPR_type == "end":
			return numpy.matmul(M_pseudoinverse, Ends)
		
		return numpy.matmul(M_pseudoinverse, Scores)

	# average OPR of certain type, needed for team performance display
	def avg_OPR(self, OPR_type):
		return avg(convertToList(self.OPR_matrix(OPR_type)))

	# for displaying user OPR vs average OPR
	def vs_avg_phrase(self, OPR, OPR_type):
		if self.is_valid():
			avg = self.avg_OPR(OPR_type)
			above = OPR >= avg
			diff = abs(round(OPR - avg, 2))
			above_or_below = "above" if above else "below"

			return str(diff) + " pts " + above_or_below + " average"

		return "no match data"

	# updates OPR attributes of self.teams objects (called after match submitted)
	def applyToTeams(self):
		# grab list of each opr type
		auto_oprs = convertToList(self.OPR_matrix("auto"))
		tele_oprs = convertToList(self.OPR_matrix("tele"))
		end_oprs = convertToList(self.OPR_matrix("end"))
		oprs = convertToList(self.OPR_matrix("total"))

		# loop through teams and update their OPR properties
		teamNums = list(self.teams.keys())
		for i in range(0, len(teamNums)):
			teamNum = teamNums[i]
			self.teams[teamNum].OPR = oprs[i]
			self.teams[teamNum].autoOPR = auto_oprs[i]
			self.teams[teamNum].teleOPR = tele_oprs[i]
			self.teams[teamNum].endOPR = end_oprs[i]

	# sorts a specific list of teams by TBP
	def sortByTBP_specificTeams(self, teamNums):
		for i in range(0, len(teamNums)):
			bestTeamNum = teamNums[i]
			bestStat = self.teams[bestTeamNum].TBP
			bestIndex = i
			for j in range(i + 1, len(teamNums)):
				currTeamNum = teamNums[j]
				currStat = self.teams[currTeamNum].TBP
				if currStat > bestStat or (currStat == bestStat and currTeamNum == self.teamBias):
					bestStat = currStat
					bestTeamNum = currTeamNum
					bestIndex = j
			
			# swap
			teamNums[i], teamNums[bestIndex] = teamNums[bestIndex], teamNums[i]

		return teamNums

	# sorts all teams with a specific RP by TBP
	def sortByTBP_specificRP(self, RP):
		teamNums = list(self.teams.keys())

		for teamNum in teamNums:
			if self.teams[teamNum].RP != RP:
				teamNums.remove(teamNum)

		return self.sortByTBP_specificTeams(teamNums)

	# sorts all teams by TBP
	def sortByTBP(self):
		return self.sortByTBP_specificTeams(list(self.teams.keys()))

	# sorts all teams by RP (adjusted RP if adjusted == True)
	def sortByRP(self, adjusted):
		teamNums = list(self.teams.keys())

		for i in range(0, len(teamNums)):
			bestTeamNum = teamNums[i]
			bestStat = self.teams[bestTeamNum].RP if not adjusted else self.teams[bestTeamNum].adjustedRP()
			bestIndex = i
			for j in range(i + 1, len(teamNums)):
				currTeamNum = teamNums[j]
				currStat = self.teams[currTeamNum].RP if not adjusted else self.teams[currTeamNum].adjustedRP()
				if currStat > bestStat or (currStat == bestStat and currTeamNum == self.teamBias):
					bestStat = currStat
					bestTeamNum = currTeamNum
					bestIndex = j
			
			# swap
			teamNums[i], teamNums[bestIndex] = teamNums[bestIndex], teamNums[i]

		
		# sort by TBP among those tied
		i = 0
		while i < len(teamNums) - 1:
			currTeam = self.teams[teamNums[i]]
			equalRPs = [teamNums[i]] # list of team nums with equal RPs
			for j in range(i+1, len(teamNums)):
				nextTeam = self.teams[teamNums[j]]
				if (not adjusted and currTeam.RP == nextTeam.RP) or (adjusted and currTeam.adjustedRP() == nextTeam.adjustedRP()):
					equalRPs.append(teamNums[j])
				else:
					break

			teamNums[i:i+len(equalRPs)] = self.sortByTBP_specificTeams(equalRPs)
			i += len(equalRPs)
		
		return teamNums


	def sortByOPR(self, OPR_type):
		teamNums = list(self.teams.keys())

		for i in range(0, len(teamNums)):
			bestTeamNum = teamNums[i]
			bestStat = self.teams[bestTeamNum].getOPR(OPR_type)
			bestIndex = i
			for j in range(i + 1, len(teamNums)):
				currTeamNum = teamNums[j]
				currStat = self.teams[currTeamNum].getOPR(OPR_type)
				if currStat > bestStat or (currStat == bestStat and currTeamNum == self.teamBias):
					bestStat = currStat
					bestTeamNum = currTeamNum
					bestIndex = j
			
			# swap
			teamNums[i], teamNums[bestIndex] = teamNums[bestIndex], teamNums[i]

		return teamNums
