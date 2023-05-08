function initMap() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var lat = position.coords.latitude;
      var lng = position.coords.longitude;

      var locationInfo = document.getElementById('location-info');
      locationInfo.innerHTML = "Latitude: " + lat.toFixed(6) + "<br>" + "Longitude: " + lng.toFixed(6);

      var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: lat, lng: lng},
        zoom: 14
      });
      var marker = new google.maps.Marker({
        position: {lat: lat, lng: lng},
        map: map,
        title: 'Your Location'
      });
    });
  } else {
    alert('Geolocation is not supported by your browser');
  }
}