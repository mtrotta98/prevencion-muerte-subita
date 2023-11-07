var map;  
var markers = [];
const LaPlata = {
    north: -34.81936536255149, //-34.81936536255149, -57.96880667574618
    south: -35.02991601497499, //-35.02991601497499, -57.950256047701615
    west: -58.14412828713677, //-34.95720890319979, -58.14412828713677
    east: -57.80657962260428, //-34.94260009885324, -57.80657962260428
  };

function initMap() {
    // create the maps
    var lat_lng = {lat: -34.921370606389594, lng: -57.95480962673844}; 
    var prueba = {lat: -34.92149, lng: -57.95809}

    map = new google.maps.Map(document.getElementById('map'), {  
        zoom: 15,
        center: lat_lng,
        restriction: {
            latLngBounds: LaPlata,
            strictBounds: false,
        } , 
        mapTypeId: google.maps.MapTypeId.TERRAIN
    }); 
    addMarker(prueba)
}

function addMarker(location) {
    var marker = new google.maps.Marker({  
      position: location,  
      map: map,
    });
    var information = new google.maps.InfoWindow({
      content: "<h4>Espacio obligado: Plaza Moreno</h4><br><p>Cantidad de deas " + 24 + "</p><br><p>DEA solidario: Si</p>"
    });
    marker.addListener("click", function() {
      information.open(map, marker)
    });
    markers.push(marker); 
}

function deleteMarkers(){
    hideMarkers();
    markers = [];
  }

function hideMarkers(){
    setMapOnAll(null);
}

function setMapOnAll(map) {
    for (let i = 0; i < markers.length; i++) {
      markers[i].setMap(map);
    }
  }