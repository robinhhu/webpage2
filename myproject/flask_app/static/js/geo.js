if (typeof(Storage) !== "undefined") {
  // Code for localStorage/sessionStorage.
} else {
  window.alter("Local storage is not supported");
}

navigator.geolocation.getCurrentPosition(storePosition);
function storePosition(position) {
  localStorage.setItem("longitude", position.coords.longitude);
  localStorage.setItem("latitude", position.coords.latitude);
}


$(document).ready (function () {
    addOverlay();
    });
    longitude=localStorage.getItem("longitude");
    latitude=localStorage.getItem("latitude")
    var map = new BMapGL.Map("baiduMap");
    var point = new BMapGL.Point(longitude,latitude);
    map.centerAndZoom(point, 17);
    map.enableScrollWheelZoom(true);
    var marker = new BMapGL.Marker(new BMapGL.Point(longitude,latitude));

    function addOverlay() {
        map.addOverlay(marker);
    }



