function check_response(response) {
    if (response.ok) {
        return response.json()
            .then(function(parsed_response){
                return Promise.resolve(parsed_response);
            });
    } else {
        return response.json()
            .then(function(parsed_error) {
                return Promise.reject(parsed_error); 
            });
    }
}

function call_toast(message){
    const toast_el = document.getElementById('toast-el');
    let toast_message = document.getElementById('toast-message');

    toast_message.innerText = message;

    const toast = new bootstrap.Toast(toast_el);
    toast.show();
}

// initialize all tooltips el
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})