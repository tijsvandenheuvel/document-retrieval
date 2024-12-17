<template>
	<div class="nav">

		<!-- routes -->
		<div class="nav-router-links">
			<RouterLink to="/">Home</RouterLink>
			<RouterLink to="/documents">Documents</RouterLink>
			<!-- <RouterLink to="/about">About</RouterLink> -->
			<!-- <RouterLink to="/engine">Engine</RouterLink>
			<RouterLink to="/editor">Editor</RouterLink>
			<RouterLink to="/map">Map</RouterLink>
			<RouterLink to="/todo">To Do</RouterLink> -->
		</div>

	</div>
</template>

<script setup lang="ts">

</script>

<style scoped>
.nav {
	background-color: #333;
	overflow-x: hidden;
	overflow-y: hidden;
	position: fixed;
	overflow: hidden;
	width: 100vw;
	display: flex;

	z-index:1;
}

.nav a {
	float: left;
	color: white;
	text-align: center;
	padding: 10px 15px;
	text-decoration: none;
	font-size: 18.5px;
}

.nav a:hover {
	background-color: #ddd;
	color: #333;
}

.nav a.router-link-exact-active,
.nav .active {
	background-color: #17a2b8;
	color: white;
}

.divider {
	width: 3px;
	background: white;
}
</style>