
gallery_api = "http://localhost:5000/gallery"
image_api = "http://localhost:5000/camera"
$(document).ready(function() {

    fetch(gallery_api)
      .then(response => response.json())
      .then(json => {

        let data = json.slice(-50);
        data = data.map(obj => {
            console.log(obj)
            let image_uri = image_api + "/" + obj 
            return {
                image: `${image_uri}`
            };
        });

        Galleria.loadTheme('https://cdnjs.cloudflare.com/ajax/libs/galleria/1.5.7/themes/classic/galleria.classic.min.js');
        Galleria.run('.galleria', {
            dataSource: data
        });
      })

})

