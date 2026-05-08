<script setup>
import LoginPage from "./pages/LoginPage.vue";

import DashboardPage from "./pages/DashboardPage.vue";

const token = localStorage.getItem("token");
</script>

<template>
  <LoginPage v-if="!token" />

  <DashboardPage v-else />
</template>
