Vue.component('flash-card', {
    props: ['message'],
    delimiters: ['[[', ']]'],
    template: `
                <div class="container mb-3 animate__animated animate__shakeX">
                      <div class="row">
                          <div class="col-12">
                              <div class="card rounded-3 p-2 alert-error-card">
                                  [[ message ]]
                              </div>
                          </div>
                      </div>
                 </div>
    `
})

Vue.component('chat-message', {
    props: ['message'],
    delimiters: ['[[', ']]'],
    template: `
        <li class="list-group-item border-0 mb-2 animate__animated animate__pulse">
            <div class="p-0">
                <div class="d-flex justify-content-start align-items-start">
                    <div class="position-relative me-2" style="flex-shrink: 0">
                        <img :src="message.avatar" class="rounded-avatar" />
                        <span class="online-marker"></span>
                    </div>
                    <div class="message-container flex-grow-1">
                        <p class="m-0 small chat-box-left">
                            [[ message.message ]]
                        </p>
                    </div>
                </div>
                
                <div class="mx-5 d-flex justify-content-start align-items-center">
                    <img src="/static/image/svg/icon-calendar.svg" width="15px">
                    <p class="m-0 mx-1 small text-start" style="opacity: .6;">[[ message.time ]] | [[ message.date ]] | [[ message.username ]]</p>
                </div>
            </div>
        </li>      
    `
})

Vue.component('validate-card', {
    props: ['message'],
    delimiters: ['[[', ']]'],
    template: `
                
    `
})

// chat app components
Vue.component('user-chat-room', {
    props: ['user_room'],
    delimiters: ['[[', ']]'],
    template: `
    <div class="chat-container-hvr d-flex justify-content-start mt-2 mb-1 animate__animated animate__fadeInDown">
        <div class="position-relative" style="flex-shrink: 0;">
            <img :src="user_room.room_avatar" class="rounded-avatar" />
        </div>

        <div class="mx-2">
            <p class="mt-0 mb-0">[[ user_room.room_name ]]</p>
            <p class="small text-muted"><strong>Участники</strong>: [[ user_room.participants.join(', ') ]]</p>
        </div>
    </div> 
    `
})

Vue.component('shared-chat-room', {
    props: ['shared_chat_room'],
    delimiters: ['[[', ']]'],
    template: `
    <div class="chat-container-hvr d-flex justify-content-start mt-2 mb-3 animate__animated animate__fadeInDown">
        <div class="position-relative" style="flex-shrink: 0;">
            <img :src="shared_chat_room.room_avatar" class="rounded-avatar" />
        </div>

        <div class="mx-1">
            <p class="mt-0 mb-0">[[ shared_chat_room.room_name ]]</p>
            <p class="mt-0 mb-0 small text-muted">Создатель: [[ shared_chat_room.room_owner ]]</p>
        </div>

        <div class="d-flex align-items-center mb-3 mt-2">
            <button class="btn btn-sm btn-outline-success mx-2">Присоединиться</button>
            <button class="btn btn-sm btn-outline-secondary">Подробнее</button>
        </div>
    </div> 
    `
})

Vue.component('search-user-card', {
    props: ['searched_user', 'invited_users_ids'],
    delimiters: ['[[', ']]'],
    template: `
    <div class="d-flex justify-content-center mt-2 mb-1 animate__animated animate__fadeInDown">
        <div class="position-relative mt-1" style="flex-shrink: 0;">
            <img :src="searched_user.src_avatar" class="rounded-avatar" />
            <span class="badge-online-marker"></span>
        </div>

        <div class="mx-2">
            <p class="mt-0 mb-0">[[ searched_user.last_name ]] [[ searched_user.first_name ]]</p>
            <div class="">
                <button class="btn btn-sm btn-outline-success" :disabled="invited_users_ids.includes(searched_user.pk)" @click="$emit('invite-user', searched_user.pk)">Пригласить</button>
                <button class="btn btn-sm btn-outline-secondary" @click="$emit('show-details', searched_user.pk)">Подробнее</button>
            </div>
        </div>
    </div>
    `
})