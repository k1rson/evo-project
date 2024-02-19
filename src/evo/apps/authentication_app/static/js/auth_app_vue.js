// apps
const auth_app = new Vue({
    el: '#auth-app',
    delimiters: ['[[', ']]'],
    data() {
        return {
            show_flash_card: false, 
            show_span_loader: false,
            show_auth_button: true,

            flash_card_message: '', 
            username: '', 
            password: ''
        }
    },
    methods: {
      auth_user(){
        const url = '/api/v1/auth-api/auth-user-token/';

        this.show_loader();
        
        let res_val = this.validate_fields(this.username, this.password);
        if(!res_val){
          this.show_error('Поле логин/пароль не может быть пустым');
          return;
        }

        let post_data = {
          'username': this.username, 
          'password': this.password
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
            Cookies.set('token', response.token)
            window.location.href = '/'
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
        this.show_auth_button = false;
        this.show_flash_card = false;

        console.log('show_loa')
      }, 
      show_error(err_msg){
        this.flash_card_message = err_msg;

        this.show_auth_button = true; 
        this.show_flash_card = true; 
        this.show_span_loader = false;
      },
      validate_fields(username, password){
        if(!username || !password){
          return false;
        }

        return true;
      }
    }
})