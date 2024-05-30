let currentPage = 1;
const pageSize = 100;
let currentType = null;

document.addEventListener("DOMContentLoaded", function() {
    var map = new kakao.maps.Map(document.getElementById('map'), {
        center: new kakao.maps.LatLng(37.4966645, 127.0629804),
        level: 7
    });

    var clusterer = new kakao.maps.MarkerClusterer({
        map: map,
        averageCenter: true,
        minLevel: 5,
        disableClickZoom: true
    });

    function loadMarkers(page, type) {
        let url = `/locations?page=${page}&pageSize=${pageSize}`;
        if (type) {
            url += `&type=${type}`;
        }
        fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log(data); // 데이터 확인용
                var markers = data.map(function(location) {
                    var marker = new kakao.maps.Marker({
                        position: new kakao.maps.LatLng(location.lat, location.lng),
                        title: location.atclNm || location.road_address
                    });

                    var infowindow = new kakao.maps.InfoWindow({
                        content: `<div style="padding:5px;">${location.atclNm || location.road_address}</div>`
                    });

                    kakao.maps.event.addListener(marker, 'mouseover', function() {
                        infowindow.open(map, marker);
                    });

                    kakao.maps.event.addListener(marker, 'mouseout', function() {
                        infowindow.close();
                    });

                    kakao.maps.event.addListener(marker, 'click', function() {
                        showInfo(location);
                    });

                    return marker;
                });

                clusterer.clear(); // 기존 마커 제거
                clusterer.addMarkers(markers); // 새로운 마커 추가
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    function showInfo(location) {
        var infoDiv = document.getElementById('info');
        infoDiv.innerHTML = `
            <h2>${location.atclNm}</h2>
            <p>유형: ${location.rletTpNm}</p>
            <p>가격: ${location.prc}</p>
            <p>주소: ${location.address}</p>
            <p>도로명 주소: ${location.road_address}</p>
            <p>위도: ${location.lat}</p>
            <p>경도: ${location.lng}</p>
        `;
    }

    loadMarkers(currentPage, currentType);

    document.getElementById('nextPage').addEventListener('click', function() {
        currentPage++;
        loadMarkers(currentPage, currentType);
    });

    document.getElementById('prevPage').addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            loadMarkers(currentPage, currentType);
        }
    });

    document.getElementById('showApartments').addEventListener('click', function() {
        currentType = "아파트"; // 아파트 유형
        currentPage = 1; // 페이지 초기화
        loadMarkers(currentPage, currentType);
    });

    document.getElementById('showOfficetels').addEventListener('click', function() {
        currentType = "오피스텔"; // 오피스텔 유형
        currentPage = 1; // 페이지 초기화
        loadMarkers(currentPage, currentType);
    });
    document.getElementById('showOffice').addEventListener('click', function() {
        currentType = "사무실"; 
        currentPage = 1; 
        loadMarkers(currentPage, currentType);
    });
    document.getElementById('showMarket').addEventListener('click', function() {
        currentType = "상가"; 
        currentPage = 1; 
        loadMarkers(currentPage, currentType);
    });
    document.getElementById('showElse').addEventListener('click', function() {
        currentType = "건물,단독/다가구,재건축,원룸,상가주택,토지"; 
        currentPage = 1; 
        loadMarkers(currentPage, currentType);
    });

    kakao.maps.event.addListener(clusterer, 'clusterclick', function(cluster) {
        var level = map.getLevel() - 1;
        map.setLevel(level, { anchor: cluster.getCenter() });
    });
});