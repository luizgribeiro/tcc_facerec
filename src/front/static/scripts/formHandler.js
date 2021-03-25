
let formBtn = document.getElementById("form-btn");

formBtn.addEventListener("click", function(event) {
    event.preventDefault();

    let cadastro = {
        matricula: document.getElementById("matricula").value,
        email: document.getElementById("email").value,
        nome:  document.getElementById("nome").value,
    };

     
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/cadastra_estudante", true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

    // send the collected data as JSON
    xhr.send(JSON.stringify(cadastro));

    xhr.onloadend = function () {
        
        if (xhr.responseText == 'success') {
            $('#successModal').modal();  
            clearForm(); 
        } else if (xhr.responseText == 'no_faces') {
            $('#noFaceModal').modal();
        } else if (xhr.responseText == 'multi_faces') {
            $('#multiFacesModal').modal();
        }
    };

});

function clearForm() {
    document.getElementById('matricula').value = "";
    document.getElementById('email').value = "";
    document.getElementById('nome').value = "";
}