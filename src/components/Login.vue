<template>
    <div class="login-container">
    <h1>ChatDay 로그인</h1>
    <div class="input-container">
        <input type="text" placeholder="아이디" v-model="username" />
        <input type="password" placeholder="비밀번호" v-model="password" />
    </div>
    <button @click="login">로그인</button>
    <button @click="$router.push('/register')">회원가입</button>
    <p>{{ message }}</p>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
    return {
        message: '',
        username: '',
        password: '',
    };
    },
    methods: {
      // 로그인 메서드
    login() {
        // 비어 있는 필드 확인
        if (!this.username || !this.password) {
        this.message = '아이디와 비밀번호를 입력해주세요.';
        return;
        }

        const payload = {
        username: this.username,
        password: this.password,
        };

        axios
        .post('http://127.0.0.1:8000/api/accounts/login/', payload)
        .then(response => {
            this.message = '로그인 성공!';
            // 로그인 성공 시 페이지 이동 등 추가 작업 수행
            this.$router.push('/main');
        })
        .catch(error => {
            console.error('로그인 에러:', error);
            if (error.response && error.response.data) {
            this.message = `로그인 실패: ${Object.values(error.response.data).join(', ')}`;
            } else {
            this.message = '로그인 실패. 다시 시도해주세요.';
            }
        });
    }
    
    }
};
</script>
