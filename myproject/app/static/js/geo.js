$(document).ready (function () {
    addOverlay();
  });
  var map = new BMapGL.Map("baiduMap");
      var point = new BMapGL.Point(103.993,30.774);
    map.centerAndZoom(point, 17);
	map.enableScrollWheelZoom(true);
   var marker = new BMapGL.Marker(new BMapGL.Point(103.993,30.774));

    function addOverlay() {
        map.addOverlay(marker);
    }
