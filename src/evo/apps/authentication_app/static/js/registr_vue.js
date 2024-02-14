// apps
const reset_password_app = new Vue({
    el: '#registr-app', 
    delimiters: ['[[', ']]'],
    data() {
        return {
            is_visible_flash_card: false, 

            flash_card_message: '',
            validate_card_mesage: '', 

            username: '',
            email: '', 
            password: '', 
        }
    },
    methods: {
        check_email() {
            const url = ''

            let post_data = {
                'email': this.email
            }
        }
    }
})