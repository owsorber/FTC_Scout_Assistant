// dataconversion.js
/* A JS file for conversion between types of data representation needed throughout the website */


// Takes a DOMString (which is returned by the getItem function of localStorage)
// Returns a MATCHES array
var convertToMatches = function(domString) {
    if (domString == undefined) {
        return [];
    }
    
    var str = domString;
    var dataList = str.split(",");
    var matches = [];
    
    while (dataList.length > 0) {
        var match = [];
        for (var i = 0; i < 16; i++) {
            match.push(dataList.shift());
        }
        matches.push(match);
    }
    return matches;
}


// Given a DOMString of teams
// Returns a teams dictionary
var convertToTeamsDict = function(domString) {
    if (domString == undefined) {
        return {};
    }
    
    var teamsDOM = String(domString);
    var teamsDict = {};
    
    while (teamsDOM.length > 0) {
        // Find first comma... everything before it is the team number
        var i = 0;
        while (teamsDOM[i] != ",") {
            i += 1;
        }
        var teamNum = teamsDOM.substring(0, i);
        
        // Find second comma... everything between the first comma and second comma is the team name
        var nameStartIndex = i + 2;
        i = nameStartIndex;
        while (teamsDOM[i] != "," && i < teamsDOM.length) {
            i += 1;
        }
        var teamName = teamsDOM.substring(nameStartIndex, i);
        
        // Add to dictionary
        teamsDict[teamNum] = teamName;
        
        // Remove name from string as finished
        teamsDOM = teamsDOM.replace(teamsDOM.substring(0, i + 1), "");
        
    }
    
    return teamsDict;
}