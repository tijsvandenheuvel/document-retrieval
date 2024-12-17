
<template>
    <div id="nav">
        <NavBar></NavBar>
    </div>
    <div id="main">
        <RouterView/>
    </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBar from './components/NavBar.vue'
</script>


<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
	position: absolute;
	top: 0;
  left: 0;
	height: 50px;
	overflow: hidden;
}

#main {
  position: absolute;
  top: 50px;
  left:0;
  width: 100vw;
  min-height: 94vh;
}
</style>

