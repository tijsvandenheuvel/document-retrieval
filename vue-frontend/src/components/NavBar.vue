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

		<div class="nav-page-buttons" v-if="isDocumentsRoute">  
			<SegmentButton :options="['Folders', 'List']" v-model="selectedOption"  @change="documentStore.setSelectedOption(selectedOption);"/>
		</div>

	</div>
</template>

<script setup lang="ts">
import SegmentButton from '../components/ui/SegmentButton.vue';
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useDocumentStore } from '../stores/documentStore';


const route = useRoute();
const isDocumentsRoute = computed(() => route.path === '/documents');

const documentStore = useDocumentStore();

const selectedOption = computed({
  get: () => documentStore.selectedOption,
  set: (value) => documentStore.setSelectedOption(value),
});

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
	justify-content: space-between;

	z-index:1;
}

.nav-page-buttons {
	/* border: solid red; */
	padding: 0;
	padding-right: 20px;
	width: 250px;
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