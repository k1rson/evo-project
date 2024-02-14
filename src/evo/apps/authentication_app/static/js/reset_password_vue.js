// apps
const reset_password_app = new Vue({
    el: '#reset-password-app', 
    delimiters: ['[[', ']]'],
    data() {
        return {
            is_visible_flash_card: false, 
            is_visible_loader: false, 
            is_visible_reset_button: true, 

            flash_card_message: '',

            email: ''
        }
    },
    methods: {
        reset_password() {
            this.is_visible_flash_card = false
            const url = '/api/v1/reset-password/'

            let post_data = {
                'email': this.email
            }

            fetch(url, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': Cookies.get('csrftoken'),
                  'Authorization': ``
                },
                body: JSON.stringify(post_data),
              })
              .then(check_response)
              .then((response) => {
                if(response.status !== 'success'){
                  this.is_visible_flash_card = true

                  this.flash_card_message = response.err_msg
                }
            })
        }
    }
})