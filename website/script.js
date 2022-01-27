let week = 99;
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

/* adjust logo image for map site (annoying...) */
function resize() {
    if ($(window).width() < $(window).height()) {
        $("#home2").attr("src", "../images/mobilelogo.png");
        $("#github2").css("display", "none");
    } else {
        $("#home2").attr("src", "../images/logo.png");
        $("#github2").css("display", "block");
    }
}

/* load all functions */
function loaded() {
    resize();
    showDays();
}

/* events */
$(window).on('resize', resize);

/* Map stuff */
// Initialize and add the map
function initMap() {

    const locations = [
        { lat: 33.760, lng: -84.399 },
        { lat: -36.342, lng: -60.524 },
        { lat: 53.480, lng: -2.242 },
        { lat: 42.628, lng: -114.461 },
    ];
  
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 1,
      center: { lat: 0, lng: 0 },
    });
  
    locations.forEach(location => {
        new google.maps.Marker({
          position: location,
          map: map,
        })
    });
  }