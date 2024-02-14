// apps
const auth_app = new Vue({
    el: '#auth-app',
    delimiters: ['[[', ']]'],
    data() {
        return {
            is_visible_flash_card: false, 
            is_visible_loader: false,
            is_visible_auth_button: true,

            flash_card_message: '', 

            username: '', 
            password: ''
        }
    },
    methods: {
      auth_user() {
        const url = '/api/v1/auth-user-token/'
        this.is_visible_loader = true
        this.is_visible_auth_button = false
        this.is_visible_flash_card = false

        let post_data = {
          'username': this.username, 
          'password': this.password
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
            this.is_visible_auth_button = true
            this.is_visible_loader = false

            this.flash_card_message = response.err_msg
            return
          }
          Cookies.set('token', response.token)
          window.location.href = '/'
        })
      }
    }
})