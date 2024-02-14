function check_response(response) {
    if(response.ok){
        return response.json()
            .then(function(parsed_response){
                return Promise.resolve(parsed_response)
            });
    } else {
        return Promise.reject(response);
    }
}


// initialize all tooltips el
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))