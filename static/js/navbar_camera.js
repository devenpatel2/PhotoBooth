
var myImage = document.querySelector('#image');
const navbar = document.getElementById('click-camera');
navbar.addEventListener('click', async _ => { 
  try {
    const response = await fetch("http://localhost:5000/camera", getPostData());

    let recv_res = await response.blob();
    var objectURL = URL.createObjectURL(recv_res);
    myImage.src = objectURL;

    console.log("Response is", recv_res);
  } catch(err) {
    console.error(`Error: ${err}`);
    }
});

function getPostData(){
    data =  {"camera" :{
                "action": "take_picture"
            }
        };
    res = {
        mode: 'no-cors',
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
            },
        body: JSON.stringify(data)
        };
    return res
}
