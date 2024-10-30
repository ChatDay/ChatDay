<template>
  <div class="main-container">
    <h1>ChatDay</h1>
    <button @click="logout">로그아웃</button>
    <p v-if="logoutMessage" class="logout-message">{{ logoutMessage }}</p>
    <div class="topic">
      <div class="menu">오늘의 주제: 메뉴추천</div>
    </div>
    <div class="chat-section">
      <div v-for="(message, index) in messages" :key="index" class="chat-message">
        {{ message }}
      </div>
    </div>
    <input
      type="text"
      v-model="newMessage"
      placeholder="채팅을 입력해주세요!"
      @keyup.enter="sendMessage"
    />
    <button @click="sendMessage">전송</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      messages: [],
      newMessage: '',
      logoutMessage: '' // 로그아웃 상태 메시지
    };
  },
  created() {
    // 페이지가 로드될 때 토큰을 확인하여 로그인 상태를 검사합니다.
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      console.log('로그인되지 않은 사용자입니다. 로그인 페이지로 이동합니다.');
      this.$router.push('/login'); // 토큰이 없으면 로그인 페이지로 리다이렉트
    }
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim() !== '') {
        // 메시지를 배열에 추가
        this.messages.push(this.newMessage);
        // 입력 필드 초기화
        this.newMessage = '';
      }
    },
    logout() {
  console.log('로그아웃 시작');
  
  // 로컬 스토리지에서 refreshToken 가져오기
  const refreshToken = localStorage.getItem("refresh_token");
  
  if (!refreshToken) {
    console.log("토큰 없음. 이미 로그아웃 상태입니다.");
    this.logoutMessage = "이미 로그아웃 상태입니다.";
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    return;
  }

  // 서버에 로그아웃 요청 보내기
  axios
    .post(
      "http://127.0.0.1:8000/api/accounts/logout/",
      { refresh: refreshToken },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        }
      }
    )
    .then(response => {
      console.log('서버 로그아웃 성공');
      
      // 모든 토큰 제거
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      
      // 로그아웃 성공 메시지 표시
      this.logoutMessage = "로그아웃 되었습니다.";

      // 로그인 페이지로 이동
      this.$router.push("/login");
    })
    .catch(error => {
      console.error("로그아웃 실패:", error);
      this.logoutMessage = "로그아웃에 실패했습니다. 다시 시도해주세요.";
    });
}
  }
};
</script>

<style scoped>
.main-container {
  padding: 20px;
  background-color: #f9f295;
  max-width: 600px;
  margin: auto;
  text-align: center;
}
.topic {
  background-color: #f0f0f0;
  padding: 20px;
  margin-bottom: 20px;
}
.chat-section {
  height: 300px;
  overflow-y: auto;
  margin-bottom: 20px;
  background-color: #fff9c4;
  padding: 10px;
}
.chat-message {
  margin: 5px 0;
  text-align: left;
  padding: 5px;
  background-color: #fff;
  border-radius: 5px;
}
input {
  width: 70%;
  padding: 10px;
  margin-bottom: 10px;
}
button {
  padding: 10px;
}
.logout-message {
  color: red;
  margin-bottom: 20px;
}
</style>
