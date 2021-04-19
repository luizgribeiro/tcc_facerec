
let formBtn = document.getElementById("form-btn");

formBtn.addEventListener("click", function(event) {
    event.preventDefault();

    const cadastro = {
        matricula: document.getElementById("matricula").value,
        email: document.getElementById("email").value,
        nome:  document.getElementById("nome").value,
        foto: getImage()
    };

    console.log(cadastro);


    function getImage () {
        const canvas = document.createElement('canvas');
        const img = document.querySelector("img");
        const ctx = canvas.getContext("2d");
        ctx.canvas.height = img.height;
        ctx.canvas.width = img.width;
        ctx.drawImage(img, 0, 0);

        return canvas.toDataURL("image/jpg");
    }


    const endPoint = "http://woody:5000/student_registry"   
    //TODO: modificar para rota de API
    const options = {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
        body: JSON.stringify(cadastro)
    };

    fetch(endPoint, options)
    .then( response => {
        if (response.status === 200) return response.json()
    })
    .catch(error => console.log(error))
    .then( data => {
        if ( data.response == 'success') {
            $('#successModal').modal();  
            clearForm(); 
        } else if (data.response == 'no_faces') {
            $('#noFaceModal').modal();
        } else if ( data.response == 'multi_faces') {
            $('#multiFacesModal').modal();
        }
    })
});

function clearForm() {
    document.getElementById('matricula').value = "";
    document.getElementById('email').value = "";
    document.getElementById('nome').value = "";
}