// asset for custom map marker
image = "https://icons.iconarchive.com/icons/flaticonmaker/flat-style/48/bus-icon.png"

// const locations = [
//   ["Velachery", 12.9815, 80.218],
//   ["KK Nagar", 13.041, 80.1994],
//   ["Egmore", 13.0732, 80.2609],
//   ["Koyembedu", 13.0694, 80.1948],
// ];

const locations = {
  0: [
    [12.9815, 80.218],
    [12.8459, 80.2265],
    [12.7897, 80.2216]],

  1: [
    [12.9815, 80.218],
    [12.9249, 80.1],
    [12.823, 80.0447]],

  2: [
    [12.9048, 80.0891],
    [12.9249, 80.1],
    [12.7897, 80.2216]]
}


var data, userbusno, lat, long;

// getting bus number of currently logged in users
async function getuserbus() {
  const response = await fetch("/busno")
  userbusno = await response.json()
}

// get location of buses from mongodb 
async function getlocation() {
  const response = await fetch("/location")
  data = await response.json()
}

function initMap() {
  bus_number = document.getElementById("choice-busroute").value
  location_number = document.getElementById("choice-location").value

  var center = { lat: 12.8923, lng: 80.1889 }; // coods of Perumbakkam
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: center,
  });

  var marker, count, mapid = 0;
  for (count = 0; count < data.length; count++) {
    if (data[count][0] == bus_number) {
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(
          data[count][1],
          data[count][2]
        ),
        map: map,
        icon: image,
        title: "Bus " + String(data[count][0]),
        animation: google.maps.Animation.BOUNCE,
      });
    }

    if (count == location_number) {
      for (mapid = 0; mapid < 3; mapid++) {
        console.log(locations)
        console.log(count)
        console.log(locations[count])

        marker = new google.maps.Marker({

          position: new google.maps.LatLng(
            locations[count][mapid][0],
            locations[count][mapid][1]
          ),
          map: map,
          title: "Bus Stop" + String(mapid + 1),
          animation: google.maps.Animation.DROP,

        });
      }
    }


  }
}

window.initMap = initMap;

function forgotpwd() {
  prompt("To reset your password, submit your registration number or your email address below. If we can find you in the database, an email will be sent to your email address, with instructions how to get access again.", "");
}

async function currentpos() {
  const successCallback = (position) => {
    lat = position.coords.latitude;
    long = position.coords.longitude;

    const senddata = { busno: userbusno, lat: lat, long: long }

    fetch("/sharelocation", {
      method: "POST",
      body: JSON.stringify(senddata),
      headers: { 'Content-Type': 'application/json' }
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

function clearmap() {
  document.getElementById("choice-location").value = "none";
  document.getElementById("choice-busroute").value = "none";

  initMap()

}