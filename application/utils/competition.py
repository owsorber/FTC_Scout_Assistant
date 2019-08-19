# competition.py
# a python module containing classes for different aspects of a competition


class Team():
	def __init__(self, num, name):
		self.num = num # string
		self.name = name # string
		self.matchesPlayed = 0
		self.RP = 0 # ranking points
		self.TBP = 0 # tiebreaker points
		
		self.OPR = 0
		self.autoOPR = 0
		self.teleOPR = 0
		self.endOPR = 0

	def setName(self, name):
		self.name = name

	def convertToDict(self):
		return {
			"num": self.num,
			"name": self.name,
			"matches": self.matchesPlayed,
			"RP": self.RP,
			"TBP": self.TBP,
			"OPR": self.OPR,
			"autoOPR": self.autoOPR,
			"teleOPR": self.teleOPR,
			"endOPR": self.endOPR
		}

	def getOPR(self, OPR_type):
		if OPR_type == "auto":
			return self.autoOPR
		elif OPR_type == "tele":
			return self.teleOPR
		elif OPR_type == "end":
			return self.endOPR
		return self.OPR

	def adjustedRP(self):
		if self.matchesPlayed == 0:
			return 0
		return self.RP / self.matchesPlayed

	def __str__(self):
		return "Team " + self.num + " " + self.name

class Alliance():
	def __init__(self, col, team1, team2, auto, tele, end, total):
		self.color = col
		self.team1 = team1
		self.team2 = team2

		self.auto = auto
		self.tele = tele
		self.end = end
		self.total = total

	def convertToDict(self):
		return {
			"color": self.color,
			"team1": self.team1.num,
			"team2": self.team2.num,
			"auto": self.auto,
			"tele": self.tele,
			"end": self.end,
			"total": self.total
		}

	def increaseRP(self, increment):
		self.team1.RP += increment
		self.team2.RP += increment

	def updateTBP(self, opponent_score):
		self.team1.TBP += opponent_score
		self.team2.TBP += opponent_score

	def updateMatchesPlayed(self, increase):
		self.team1.matchesPlayed += 1 if increase else -1
		self.team2.matchesPlayed += 1 if increase else -1

	def hasTeam(self, team):
		return self.team1 == team or self.team2 == team

	def __str__(self):
		return (self.color.upper() + " Alliance: " + self.team1.__str__() + 
				" and " + self.team2.__str__() + ", " + str(self.total) + " points")

class Match():
	def __init__(self, num, red, blue):
		self.num = num
		self.redAlliance = red
		self.blueAlliance = blue

	def convertToDict(self):
		return {
			"num": self.num,
			"red": self.redAlliance.convertToDict(),
			"blue": self.blueAlliance.convertToDict()
		}

	def winner(self):
		if self.redAlliance.total > self.blueAlliance.total:
			return "RED"
		elif self.blueAlliance.total > self.redAlliance.total:
			return "BLUE"
		else:
			return "TIE"

	def applyResult(self):
		r = self.winner()

		if r == "RED":
			self.redAlliance.increaseRP(2)
		elif r == "BLUE":
			self.blueAlliance.increaseRP(2)
		else:
			self.redAlliance.increaseRP(1)
			self.blueAlliance.increaseRP(1)

		self.redAlliance.updateMatchesPlayed(True)
		self.blueAlliance.updateMatchesPlayed(True)
		self.redAlliance.updateTBP(self.blueAlliance.total)
		self.blueAlliance.updateTBP(self.redAlliance.total)

	# if match gets edited
	def unapplyResult(self):
		r = self.winner()

		if r == "RED":
			self.redAlliance.increaseRP(-2)
		elif r == "BLUE":
			self.blueAlliance.increaseRP(-2)
		else:
			self.redAlliance.increaseRP(-1)
			self.blueAlliance.increaseRP(-1)

		self.redAlliance.updateMatchesPlayed(False)
		self.blueAlliance.updateMatchesPlayed(False)
		self.redAlliance.updateTBP(-self.blueAlliance.total)
		self.blueAlliance.updateTBP(-self.redAlliance.total)


	def __str__(self):
		return "Match #" + str(self.num)




