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
</div>
</template>

<script>
export default {
data() {
    return {
    nickname: '',
    username: '',
    password: '',
    email: ''
    };
},
methods: {
    register() {
      // 회원가입 로직 구현
    console.log('Register:', this.nickname, this.username, this.password, this.email);
    this.$router.push('/login');
    }
}
};
</script>
