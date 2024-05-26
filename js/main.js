document.addEventListener("DOMContentLoaded", function() {
    fetch('/data/locations.json')
        .then(response => response.json())
        .then(data => {
            initializeMap(data);
        });
});

function initializeMap(locations) {
    var container = document.getElementById('map');
    var options = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567),
        level: 3
    };

    var map = new kakao.maps.Map(container, options);

    locations.forEach(function(location) {
        var marker = new kakao.maps.Marker({
            position: new kakao.maps.LatLng(location.lat, location.lng),
            title: location.title
        });
        marker.setMap(map);
    });
}