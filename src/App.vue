<template>
    <div id="app">
    <router-view v-slot="{ Component, isRouteChanging }">
        <transition name="page-flip" mode="out-in">
        <div v-if="isRouteChanging" class="loading">로딩 중...</div>
        <component v-else :is="Component" />
        </transition>
    </router-view>
    </div>
</template>
<script>
export default {
name: 'App',
};
</script>

<style src="./styles/App.css"></style>
