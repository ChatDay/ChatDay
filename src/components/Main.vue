<template>
  <div class="chat-container">
    <h1>ChatDay - 실시간 채팅</h1>
    <div class="chat-box">
      <div v-for="(msg, index) in message" :key="index" class="chat-message">
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
      message: [],
      newMessage: '',
      roomName: 'default', // 채팅방 이름 설정
      user: '사용자1'  // 하드코딩된 사용자 이름
    };
  },
  async created() {
    await this.fetchPreviousMessages(); // 기존 채팅 메시지 불러오기
    this.connectWebSocket();            // WebSocket 연결
  },
  mounted() {
  const savedMessages = localStorage.getItem('chatMessages');
  if (savedMessages) {
    const savedData = JSON.parse(savedMessages);
    const currentTime = new Date();
    const lastSavedTime = new Date(savedData.timestamp);

    // 저장된 날짜가 오늘인지 확인
    if (currentTime.getDate() === lastSavedTime.getDate() &&
    currentTime.getMonth() === lastSavedTime.getMonth() &&
    currentTime.getFullYear() === lastSavedTime.getFullYear()) {
  this.message = savedData.messages;
} else {
  // 날짜가 다르면 로컬 스토리지에서 삭제
  localStorage.removeItem('chatMessages');
  this.message = []; // 메시지 배열 초기화
}
  }

  // 자정에 자동으로 새로고침 설정 - 매 1분 자정인지 확인
  setInterval(() => {
  const now = new Date();
  if (now.getHours() === 0 && now.getMinutes() === 0) {
    console.log('자정에 도달했습니다. 페이지를 새로고침합니다.');
    window.location.href = window.location.href; // 페이지 새로고침
  }
}, 60000); // 1분마다 확인
},
  beforeDestroy() {
    // 컴포넌트가 파괴되기 전에 WebSocket 연결 해제
    if (this.socket) {
      this.socket.close();
    }
  },
  methods: {
    async fetchPreviousMessages() {
      try {
        const response = await fetch(`/api/chat/history/`);  // API 접근을 위한 URL을 사용
        if (response.ok) {
          const data = await response.json();
          this.message = data.map(msg => ({
            user: msg.user,
            message: msg.content  // Django에서 반환된 데이터와 일치하도록 설정
          }));
        } else {
          console.error("Failed to load previous messages. Status:", response.status, response.statusText);
        }
      } catch (error) {
        console.error("Error fetching previous messages:", error);
      }
    },
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
          this.message.push({
            user: data.user,
            message: data.message
          });
          // 타임스탬프와 함께 저장
          localStorage.setItem('chatMessages', JSON.stringify({
            messages: this.message,
            timestamp: new Date().toISOString()
          }));
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
    async sendMessage() {
      if (this.newMessage.trim() !== '' && navigator.onLine && this.socket.readyState === WebSocket.OPEN) {
        // WebSocket을 통해 메시지 전송
        this.socket.send(JSON.stringify({
          'user': this.user,
          'message': this.newMessage
        }));
        this.newMessage = ''; // 입력 필드 초기화
      } else {
        if (!navigator.onLine) {
          console.log('네트워크가 연결되어 있지 않습니다. 메시지를 보낼 수 없습니다.');
        } else {
          console.log('WebSocket 연결이 열려 있지 않습니다. 메시지를 보낼 수 없습니다.');
        }
      }
    },
    async saveMessage(user, message) {
      try {
        const response = await fetch(`/api/chat/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ user, content: message }) // 필드 이름을 content로 수정
        });
        if (!response.ok) {
          console.error('Failed to save message. Status:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error saving message:', error);
      }
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
