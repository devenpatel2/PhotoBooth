
//const btn = document.getElementById('click-camera');
var myImage = document.querySelector('#image');
//btn.addEventListener('click', async _ => {
const navbar = document.getElementById('click-camera');
navbar.addEventListener('click', async _ => { 
  try {
    const response = await fetch('http://192.168.0.153:5000/camera', getPostData());


    let data = await response.blob();
    var objectURL = URL.createObjectURL(data);
    myImage.src = objectURL;

    console.log("Response is", data);
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
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
            },
        body: JSON.stringify(data)
        };
    return res
}
