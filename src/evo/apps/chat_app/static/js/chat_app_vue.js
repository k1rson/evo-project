// apps 
const tooltip_actions_app = new Vue({
    el: '#tooltip-actions-app',
    delimiters: ['[[', ']]'],
    data() {
        return {
            chat_room_name: '',
            chat_room_avatar_base64 : '',

            searched_users: [],
            invited_users_ids: [],

            query: '',
            flash_card_message: '',

            is_valid_room_name_input: false,
            is_valid_room_avatar_input: false, 

            show_chat_creation_card: false,
            show_flash_card: false, 
        }
    }, 
    methods: {
        // functions that serve the search and adding a user to the chat 
        search_user() {
            const url = `/api/v1/chat-room-api/search-target-user/?query=${this.query}`;

            fetch(url, {
                method: 'GET', 
                headers: {
                    'Content-Type': 'application/json', 
                    'Accept': 'application/json', 
                    'Authorization': `Token ${Cookies.get('token')}`,
                    'Cookie': `csrf_token=${Cookies.get('csrf_token')}`
                }
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

        create_chat_room(){
            const url = `/api/v1/chat-room-api/chat-room-actions`;

            const post_data = {
                'room_name': this.chat_room_name,
                'room_avatar': this.chat_room_avatar_base64,
                'invited_users_ids': this.invited_users_ids
            };

            fetch(url, {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json', 
                    'Authorization': `Token ${Cookies.get('token')}`,
                    'Cookie': `csrf_token=${Cookies.get('csrf_token')}`
                }, 
                body: JSON.stringify(post_data)
            })
            .then(check_response)
            .then(response => {
                if(!response.success){
                    console.log(response)
                    return;
                }
                this.close_chat_creation_card();
                chat_rooms_app.get_user_chat_rooms();

                console.log(response.data);
            })
            .catch(error => {
                call_toast(`Ошибка сервера: ${error.detail} Пожалуйста, перезайдите в аккаунт`);
            });
        },
        close_chat_creation_card(){
            // сбор ненужных данных при закрытии окна создания чата
            this.searched_users = []; 
            this.invited_users_ids = []; 

            this.chat_room_name = ''; 
            this.chat_room_avatar = undefined;
            this.query = '';
            
            this.is_valid_room_name_input = false;
            this.is_valid_room_avatar_input = false
            this.show_chat_creation_card = false;
        }, 

        // validators 
        validate_room_name(){
            if (this.chat_room_name.length < 4) {
                this.is_valid_room_name_input = false; 
                return; 
            }
            this.is_valid_room_name_input = true;
        },
        validate_room_avatar(image){
            const allowed_image_types = ['image/jpeg', 'image/webp', 'image/png'];

            if(!allowed_image_types.includes(image.type)){
                this.is_valid_room_avatar_input = false; 
                return;
            }

            this.is_valid_room_avatar_input = true; 
        },
        handle_input_avatar(event){
            const image = event.target.files[0];
            this.validate_room_avatar(image);

            const reader = new FileReader();
            reader.onload = (e) => {
                this.chat_room_avatar_base64 = e.target.result;
            };
            reader.readAsDataURL(image);
        },
    }
})

const chat_rooms_app = new Vue({
    el: '#chat-rooms-app', 
    delimiters: ['[[', ']]'],
    data(){
        return{
            user_chat_rooms: [],
            shared_chat_rooms: [],
            invitation_chat_rooms: [],

            show_empty_user_chat_rooms: false,
            show_empty_shared_chat_rooms: false,
            show_empty_invititaion: false, 

            toggle_invitation_chats: true, 
            toggle_user_chats: true, 
            toggle_shared_chats: true
        }
    }, 
    mounted(){
        this.get_invitation_chat_rooms();
        this.get_shared_chat_rooms();
        this.get_user_chat_rooms();
    },
    methods: {
        // functions for fething chat rooms
        fetch_chat_rooms(url, callback){
            fetch(url, {
                method: 'GET', 
                headers: {
                    'Content-Type': 'application/json', 
                    'Accept': 'application/json', 
                    'Authorization': `Token ${Cookies.get('token')}`,
                    'Cookie': `csrf_token=${Cookies.get('csrf_token')}`
                }
                })
                .then(check_response)
                .then(response => callback(response))
                .catch(error => {
                    call_toast(`Ошибка сервера: ${error.detail} Пожалуйста, попробуйте перезайти в аккаунт, или же обратитесь к системному администратору`);
                })
        },
        get_user_chat_rooms(){
            const url = `/api/v1/chat-room-api/user-chat-rooms`;

            this.user_chat_rooms = [];
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
            
            this.shared_chat_rooms = [];
            this.fetch_chat_rooms(url, response => {
                if(!response.shared_chat_rooms){
                    this.show_empty_shared_chat_rooms = true; 
                    return; 
                }

                this.show_empty_shared_chat_rooms = false;
                this.shared_chat_rooms = response.shared_chat_rooms;
            });
        },
        get_invitation_chat_rooms(){
            const url = `/api/v1/chat-room-api/invitation-chat-rooms`;
            
            this.invitation_chat_rooms = [];
            this.fetch_chat_rooms(url, response => {
                if(!response.invitations_chat_rooms){
                    this.show_empty_invititaion = true;
                    return;
                }

                this.show_empty_invititaion = false;
                this.invitation_chat_rooms = response.invitations_chat_rooms;
            });
        },
        
        // function for send accept/discard action for invi chat
        send_invitation_chat_action(room_id, action){
            const url = `/api/v1/chat-room-api/invitation-chat-rooms`;

            const post_data = {
                'room_id': room_id,
                'action': action
            };
            
            fetch(url, {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json', 
                    'Accept': 'application/json', 
                    'Authorization': `Token ${Cookies.get('token')}`,
                    'Cookie': `csrf_token=${Cookies.get('csrf_token')}`
                }, 
                body: JSON.stringify(post_data)
                })
                .then(check_response)
                .then(response => {
                    if(!response.success){
                        call_toast(`Ошибка: ${response.err_msg}`)
                        return;
                    }

                    this.get_invitation_chat_rooms();
                    this.get_user_chat_rooms();
                    this.get_shared_chat_rooms();
                })
                .catch(error => {
                    call_toast(`Ошибка сервера: ${error.detail} Пожалуйста, попробуйте перезайти в аккаунт, или же обратитесь к системному администратору`);
             })
        }
    }
})

const employees_app = new Vue({
    el: '#employees-app', 
    delimiters: ['[[', ']]'],
    data(){
        return{
            
        }
    }
})