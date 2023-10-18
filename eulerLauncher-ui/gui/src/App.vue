<script setup>
import Index from './components/index.vue'
</script>


<template>
  <div class="center-col h100 w100 scroll">
    <!-- <div class="logo-box">
      <img alt="pywebview logo" src="./assets/pywebview.png" />
      <img class="ml50 mr50" alt="pyinstaller logo" src="./assets/pyinstaller.png" />
      <img alt="Vue logo" src="./assets/vue.png" />
    </div> -->
    <Index/>
    <!-- <router-view /> -->
  </div>
</template>

<style>
.scroll {
  overflow: scroll;
  background-color: #F7F7F7;
  height: 100vh;
}

.logo-box span {
  width: 74px;
}
</style>
