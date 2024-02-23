// apps
const left_bar_app = new Vue({
    el: '#left-bar-app',
    delimiters: ['[[', ']]'],
    data() {
        return {
            user_chat_rooms: [],
            shared_chat_rooms: [],
            searched_users: [],
            invited_users_ids: [],

            query: '',
            flash_card_message: '',

            chat_room_name: '',
            chat_room_avatar: undefined,

            show_empty_user_chat_rooms: false,
            show_empty_shared_chat_rooms: false,

            show_creation_card: false, 
            show_flash_card: false,

            is_valid_room_name_input: false,
            is_valid_room_avatar_input: false,
        }
    },
    beforeMount() {
        this.get_user_chat_rooms();
        this.get_shared_chat_rooms();
    },
    methods: {
        // functions for fething chat rooms
        fetch_chat_rooms(url, callback){
            fetch(url, {
                method: 'GET', 
                headers: this.get_request_headers()
                })
                .then(check_response)
                .then(response => callback(response))
                .catch(error => {
                    call_toast(`Ошибка сервера: ${error.detail} Пожалуйста, попробуйте перезайти в аккаунт, или же обратитесь к системному администратору`);
                })
        },
        get_request_headers(content_type){
            return {
                'Content-Type': 'application/json', 
                'Accept': 'application/json', 
                'Authorization': `Token ${Cookies.get('token')}`,
                'Cookie': `csrf_token=${Cookies.get('csrf_token')}`
            }
        },
        get_user_chat_rooms(){
            const url = `/api/v1/chat-room-api/user-chat-rooms`;
            this.fetch_chat_rooms(url, response => {
                if(!response.user_chat_rooms){
                    this.show_empty_user_chat_rooms = true; 
                    return; 
                }
                
                this.show_empty_user_chat_rooms = false;
                this.user_chat_rooms = response.user_chat_rooms;
            });
        },
        get_shared_chat_rooms(){
            const url = `/api/v1/chat-room-api/shared-chat-rooms`;
            this.fetch_chat_rooms(url, response => {
                let chat_rooms = response.shared_chat_rooms
                if(!chat_rooms){
                    this.show_empty_shared_chat_rooms = true; 
                    return; 
                }

                this.shared_chat_rooms = response.shared_chat_rooms;
            });
        },

        // functions for searching and inviting users to chat room
        search_user() {
            const url = `/api/v1/chat-room-api/search-target-user/?query=${this.query}`;

            fetch(url, {
                method: 'GET', 
                headers: this.get_request_headers()
            })
            .then(check_response)
            .then(response => {
                this.searched_users = [];
                this.show_flash_card = false; 

                if(!response.success){
                    this.show_user_not_found_message(response.err_msg);
                    return;
                }

                // добавляем свойство invited к каждому пользователю в массиве searched_users
                this.searched_users = response.searched_users.map(user => ({
                    ...user,
                    invited: this.invited_users_ids.includes(user.pk)
                }));
            })
            .catch(error => {
                call_toast(`Ошибка сервера: ${error.detail} Пожалуйста, перезайдите в аккаунт`);
            });
        },
        show_user_not_found_message(message){
            this.show_flash_card = true; 
            this.flash_card_message = message;
        },
        invite_user_to_chat(user_id) {
            this.invited_users_ids.push(user_id);
        },
        show_user_details(user_id){
            console.log(`show: ${user_id}`)
        }, 
        
        // functions for create chat room
        close_creation_chat_card(){
            // сбор ненужных данных при закрытии окна создания чата
            this.excluded_users_id = [];
            this.searched_users = [];
            this.invited_users_ids = [];
            this.query = '';

            this.show_creation_card = false;
        }, 
        validate_room_name(){
            if (this.chat_room_name.length < 4) {
                this.is_valid_room_name_input = false; 
                return; 
            }
            this.is_valid_room_name_input = true;
        },
        validate_room_avatar(){
            const allowed_image_types = ['image/jpeg', 'image/webp', 'image/png'];
            const file = this.chat_room_avatar;

            if(!allowed_image_types.includes(file.type)){
                this.is_valid_room_avatar_input = false; 
                return;
            }

            this.is_valid_room_avatar_input = true; 
        },
        handle_input_avatar(event){
            this.chat_room_avatar = event.target.files[0];
            this.validate_room_avatar();
        },
        create_chat_room(){
            const url = `/api/v1/chat-room-api/chat-room-actions`;

            let post_data = new FormData(); 
            post_data.append('room_name', this.chat_room_name);
            post_data.append('room_avatar', this.chat_room_avatar);

            fetch(url, {
                method: 'POST', 
                headers: {
                    'Accept': 'application/json', 
                    'Authorization': `Token ${Cookies.get('token')}`,
                    'Cookie': `csrf_token=${Cookies.get('csrf_token')}`
                }, 
                body: post_data
            })
            .then(check_response)
            .then(() => {
                this.close_creation_chat_card();
                this.get_user_chat_rooms(); 
            })
            .catch(error => {
                call_toast(`Ошибка сервера: ${error.detail} Пожалуйста, перезайдите в аккаунт`);
            });
        }
    }
})