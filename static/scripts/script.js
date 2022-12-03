// asset for custom map marker
image = "https://icons.iconarchive.com/icons/flaticonmaker/flat-style/48/bus-icon.png"

const locations = [
  ["Velachery", 12.9815, 80.218],
  ["KK Nagar", 13.041, 80.1994],
  ["Egmore", 13.0732, 80.2609],
  ["Koyembedu", 13.0694, 80.1948],
];

var data, userbusno, lat, long;

// getting bus number of currently logged in users
async function getuserbus(){
  const response = await fetch("/busno")
  userbusno = await response.json()
}

// get location of buses from mongodb 
async function getlocation(){
  const response = await fetch("/location")
  data = await response.json()
}

function initMap() {
  bus_number = document.getElementById("choice-busroute").value
  location_number = document.getElementById("choice-location").value

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
        title: "Route " + String(data[count][0]),
        animation: google.maps.Animation.BOUNCE,
      });
    }

    if(count == location_number){
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(
          locations[count][1],
          locations[count][2]
        ),
        map: map,
        title: String(locations[count][0]),
        animation: google.maps.Animation.DROP,
      });
    }
    
    
}
}

window.initMap = initMap;

function forgotpwd() {
  prompt("To reset your password, submit your username or your email address below. If we can find you in the database, an email will be sent to your email address, with instructions how to get access again.", "");
}

async function currentpos(){
  const successCallback = (position) => {
    lat = position.coords.latitude;
    long = position.coords.longitude;

    const senddata = {busno: userbusno, lat: lat, long: long}

    fetch("/sharelocation", {
      method: "POST", 
      body: JSON.stringify(senddata),
      headers: {'Content-Type': 'application/json'}
    }).then(res => {
      console.log("Request complete! response:", res);
    });

  };

  const errorCallback = (error) => {
    console.log(error);
  };

  navigator.geolocation.getCurrentPosition(successCallback, errorCallback)

  console.log(userbusno)
  alert("Your Location has been shared for Bus " + userbusno)

}