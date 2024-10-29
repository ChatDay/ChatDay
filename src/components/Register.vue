<template>
    <div class="register-container">
    <h1>ChatDay</h1>
    <div class="input-container">
        <input type="text" placeholder="닉네임" v-model="nickname" />
        <input type="text" placeholder="아이디" v-model="username" />
        <input type="password" placeholder="비밀번호" v-model="password" />
        <input type="email" placeholder="이메일" v-model="email" />
    </div>
    <button @click="register">가입 완료!</button>
    <p>{{ message }}</p>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
    return {
        message: '',
        nickname: '',
        username: '',
        password: '',
        email: '',
    };
    },
    methods: {
      // 회원가입 메서드
    register() {
        if (!this.validateEmail(this.email)) {
        this.message = '올바른 이메일 주소를 입력해주세요.';
        return;
        }

        const payload = {
        nickname: this.nickname,
        username: this.username,
        password: this.password,
        email: this.email,
        };

        axios
        .post('http://127.0.0.1:8000/api/accounts/signup/', payload)
        .then(response => {
            this.message = '회원가입 성공! 로그인 페이지로 이동합니다.';
            this.$router.push('/login'); // 회원가입 후 로그인 페이지로 이동
        })
        .catch(error => {
            console.error('회원가입 에러:', error);
            if (error.response && error.response.data) {
            this.message = `회원가입 실패: ${error.response.data.email || '다시 시도해주세요.'}`;
            } else {
            this.message = '회원가입 실패. 다시 시도해주세요.';
            }
        });
    },
      // 이메일 형식 검증 메서드
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    }
};
</script>
