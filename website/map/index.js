// Initialize and add the map
function initMap() {

  // Anonymous!!
  const locations = [
    { lat: -25.344, lng: 131.036 },
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