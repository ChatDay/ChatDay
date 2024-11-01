<template>
  <div class="chat-container">
    <h1>ChatDay - 실시간 채팅</h1>
    <div class="chat-box" ref="chatBox">
      <div v-for="(msg, index) in messages" :key="index" class="chat-message">
        <strong>{{ msg.user }}:</strong> {{ msg.message }}
      </div>
    </div>
    <input
      type="text"
      v-model="newMessage"
      placeholder="메시지를 입력하세요"
      @keyup.enter="sendMessage"
    />
    <button @click="sendMessage">전송</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      socket: null,
      messages: [], // 복수형으로 변경
      newMessage: '',
      roomName: 'default', // 채팅방 이름 설정
      user: '사용자1', // 하드코딩된 사용자 이름
    };
  },
  created() {
    this.connectWebSocket();
  },
  methods: {
    connectWebSocket() {
      // WebSocket 서버에 연결
      const socketUrl = `ws://127.0.0.1:8000/ws/chat/${this.roomName}/`;
      this.socket = new WebSocket(socketUrl);

      // WebSocket 이벤트 설정
      this.socket.onopen = () => {
        console.log('WebSocket 연결 성공');
      };

      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.message) {
          this.messages.push({
            user: data.user,
            message: data.message,
          });
          // 새로운 메시지가 추가되면 스크롤을 맨 아래로 이동
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        }
      };

      this.socket.onclose = () => {
        console.log('WebSocket 연결 종료. 5초 후 재연결을 시도합니다.');
        setTimeout(() => {
          this.connectWebSocket();
        }, 5000); // 5초 후 재연결 시도
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket 오류 발생:', error);
      };
    },
    sendMessage() {
      if (this.newMessage.trim() !== '' && this.socket.readyState === WebSocket.OPEN) {
        // WebSocket을 통해 메시지 전송
        this.socket.send(JSON.stringify({
          'user': this.user,
          'message': this.newMessage,
        }));
        this.newMessage = ''; // 입력 필드 초기화
      } else {
        console.log('WebSocket 연결이 열려 있지 않습니다. 메시지를 보낼 수 없습니다.');
      }
    },
    scrollToBottom() {
      const chatBox = this.$refs.chatBox;
      if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    }
  },
  beforeDestroy() {
    // 컴포넌트가 파괴되기 전에 WebSocket 연결 해제
    if (this.socket) {
      this.socket.close();
    }
  }
};
</script>

<style scoped>
.chat-container {
  max-width: 600px;
  margin: auto;
  text-align: center;
  background-color: #f0f0f0;
  padding: 20px;
  border-radius: 10px;
}
.chat-box {
  height: 300px;
  overflow-y: auto;
  background-color: #ffffff;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  border: 1px solid #ffffff;
}
.chat-message {
  padding: 5px;
  text-align: left;
  margin-bottom: 5px;
  background-color: #ececec;
  border-radius: 5px;
}
input {
  width: 80%;
  padding: 10px;
}
button {
  padding: 10px;
}
</style>
