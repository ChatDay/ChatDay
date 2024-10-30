<template>
    <div class="login-container">
    <h1>ChatDay</h1>
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
created() {
    // 로그인 페이지에 접근 시 로컬 스토리지 초기화
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
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
          // 서버에서 토큰 받아오기
        const { access, refresh } = response.data;

          // 로컬 스토리지에 토큰 저장
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);

        this.message = '로그인 성공!';
          // 로그인 성공 시 페이지 이동 등 추가 작업 수행
        this.$router.push('/main');
        })
        .catch(error => {
        console.error('로그인 에러:', error);
        if (error.response && error.response.status === 401) {
            this.message = '아이디 또는 비밀번호가 잘못되었습니다. 다시 확인해주세요.';
        } else {
            this.message = '로그인 실패. 다시 시도해주세요.';
        }
        });
    }
}
};
</script>

<style scoped>
.login-container {
    padding: 20px;
    background-color: #f9f295;
    max-width: 400px;
    margin: auto;
    text-align: center;
}
.input-container {
    margin-bottom: 20px;
}
input {
    width: 90%;
    padding: 10px;
    margin: 10px 0;
}
button {
    padding: 10px;
    margin: 5px;
}
</style>
