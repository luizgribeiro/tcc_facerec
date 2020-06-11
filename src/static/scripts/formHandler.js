
var formBtn = document.getElementById("form-btn");

formBtn.addEventListener("click", function(event) {
    event.preventDefault();

    let cadastro = {
        matricula: document.getElementById("matricula").value,
        email: document.getElementById("email").value,
        nome:  document.getElementById("nome").value,
    };
    
//TODO: Add form validation and modals (dialog)
     
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/cadastra_estudante", true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

    // send the collected data as JSON
    xhr.send(JSON.stringify(cadastro));

    xhr.onloadend = function () {
    //TODO: display modal
    //conditions: If face was detected and data captured load modal ok
    //else display modal error
    console.log(xhr)
  };


});