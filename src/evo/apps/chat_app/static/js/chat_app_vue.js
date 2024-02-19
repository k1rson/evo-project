// apps
const left_bar_app = new Vue({
    el: '#left-bar-app',
    delimiters: ['[[', ']]'],
    data() {
        return {
            chat_rooms: [],
        }
    },
    beforeMount() {
        this.get_all_user_chat_rooms();
    },
    methods: {
        get_all_user_chat_rooms(){
            const url = `/api/v1/chat-room-api/chat-rooms`
            fetch(url, {
                method: 'GET',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Token ${Cookies.get('token')}`
                },
              })
              .then(check_response)
              .then((response) => {
                if(response.status !== 'success'){
                    console.log(response.err_msg)
                    return
                }
                this.chat_rooms = response.chat_rooms
            })
        }
    }
})