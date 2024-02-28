Vue.component('user-chat-room', {
    props: ['user_room'],
    delimiters: ['[[', ']]'],
    template: `
    <div class="chat-container-hvr d-flex justify-content-start mt-2 mb-1 animate__animated animate__fadeInDown" style="cursor: default;">
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
    <div class="d-flex justify-content-start mt-2 mb-3 animate__animated animate__fadeInDown" style="cursor: default;">
        <div class="position-relative" style="flex-shrink: 0;">
            <img :src="shared_chat_room.room_avatar" class="rounded-avatar" />
        </div>

        <div class="mx-1">
            <p class="mt-0 mb-0">[[ shared_chat_room.room_name ]]</p>
            <p class="mt-0 mb-0 small text-muted">Создатель: [[ shared_chat_room.room_owner ]]</p>
        </div>

        <div class="d-flex align-items-center ms-auto mb-3 mt-2">
                <button class="border-0 btn-transition btn btn-outline-success" @click="$emit('chat-action', invitation_chat_room.room_id, 'accept')">
                    <svg width="15px" height="15px" viewBox="0 0 14 14" role="img" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
                        <path fill="currentColor" d="M13 4.1974q0 .3097-.21677.5265L7.17806 10.329l-1.0529 1.0529q-.21677.2168-.52645.2168-.30968 0-.52645-.2168L4.01935 10.329 1.21677 7.5264Q1 7.3097 1 7t.21677-.5265l1.05291-1.0529q.21677-.2167.52645-.2167.30968 0 .52645.2167l2.27613 2.2839 5.07871-5.0864q.21677-.2168.52645-.2168.30968 0 .52645.2168l1.05291 1.0529Q13 3.8877 13 4.1974z"/>
                    </svg>
                </button>
        </div>
    </div> 
    `
})

Vue.component('invitation-chat-room', {
    props: ['invitation_chat_room'],
    delimiters: ['[[', ']]'],
    template: `
    <div class="mb-2">
        <div class="d-flex justify-content-start mt-2 mb-3 animate__animated animate__fadeInDown" style="cursor: default;">
            <div class="position-relative" style="flex-shrink: 0;">
                <img :src="invitation_chat_room.room_avatar" class="rounded-avatar" />
            </div>
            <div class="mx-1">
                <p class="mt-0 mb-0">[[ invitation_chat_room.room_name ]]</p>
                <p class="mt-0 mb-0 small text-muted">Создатель: [[ invitation_chat_room.room_owner ]] | Вас пригласил: [[ invitation_chat_room.inviting_user ]]</p>
            </div>
            <div class="d-flex align-items-center ms-auto mb-3 mt-2">
                <button class="border-0 btn-transition btn btn-outline-success" @click="$emit('chat-action', invitation_chat_room.room_id, 'accept')">
                    <svg width="15px" height="15px" viewBox="0 0 14 14" role="img" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
                        <path fill="currentColor" d="M13 4.1974q0 .3097-.21677.5265L7.17806 10.329l-1.0529 1.0529q-.21677.2168-.52645.2168-.30968 0-.52645-.2168L4.01935 10.329 1.21677 7.5264Q1 7.3097 1 7t.21677-.5265l1.05291-1.0529q.21677-.2167.52645-.2167.30968 0 .52645.2167l2.27613 2.2839 5.07871-5.0864q.21677-.2168.52645-.2168.30968 0 .52645.2168l1.05291 1.0529Q13 3.8877 13 4.1974z"/>
                    </svg>
                </button>
                <button class="border-0 btn-transition btn btn-outline-danger" @click="$emit('chat-action', invitation_chat_room.room_id, 'discard')">
                    <svg width="16" height="16" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M432 32H312l-9.4-18.7A24 24 0 0 0 281.1 0H166.8a23.72 23.72 0 0 0-21.4 13.3L136 32H16A16 16 0 0 0 0 48v32a16 16 0 0 0 16 16h416a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16zM53.2 467a48 48 0 0 0 47.9 45h245.8a48 48 0 0 0 47.9-45L416 128H32z" fill="currentColor"/>
                    </svg>
                </button>
            </div>
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

Vue.component('employee', {
    props: ['employee'],
    delimiters: ['[[', ']]'],
    template: `
    <div class="chat-container-hvr d-flex justify-content-start mt-2 mb-1 animate__animated animate__fadeInDown" style="cursor: default;">
        <div class="position-relative" style="flex-shrink: 0;">
            <img :src="employee.src_avatar" class="rounded-avatar" />
            <span v-bind:class="{ 'badge-online-marker': employee.is_online, 'badge-offline-marker': !employee.is_online }"></span>
        </div>

        <div class="mx-2">
            <p class="mt-0 mb-0">[[ employee.last_name ]] [[ employee.first_name ]] 
            <span v-show="!employee.is_online" class="badge bg-danger animate__animated animate__fadeInRight">Был в сети: [[ employee.last_activity ]]</span>
            <span v-show="employee.is_online" class="badge bg-success animate__animated animate__fadeInRight">В сети</span>
            </p>
            <p class="small text-muted">Last Message In This Chat</p>
        </div>
    </div>
    `
})
