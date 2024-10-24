<template>
<div class="login-container">
    <h1>놀다가자 ~</h1>
    <div class="input-container">
    <input type="text" placeholder="아이디를 입력해주세요" v-model="username" />
    <input type="password" placeholder="비밀번호를 입력해주세요" v-model="password" />
    </div>
    <button @click="login">로그인</button>
    <button @click="goToRegister">회원가입을 원하십니까?</button>
</div>
</template>

<script>
export default {
data() {
    return {
    username: '',
    password: ''
    };
},
methods: {
    login() {
      // 로그인 로직 구현
    console.log('Login:', this.username, this.password);
    this.$router.push('/main');
    },
    goToRegister() {
    this.$router.push('/register');
    }
}
};
</script>
