//footer.js
/* Script for the year in the copyright footer on every page */

var startingYear = 2019; //gather the starting year of work featured in website
var year = new Date().getFullYear(); //get the current year
var footerYear = document.getElementById("footer-date"); //access "footer-date" id in html file

if (year == startingYear) {
    footerYear.innerHTML = startingYear;
} else {
    footerYear.innerHTML = startingYear + "-" + year;
}