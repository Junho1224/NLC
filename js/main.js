// main.js
// document.addEventListener("DOMContentLoaded", function() {
//     fetch('/locations')
//         .then(response => response.json())
//         .then(data => {
//             initializeMap(data);
//         });
// });

// function initializeMap(locations) {
//     var container = document.getElementById('map');
//     var options = {
//         center: new kakao.maps.LatLng(37.4966645, 127.0629804),
//         level: 7
//     };

//     var map = new kakao.maps.Map(container, options);

//     locations.forEach(function(location) {
//         var marker = new kakao.maps.Marker({
//             position: new kakao.maps.LatLng(location.lat, location.lng),
//             title: location.atclNm || location.road_address
//         });
//         marker.setMap(map);
//     });
// }


document.addEventListener("DOMContentLoaded", function() {
    // 지도를 표시할 div와 초기 설정
    var map = new kakao.maps.Map(document.getElementById('map'), {
        center: new kakao.maps.LatLng(37.4966645, 127.0629804),
        level: 7
    });

    // 마커 클러스터러 생성
    var clusterer = new kakao.maps.MarkerClusterer({
        map: map,
        averageCenter: true,
        minLevel: 5,
        disableClickZoom: true
    });

    // 데이터를 가져와 마커를 생성하고 클러스터러에 추가
    fetch('/locations')
        .then(response => response.json())
        .then(data => {
            console.log(data); // 데이터 확인용
            var markers = data.map(function(location) {
                return new kakao.maps.Marker({
                    position: new kakao.maps.LatLng(location.lat, location.lng),
                    title: location.atclNm || location.road_address
                });
            });

            // 클러스터러에 마커 추가
            clusterer.addMarkers(markers);
        })
        .catch(error => console.error('Error fetching data:', error));

    // 클러스터 마커 클릭 이벤트 등록
    kakao.maps.event.addListener(clusterer, 'clusterclick', function(cluster) {
        var level = map.getLevel() - 1;
        map.setLevel(level, { anchor: cluster.getCenter() });
    });
});