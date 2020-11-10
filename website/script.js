var week = 36;
var inception = "2020-03-10T00:00:00Z";

var now = new Date();
var inceptionTime = (new Date(inception)).getTime();
var nowTime = now.getTime();

var milliseconds = Math.abs(inceptionTime - nowTime);
var days = Math.floor(milliseconds/(1000 * 60 * 60  * 24));

var actualweek = Math.ceil((days+2)/7);

var isUpdated = days + " days since inception<br>Data will be updated soon";
if (week == actualweek) {
    isUpdated = days + " days since inception<br>Data is up to date";
}

function showTime() {
    document.getElementById("timi").innerHTML = isUpdated;
    document.getElementById("time").style.marginLeft = window.innerWidth/2 - 285 + "px" ;
};