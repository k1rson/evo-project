// apps
const reset_password_app = new Vue({
    el: '#reset-password-app', 
    delimiters: ['[[', ']]'],
    data() {
        return {
            show_flash_card: false, 
            show_span_loader: false, 
            show_reset_button: true, 

            flash_card_message: '',
            email: ''
        }
    },
    methods: {
        reset_password() {
            const url = '/api/v1/auth-api/reset-password/';
            
            this.show_loader();
            
            let res_val = this.validate_email(this.email);
            if(!res_val){
              return; 
            }

            let post_data = {
              'email': this.email
            }

            fetch(url, {
                method: 'POST', 
                headers: {
                  'Content-Type': 'application/json', 
                  'Accept': 'application/json', 
                  'Cookie': `csrf_token=${Cookies.get('csrf_token')}`
                },
                body: JSON.stringify(post_data),
              })
              .then(check_response)
              .then(response => {
                if(response.success){
                  console.log('good')
                }
                else{
                  this.show_error(response.err_msg);
                }
              })
              .catch(error => {
                console.error(error)
            })
        }, 
        show_loader(){
            this.show_span_loader = true;
            this.show_reset_button = false;
            this.show_flash_card = false;
        },
        show_error(err_msg){
            this.flash_card_message = err_msg;

            this.show_span_loader = false;
            this.show_reset_button = true;
            this.show_flash_card = true;
        }, 
        validate_email(email){
          if(!email){
            this.show_error('Поле email не может быть пустым');
            return false;
          }

          const email_pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!email_pattern.test(email)) {
              this.show_error('Некорректный формат email');
              return false;
          }

          return true; 
        }
    }
})