<script setup>
import { onMounted, ref } from "vue";

import api from "../services/api";

const coffees = ref([]);

const showModal = ref(false);

const selectedCoffee = ref(null);

const quantity = ref(1);

const notes = ref("");

const successMessage = ref("");

const showEditModal = ref(false);

const editCoffee = ref({
  id: null,
  title: "",
  description: "",
  image: "",
});

const loadCoffees = async () => {
  try {
    const response = await api.get("/coffees");

    coffees.value = response.data;
  } catch (err) {
    console.error(err);
  }
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

const openEditModal = (coffee) => {
  editCoffee.value = {
    id: coffee.id,
    title: coffee.title,
    description: coffee.description,
    image: coffee.image,
  };

  showEditModal.value = true;
};

const updateCoffee = async () => {
  try {
    await api.put(`/coffees/${editCoffee.value.id}`, {
      title: editCoffee.value.title,
      description: editCoffee.value.description,
      image: editCoffee.value.image,
    });

    successMessage.value = "Coffee updated successfully";

    showEditModal.value = false;

    loadCoffees();
  } catch (err) {
    console.error(err);

    alert("Failed to update coffee");
  }
};

const deleteCoffee = async (id) => {
  const confirmed = confirm("Delete this coffee?");

  if (!confirmed) return;

  try {
    await api.delete(`/coffees/${id}`);

    successMessage.value = "Coffee deleted successfully";

    loadCoffees();
  } catch (err) {
    console.error(err);

    alert("Failed to delete coffee");
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
            <div class="d-flex gap-2">
              <button
                @click="openOrderModal(coffee)"
                class="btn btn-primary btn-sm"
              >
                Order
              </button>

              <button
                @click="openEditModal(coffee)"
                class="btn btn-warning btn-sm"
              >
                Edit
              </button>

              <button
                @click="deleteCoffee(coffee.id)"
                class="btn btn-danger btn-sm"
              >
                Delete
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- ORDER MODAL -->

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

    <!-- EDIT MODAL -->

    <div v-if="showEditModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Coffee</h5>

            <button class="btn-close" @click="showEditModal = false"></button>
          </div>

          <div class="modal-body">
            <input
              v-model="editCoffee.title"
              class="form-control mb-3"
              placeholder="Title"
            />

            <textarea
              v-model="editCoffee.description"
              class="form-control mb-3"
              placeholder="Description"
            ></textarea>

            <input
              v-model="editCoffee.image"
              class="form-control"
              placeholder="Image URL"
            />
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showEditModal = false">
              Close
            </button>

            <button class="btn btn-warning" @click="updateCoffee">
              Update
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
