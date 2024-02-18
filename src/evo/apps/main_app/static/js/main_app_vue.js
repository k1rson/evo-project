let url = `ws://${window.location.hostname}:8001/ws/main_chat/`;
const chatSocket = new WebSocket(url);

chatSocket.onmessage = (e) => {
  let data = JSON.parse(e.data);
  chat_app.add_message_to_chat(data);
}

const chat_app = new Vue({
  el: '#chat-app',
  delimiters: ['[[', ']]'],
  data() {
      return {
          messages: [],
          form_message: '', 
      }
  },
  beforeMount() {

  },
  methods: {
    add_message_to_chat(message) {
      this.messages.push(message);
    },
    send_message() {
      let send_msg = {
        'token': Cookies.get('token'), 
        'message': this.form_message
      }

      console.log(send_msg)
      chatSocket.send(JSON.stringify(send_msg))

      this.form_message = ''
    }
  },
})

