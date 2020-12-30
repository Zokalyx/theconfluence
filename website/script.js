var week = 43;
var inception = 1583877600000;
var updatal = inception + week*604800000;

var now = Date.now();


var milliseconds = now - inception;
var days = Math.floor(milliseconds/(1000 * 60 * 60  * 24));

var isUpdated = days + " days since inception<br>Data is up to date";
if (now > updatal) {
    isUpdated = days + " days since inception<br>Data will be updated soon";
}

function showTime() {
    document.getElementById("timi").innerHTML = isUpdated;
    document.getElementById("time").style.marginLeft = window.innerWidth/2 - 285 + "px" ;
};