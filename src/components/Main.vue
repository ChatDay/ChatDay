<template>
    <div class="main-container">
    <h1>이름?</h1>
    <div class="topic">
        <div class="menu">오늘의 주제: 메뉴추천</div>
    </div>
    <div class="chat-section">
    </div>
    <input type="text" placeholder="채팅을 입력해주세요!" />
    </div>
</template>

<script>
export default {
    data() {
    return {
        messages: []
    };
    },
    methods: {
    sendMessage() {
        // 메시지 보내기 로직
    }
    }
};
</script>