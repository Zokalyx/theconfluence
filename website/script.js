let week = 57;
let inception = 1583877600000;
let updated = inception + week*604800000;
let now = Date.now();
let millis = now - inception;
let days = Math.floor(millis/(1000 * 60 * 60  * 24)) + 1;

let daysText = days + " days since inception<br>";
daysText += (now > updated) ? "Data will be updated soon" : "Data is up to date";

/* function to show days */
function showDays() {
    $("#days").html(daysText);
}

/* adjust logo image */
function resize() {
    if ($(window).width() < $(window).height()) {
        $("#home").attr("src", "website/images/mobilelogo.png");
        $("#github").css("display", "none");
    } else {
        $("#home").attr("src", "website/images/logo.png");
        $("#github").css("display", "block");
    }
}

/* load all functions */
function loaded() {
    resize();
    showDays();
}

/* events */
$(window).on('resize', resize);