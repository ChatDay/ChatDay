<template>
    <div class="login-container">
    <h1>ChatDay</h1>
    <div class="input-container">
        <input type="text" placeholder="아이디를 입력해주세요" v-model="username" />
        <input type="password" placeholder="비밀번호를 입력해주세요" v-model="password" />
    </div>
    <button @click="login">로그인</button>
    <button @click="goToRegister">회원가입을 원하십니까?</button>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
    return {
        username: '',
        password: ''
    };
    },
    methods: {
    async login() {
        try {
          // 로그인 API 요청
        const response = await axios.post('http://localhost:8000/api/token/', {
            username: this.username,
            password: this.password
        });
        
          // 성공적으로 응답을 받으면, 토큰을 저장 (예: localStorage)
        localStorage.setItem('accessToken', response.data.access);
        localStorage.setItem('refreshToken', response.data.refresh);
        console.log('로그인 성공:', response.data);
        
          // 로그인 후 메인 페이지로 이동
        this.$router.push('/main');
        } catch (error) {
        console.error('로그인 실패:', error);
        alert('로그인에 실패하였습니다. 아이디와 비밀번호를 확인하세요.');
        }
    },
    goToRegister() {
        this.$router.push('/register');
    }
    }
};
</script>