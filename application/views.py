from django.shortcuts import render, HttpResponse
from application.utils.competition import *
import application.utils.data as data
import application.utils.robot_performance as performance

pcalc = performance.PerformanceCalculator()

# Create your views here.

def home(request):
	if request.method == "POST":
		if request.POST.get("name") == "stored":
			data.updateFromLocalStorage(request.POST.get("teams"), request.POST.get("matches"))
			
			print(data.teamsDict)
			print(data.matches)

			pcalc.update(data.teamsDict, data.matches)
			pcalc.applyToTeams()
		else:
			data.teamsDict = {}
			data.matches = []

	return render(request, "application/home.html")

def event(request):
	if request.method == "POST":
		teams_str = request.POST.get("teams")
		data.buildTeamsDict(teams_str)
	return render(request, "application/eventinfo.html")

def team(request):
	myTeamNum = "6032"
	print(data.teamsDict)
	if myTeamNum in data.teamsDict:
		myTeam = data.teamsDict[myTeamNum]
		team_data = {
			"team": myTeamNum,

			"matches": myTeam.matchesPlayed,
			"RP": myTeam.RP,
			"rank": data.rankDisplay(pcalc.sortByRP(False).index(myTeamNum) + 1),
			"adjusted_rank": data.rankDisplay(pcalc.sortByRP(True).index(myTeamNum) + 1),
			"TBP": myTeam.TBP,
			"tbp_rank": data.rankDisplay(pcalc.sortByTBP().index(myTeamNum) + 1),
			"tbp_rank_tied": data.rankDisplay(pcalc.sortByTBP_specificRP(myTeam.RP).index(myTeamNum) + 1),
			
			"OPR": myTeam.OPR,
			"OPR_rank": data.rankDisplay(pcalc.sortByOPR("total").index(myTeamNum) + 1),
			"autoOPR": myTeam.autoOPR,
			"autoOPR_rank": data.rankDisplay(pcalc.sortByOPR("auto").index(myTeamNum) + 1),
			"teleOPR": myTeam.teleOPR,
			"teleOPR_rank": data.rankDisplay(pcalc.sortByOPR("tele").index(myTeamNum) + 1),
			"endOPR": myTeam.endOPR,
			"endOPR_rank": data.rankDisplay(pcalc.sortByOPR("end").index(myTeamNum) + 1),
			
			"vsavg_OPR": pcalc.vs_avg_phrase(myTeam.OPR, "total"),
			"vsavg_autoOPR": pcalc.vs_avg_phrase(myTeam.autoOPR, "auto"),
			"vsavg_teleOPR": pcalc.vs_avg_phrase(myTeam.teleOPR, "tele"),
			"vsavg_endOPR": pcalc.vs_avg_phrase(myTeam.endOPR, "end"),

			"all_played": pcalc.all_teams_played()
		}
	else:
		team_data = {"team": myTeamNum, "matches": 0, "all_played": 0}

	print(team_data)
	return render(request, "application/team.html", team_data)

def matchCenter(request):
	if request.method == "POST":
		matchNum = int(request.POST.get("num"))
		red1 = data.teamsDict[request.POST.get("red1")]
		red2 = data.teamsDict[request.POST.get("red2")]
		blue1 = data.teamsDict[request.POST.get("blue1")]
		blue2 = data.teamsDict[request.POST.get("blue2")]
		
		redAlliance = Alliance("red",
								red1, 
								red2, 
							   	int(request.POST.get("redauto")), 
							   	int(request.POST.get("redtele")),
							   	int(request.POST.get("redend")),
							   	int(request.POST.get("redtotal")))
		blueAlliance = Alliance("blue", 
							   	blue1,
							   	blue2, 
							   	int(request.POST.get("blueauto")), 
							   	int(request.POST.get("bluetele")),
							   	int(request.POST.get("blueend")),
							   	int(request.POST.get("bluetotal")))

		data.addMatch(Match(matchNum, redAlliance, blueAlliance))

		pcalc.update(data.teamsDict, data.matches)
		pcalc.applyToTeams()

		for team_num in pcalc.sortByTBP():
			team = data.teamsDict[team_num]
			print(team.__str__() + ": " + str(team.RP) + ", " + str(team.TBP))


	return render(request, "application/match.html")

def rankings(request):
	return render(request, "application/rankings.html")


