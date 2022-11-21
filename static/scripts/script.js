// functions added by Likith Venkat

function initMap() {
// Initialize and add the map
    // The location of Uluru
    const uluru = { lat: -25.344, lng: 131.031 };
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 4,
      center: uluru,
    });
    // The marker, positioned at Uluru
    const marker = new google.maps.Marker({
      position: uluru,
      map: map,
    });
  }
  
  window.initMap = initMap;

// functions added by TheNithinBalaji

function forgotpwd(){
  alert("That's Cool! But Who Asked?");
}