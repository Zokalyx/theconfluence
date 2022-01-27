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
function resize2() {
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
    resize2();
    showDays();
}

/* events */
$(window).on('resize', resize);

/* Map stuff */
// Initialize and add the map
function initMap() {

    const locations = [
        { lat: 39.959, lng: -83.003 },
        { lat: 61.897, lng: 9.399 },
        { lat: 39.340, lng: -120.825 },
        { lat: 51.233, lng: 4.736 },
        { lat: 33.760, lng: -84.399 },
        { lat: 30.148, lng: -85.683 },
        { lat: -36.342, lng: -60.524 },
        { lat: 53.480, lng: -2.242 },
        { lat: 39.960, lng: -83.004 },
        { lat: 57.553, lng: -102.197 },
        { lat: 39.988, lng: -75.201 },
        { lat: -27.473, lng: 153.021 },
        { lat: 40.662, lng: -73.969 },
        { lat: 45.438, lng: 11.892 },
        { lat: 35.706, lng: -86.571 },
        { lat: 43.636, lng: -79.373 },
        { lat: -37.919, lng: 144.908 },
        { lat: 41.875, lng: -87.614 }, 
        { lat: 44.991, lng: -93.269 },
        { lat: 49.273, lng: -123.106 },
        { lat: 42.628, lng: -114.461 },
        { lat: 51.207, lng: 0.864 },
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