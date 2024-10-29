<template>
    <div class="main-container">
    <h1>ChatDay</h1>
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
export default {
    data() {
    return {
        messages: [],
        newMessage: ''
    };
    },
    methods: {
    sendMessage() {
        if (this.newMessage.trim() !== '') {
          // 메시지를 배열에 추가
        this.messages.push(this.newMessage);
          // 입력 필드 초기화
        this.newMessage = '';
        }
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
</style>