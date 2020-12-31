if (typeof(Storage) !== "undefined") {
  // Code for localStorage/sessionStorage.
} else {
  window.alter("Local storage is not supported");
}

//geolocation get the current user location and stored in local storage
navigator.geolocation.getCurrentPosition(storePosition);
function storePosition(position) {
  localStorage.setItem("longitude", position.coords.longitude);
  localStorage.setItem("latitude", position.coords.latitude);
}


$(document).ready (function () {
    addOverlay();
});
    //Baidu Map
    //set the center position, marker and scale
    longitude=localStorage.getItem("longitude");
    latitude=localStorage.getItem("latitude")
    var map = new BMapGL.Map("baiduMap");
    var point = new BMapGL.Point(longitude,latitude);
    map.centerAndZoom(point, 17);
    map.enableScrollWheelZoom(true);
    var marker = new BMapGL.Marker(new BMapGL.Point(longitude,latitude));

    //add marker to the map
    function addOverlay() {
        map.addOverlay(marker);
    }



