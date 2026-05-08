<script setup>
import { onMounted, ref } from "vue";

import api from "../services/api";

const coffees = ref([]);

const showModal = ref(false);

const selectedCoffee = ref(null);

const quantity = ref(1);

const notes = ref("");

const successMessage = ref("");

const loadCoffees = async () => {
  const response = await api.get("/coffees");

  coffees.value = response.data;
};

const openOrderModal = (coffee) => {
  selectedCoffee.value = coffee;

  quantity.value = 1;

  notes.value = "";

  showModal.value = true;
};

const createOrder = async () => {
  try {
    await api.post("/orders", {
      coffee_id: selectedCoffee.value.id,
      quantity: quantity.value,
      notes: notes.value,
    });

    successMessage.value = "Order created successfully";

    showModal.value = false;
  } catch (err) {
    console.error(err);

    alert("Failed to create order");
  }
};

const logout = () => {
  localStorage.removeItem("token");

  window.location.reload();
};

onMounted(() => {
  loadCoffees();
});
</script>

<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between mb-3">
      <h2>Coffee Dashboard</h2>

      <button @click="logout" class="btn btn-danger">Logout</button>
    </div>

    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>

    <table class="table table-bordered">
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Description</th>
          <th>Image</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="coffee in coffees" :key="coffee.id">
          <td>{{ coffee.id }}</td>

          <td>{{ coffee.title }}</td>

          <td>{{ coffee.description }}</td>

          <td>
            <img :src="coffee.image" width="80" />
          </td>

          <td>
            <button @click="openOrderModal(coffee)" class="btn btn-primary">
              Order
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- MODAL -->

    <div v-if="showModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Order Coffee</h5>

            <button class="btn-close" @click="showModal = false"></button>
          </div>

          <div class="modal-body">
            <p>
              {{ selectedCoffee?.title }}
            </p>

            <input
              v-model="quantity"
              type="number"
              class="form-control mb-3"
              placeholder="Quantity"
            />

            <textarea
              v-model="notes"
              class="form-control"
              placeholder="Notes"
            ></textarea>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showModal = false">
              Close
            </button>

            <button class="btn btn-primary" @click="createOrder">
              Submit Order
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
