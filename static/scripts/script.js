image = "https://icons.iconarchive.com/icons/flaticonmaker/flat-style/48/bus-icon.png"

const locations = [
  ["Velachery", 12.9815, 80.218],
  ["KK Nagar", 13.041, 80.1994],
  ["Egmore", 13.0732, 80.2609],
  ["Koyembedu", 13.0694, 80.1948],
  ["SSN", 12.7517, 80.2033],
];

var data;
var userbusno;

async function getuserbus(){
  const response = await fetch("/busno")
  userbusno = await response.json()
}

async function getlocation(){
  const response = await fetch("/location")
  data = await response.json()
}

function initMap() {
  bus_number = document.getElementById("choice-busroute").value
  location_number = document.getElementById("choice-location").value

  console.log(data)

  var center = { lat: 13.0827, lng: 80.2707 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: center,
  });

  var marker, count;
  for (count = 0; count < data.length; count++) {
    if(data[count][0] == bus_number){
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(
          data[count][1],
          data[count][2]
        ),
        map: map,
        icon: image,
        title: data[count][0],
        animation: google.maps.Animation.DROP,
      });
    }

    if(data[count][0] == 5 - location_number){
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(
          data[count][1],
          data[count][2]
        ),
        map: map,
        title: data[count][0],
        animation: google.maps.Animation.DROP,
      });
    }
  }
}

window.initMap = initMap;

function forgotpwd() {
  prompt("To reset your password, submit your username or your email address below. If we can find you in the database, an email will be sent to your email address, with instructions how to get access again.", "");
}

function currentpos(){
  const successCallback = (position) => {
    console.log(position);
    console.log(position.coords);
    console.log(position.coords.latitude);
    console.log(position.coords.longitude);
  };

  const errorCallback = (error) => {
    console.log(error);
  };

  navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
  console.log(userbusno)
  alert("Your Location has been shared for Bus " + userbusno)

}