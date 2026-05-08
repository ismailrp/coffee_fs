<script setup>
import { ref } from "vue";

import api from "../services/api";

const username = ref("");
const password = ref("");

const error = ref("");

const login = async () => {
  try {
    const response = await api.post("/auth/login", {
      username: username.value,
      password: password.value,
    });

    localStorage.setItem("token", response.data.access_token);

    window.location.reload();
  } catch (err) {
    error.value = "Login failed";
  }
};
</script>

<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-4">
        <div class="card p-4">
          <h3 class="mb-3">Coffee Dashboard Login</h3>

          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>

          <input
            v-model="username"
            class="form-control mb-3"
            placeholder="Username"
          />

          <input
            v-model="password"
            type="password"
            class="form-control mb-3"
            placeholder="Password"
          />

          <button @click="login" class="btn btn-primary">Login</button>
        </div>
      </div>
    </div>
  </div>
</template>
