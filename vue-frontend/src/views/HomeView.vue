<template>
  <main>
    <h1>Home page</h1>
    <div>
      <RouterLink to="/search" class="rl"><button class="mega-button"> Search documents here </button></RouterLink>
      <RouterLink to="/documents" class="rl"><button class="mega-button">Browse documents here </button></RouterLink>


    </div>
  </main>
</template>

<script setup lang="ts">

</script>

<style lang="css" scoped>
.mega-button {
  margin: 10px;
  height: 100px;
  font-size: 2em;

}

.rl {
  color: #f0f0f0;
}
</style>