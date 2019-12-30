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
			if pcalc.is_valid():
				pcalc.applyToTeams()
		else:
			data.teamsDict.clear()
			data.matches.clear()

	return render(request, "application/home.html")

def event(request):
	if request.method == "POST":
		teams_str = request.POST.get("teams")
		data.buildTeamsDict(teams_str)
	return render(request, "application/eventinfo.html")

def team(request):
	myTeamNum = "6032"
	team_data = {}

	for teamNum in data.teamsDict:
		team_obj = data.teamsDict[teamNum]
		team_data["team_" + teamNum] =  teamNum
		team_data["matches_" + teamNum] =  team_obj.matchesPlayed
		team_data["RP_" + teamNum] =  team_obj.RP
		team_data["rank_" + teamNum] =  data.rankDisplay(pcalc.sortByRP(False).index(teamNum) + 1)
		team_data["adjusted_rank_" + teamNum] =  data.rankDisplay(pcalc.sortByRP(True).index(teamNum) + 1)
		team_data["TBP_" + teamNum] =  team_obj.TBP
		team_data["tbp_rank_" + teamNum] =  data.rankDisplay(pcalc.sortByTBP().index(teamNum) + 1)
		team_data["tbp_rank_tied_" + teamNum] =  data.rankDisplay(pcalc.sortByTBP_specificRP(team_obj.RP).index(teamNum) + 1)
		team_data["OPR_" + teamNum] =  team_obj.OPR
		team_data["OPR_rank_" + teamNum] =  data.rankDisplay(pcalc.sortByOPR("total").index(teamNum) + 1)
		team_data["autoOPR_" + teamNum] =  team_obj.autoOPR
		team_data["autoOPR_rank_" + teamNum] =  data.rankDisplay(pcalc.sortByOPR("auto").index(teamNum) + 1)
		team_data["teleOPR_" + teamNum] =  team_obj.teleOPR
		team_data["teleOPR_rank_" + teamNum] =  data.rankDisplay(pcalc.sortByOPR("tele").index(teamNum) + 1)
		team_data["endOPR_" + teamNum] =  team_obj.endOPR
		team_data["endOPR_rank_" + teamNum] =  data.rankDisplay(pcalc.sortByOPR("end").index(teamNum) + 1)
		team_data["vsavg_OPR_" + teamNum] =  pcalc.vs_avg_phrase(team_obj.OPR, "total")
		team_data["vsavg_autoOPR_" + teamNum] =  pcalc.vs_avg_phrase(team_obj.autoOPR, "auto")
		team_data["vsavg_teleOPR_" + teamNum] =  pcalc.vs_avg_phrase(team_obj.teleOPR, "tele")
		team_data["vsavg_endOPR_" + teamNum] =  pcalc.vs_avg_phrase(team_obj.endOPR, "end")
		team_data["all_played_" + teamNum] =  pcalc.all_teams_played()


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
							   	int(request.POST.get("redtotal")),
							   	[not data.str_to_bool(request.POST.get("rsurrogate1")),
							   	not data.str_to_bool(request.POST.get("rsurrogate2"))])
		blueAlliance = Alliance("blue", 
							   	blue1,
							   	blue2,
							   	int(request.POST.get("blueauto")), 
							   	int(request.POST.get("bluetele")),
							   	int(request.POST.get("blueend")),
							   	int(request.POST.get("bluetotal")),
							   	[not data.str_to_bool(request.POST.get("bsurrogate1")),
							   	not data.str_to_bool(request.POST.get("bsurrogate2"))])

		data.addMatch(Match(matchNum, redAlliance, blueAlliance))

		pcalc.update(data.teamsDict, data.matches)
		pcalc.applyToTeams()


	return render(request, "application/match.html")

def rankings(request):
	rankings_data = {
		"sorted_OPR": data.jsonify_sortedTeams(pcalc.sortByOPR("total")),
		"sorted_autoOPR": data.jsonify_sortedTeams(pcalc.sortByOPR("auto")),
		"sorted_teleOPR": data.jsonify_sortedTeams(pcalc.sortByOPR("tele")),
		"sorted_endOPR": data.jsonify_sortedTeams(pcalc.sortByOPR("end")),
		"sorted_RP": data.jsonify_sortedTeams(pcalc.sortByRP(False)),
		"sorted_TBP": data.jsonify_sortedTeams(pcalc.sortByTBP())
	}

	return render(request, "application/rankings.html", rankings_data)


