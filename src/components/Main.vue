<template>
  <div class="chat-container">
    <h1 @click="$router.push('/login')" style="cursor: pointer;">저녁 뭐 먹지</h1>
    <h2>오늘의 주제: {{ currentTopic }}</h2>
    <div class="chat-box" ref="chatBox">
      <div v-for="(msg, index) in message" :key="index" :class="['chat-message', msg.user === user ? 'chat-message-self' : 'chat-message-other']">
        <div class="chat-message-header">
          <strong class="chat-user">{{ msg.user }}</strong>
        </div>
        <div class="chat-message-content">
          <p class="main chat">{{ msg.message }}</p>
        </div>
        <span class="chat-timestamp">{{ formatTimestamp(msg.timestamp) }}</span>
      </div>
    </div>

    <div class="chat-input-container">
      <input
        type="text"
        class="chat-input"
        v-model="newMessage"
        placeholder="메시지를 입력하세요"
        @keyup.enter="sendMessage"
      />
      <button class="send-button" @click="sendMessage">전송</button>
    </div>
  </div>
</template>

<script>
import '../styles/Main.css';
export default {
  data() {
    return {
      socket: null,
      message: [],
      newMessage: '',
      currentTopic: '',  // 주제 데이터를 저장할 필드
      user: localStorage.getItem('nickname') || '익명',
    };
  },
  async created() {
    // this.user = prompt("사용자 이름을 입력해주세요");
    await this.fetchTopic(); // 주제 검색하기
    await this.checkMidnightRefresh(); 
    await this.fetchPreviousMessages(); // 기존 채팅 메시지 불러오기
    this.connectWebSocket(); // WebSocket 연결
  },
  updated() {
    // 메시지가 업데이트될 때마다 최신 메시지로 스크롤
    this.scrollToBottom();
  },
  beforeDestroy() {
    if (this.socket) {
      this.socket.close();
    }
  },
  methods: {
    scrollToBottom() {
      // chatBox 요소로 스크롤 내리기
      this.$nextTick(() => {
        const chatBox = this.$refs.chatBox;
        if (chatBox) {
          chatBox.scrollTop = chatBox.scrollHeight;
        }
      });
    },
    async checkMidnightRefresh() {
      console.log("checkMidnightRefresh() 호출됨");
      let midnightAlertShown = false; // 자정 알림 중복 방지 플래그

      setInterval(() => {
        const now = new Date();
        console.log(`현재 시간: ${now.toLocaleTimeString()}`);

        // 자정 감지
        if (now.getHours() === 0 && now.getMinutes() === 0 && now.getSeconds() <= 1) {
          if (!midnightAlertShown) {
            console.log("자정이 되었습니다!");
            alert("자정이 되었습니다! 페이지를 새로고침합니다.");
            location.reload(); // 페이지 새로고침
            midnightAlertShown = true; // 알림 표시 후 플래그 설정
          }
        } else {
          // 자정 범위를 벗어나면 플래그 초기화
          midnightAlertShown = false;
        }
      }, 1000);
    },

    async fetchTopic() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/chat/current-topic/`);
        if (response.ok) {
          const data = await response.json();
          this.currentTopic = data.text; // 주제 데이터
        } else {
          console.error('주제를 검색하려는 중 오류가 있습니다.');
        }
      } catch (error) {
        console.error('Error fetching topic:', error);
      }
    },
    async fetchPreviousMessages() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/chat/history/`);
        if (response.ok) {
          const data = await response.json();
          this.message = data.reverse().map((msg) => ({
            user: msg.user,
            message: msg.content,
            timestamp: msg.timestamp, // 시간도 추가
          }));
        } else {
          console.error(
            'Failed to load previous messages. Status:',
            response.status,
            response.statusText
          );
        }
      } catch (error) {
        console.error('Error fetching previous messages:', error);
      }
    },
    connectWebSocket() {
      const socketUrl = `ws://127.0.0.1:8000/ws/chat/`;
      this.socket = new WebSocket(socketUrl);

      this.socket.onopen = () => {
        console.log('WebSocket 연결 성공1111111');
      };

      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.message) {
          this.message.push({
            user: data.user,
            message: data.message,
            timestamp: new Date().toISOString(), // 시간추가
          });
          localStorage.setItem(
            'chatMessages',
            JSON.stringify({
              messages: this.message,
              timestamp: new Date().toISOString(),
            })
          );
        }
      };

      this.socket.onclose = () => {
        console.log('WebSocket 연결 종료. 5초 후 재연결을 시도합니다.');
        setTimeout(() => {
          this.connectWebSocket();
        }, 5000);
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket 오류 발생:', error);
      };
    },
    async sendMessage() {
      if (
        this.newMessage.trim() !== '' &&
        navigator.onLine &&
        this.socket.readyState === WebSocket.OPEN
      ) {
        this.socket.send(
          JSON.stringify({
            user: this.user,
            message: this.newMessage,
          })
        );
        this.newMessage = '';
      } else {
        if (!navigator.onLine) {
          console.log('네트워크가 열린 상태가 아닙니다. 메시지를 보낼 수 없습니다.');
        } else {
          console.log(
            'WebSocket 연결이 열린 상태가 아닙니다. 메시지를 보낼 수 없습니다.'
          );
        }
      }
    },
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      const hours = date.getHours();
      const minutes = date.getMinutes().toString().padStart(2, '0');
      return `${hours}:${minutes}`; // 시간을 표시 (HH:MM)
    },
    async saveMessage(user, message) {
      try {
        const response = await fetch(`/api/chat/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ user, content: message }),
        });
        if (!response.ok) {
          console.error(
            'Failed to save message. Status:',
            response.status,
            response.statusText
          );
        }
      } catch (error) {
        console.error('Error saving message:', error);
      }
    },
  },
};
</script>
