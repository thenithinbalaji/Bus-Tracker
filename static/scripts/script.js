// asset for custom map marker
image = "https://icons.iconarchive.com/icons/flaticonmaker/flat-style/48/bus-icon.png"

var livelocationdata, userbusno, lat, long, stoppingsdata;

// getting bus number of currently logged in user
async function getuserbus() {
  const response = await fetch("/busno")
  userbusno = await response.json()
}

// get live locations of buses from mongodb 
async function getlocation() {
  const response = await fetch("/location")
  livelocationdata = await response.json()
}

// get route stoppings from mongodb 
async function getstoppings() {
  const response = await fetch("/stoppings")
  stoppingsdata = await response.json()
  // console.log(locations)
}

function initMap() {
  bus_number = document.getElementById("choice-busroute").value

  var center = { lat: 12.8923, lng: 80.1889 }; // coods of Perumbakkam
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: center,
  });

  marker = new google.maps.Marker({
    position: new google.maps.LatLng(
      livelocationdata[bus_number][0],
      livelocationdata[bus_number][1]
    ),
    map: map,
    icon: image,
    title: "Bus " + String(bus_number),
    animation: google.maps.Animation.BOUNCE,
  });


  for (let count = 0; count < stoppingsdata[bus_number].length; count++) {

    marker = new google.maps.Marker({

      position: new google.maps.LatLng(
        stoppingsdata[bus_number][count][0],
        stoppingsdata[bus_number][count][1]
      ),
      map: map,
      title: "Bus Stop " + String(count + 1),
      animation: google.maps.Animation.DROP,

    });
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
  alert("Your Location has been shared for Bus " + userbusno + ". Reload the page to see changes")

}

function clearmap() {
  document.getElementById("choice-busroute").value = "none";
  initMap()
}