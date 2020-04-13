
var clickImage = document.querySelector('#image');
camera_endpoint = "http://localhost:5000/camera"
$(document).ready(function() {
    // script of index page
    $('#img-capture').on('click', getImage);
});

async function getImage(){ 
  try {
    req_data = {"action": "take_picture"}
    let response = await fetch(camera_endpoint, getRequestData(req_data, 'post'));

    let recv_res = await response.json();
    console.log("POST response is", recv_res);
    
    image_uri = camera_endpoint + "/" + recv_res
    response = await fetch(image_uri, getGetRequest())
    let recv_image = await response.blob();
    var objectURL = URL.createObjectURL(recv_image);
    clickImage.src = objectURL;
    console.log("GET response is", recv_image);
  } catch(err) {
    console.error(`Error: ${err}`);
    }

}

function getGetRequest(){
    res = {
        mode: 'no-cors',
        method: 'get',
        headers: {
            'Content-Type': 'application/json'
            },
        };
    return res
}

function getRequestData(reqeust_data, request_type){
    data =  {"camera" : req_data};
    res = {
        mode: 'no-cors',
        method: request_type,
        headers: {
            'Content-Type': 'application/json'
            },
        body: JSON.stringify(data)
        };
    return res
}
