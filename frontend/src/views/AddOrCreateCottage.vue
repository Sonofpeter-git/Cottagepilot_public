<template>
  <div class="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <h1 class="text-3xl font-bold mb-6 text-gray-900">Add or Create Cottage</h1>
      <section class="mb-8 p-6 bg-popUpBg rounded-md">
        <h2 class="text-xl text-secondary font-semibold mb-2">How to be invited to a cottage</h2>
        <p class="text-secondary">
          Ask the cottage owner to invite you to the cottage. After the invitation, check your email for the invitation link or instructions.
        </p>
      </section>

      <section class="p-6 bg-popUpBg rounded-md">
        <h2 class="text-xl font-semibold  text-secondary">Create your own</h2>
        <p class="text-secondary pb-5 ">Start my own</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="plan in plans" :key="plan.id" class="bg-popUpBg rounded-lg shadow p-6 flex flex-col">
            <h2 class="text-2xl font-semibold mb-4 text-gray-800">{{ plan.name }}</h2>
            <p class="text-3xl font-bold mb-6 text-gray-900">{{ plan.price }}</p>
            <ul class="mb-6 space-y-2 flex-grow">
              <li v-for="feature in plan.features" :key="feature" class="text-gray-700">• {{ feature }}</li>
            </ul>
            <button
              @click="openModal(plan.id)"
              class="mt-auto bg-primary hover:font-bold hover:shadow-md text-white font-semibold py-2 px-4 rounded"
            >
              Start
            </button>
          </div>
        </div>

        <div v-if="modalVisible" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div class="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 class="text-2xl font-bold mb-4 text-gray-900">Create Cottage</h2>
            <form @submit.prevent="submitCottage">
              <div class="mb-4">
                <label for="name" class="block text-gray-700 font-semibold mb-1">Cottage name</label>
                <input
                  id="name"
                  v-model="form.name"
                  type="text"
                  required
                  class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div class="mb-4">
                <label for="address" class="block text-gray-700 font-semibold mb-1">Cottage address</label>
                <input
                  id="address"
                  v-model="form.address"
                  type="text"
                  required
                  class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div class="mb-4">
                <label for="subscription" class="block text-gray-700 font-semibold mb-1">Cottage subscription</label>
                <select
                  id="subscription"
                  v-model="form.plan"
                  required
                  class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="" disabled>Select a subscription</option>
                  <option value="Basic">Basic</option>
                  <option value="Standard">Standard</option>
                  <option value="Professional">Professional</option>
                </select>
              </div>
              <div class="flex justify-end space-x-4">
                <button
                  type="button"
                  @click="closeModal"
                  class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 text-gray-800 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700 text-white font-semibold"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const modalVisible = ref(false)
const errors = ref<{ [key: string]: string[] }>({})

const form = ref({
  name: '',
  address: '',
  plan: '',
})


const plans = [
  {
    id: 1,
    name: 'Basic',
    price: '€14.99/mo',
    features: ['Users: 1 user', 'Sensors: No support', 'Simple task management'],
  },
  {
    id: 2,
    name: 'Standard',
    price: '€19.99/mo',
    features: ['Users: Up to 3 users', 'Sensors: Support for 2 sensor', 'Tasks: Task sharing and reminders'],
  },
  {
    id: 3,
    name: 'Premium',
    price: '€24.99/mo',
    features: ['Users: Unlimited users', 'Sensors: 10 sensors with alerts', 'Tasks: Task sharing and reminders'],
  },
]


function openModal(planId: number) {
  const selectedPlan = plans.find((p) => p.id === planId)
  form.value.plan = selectedPlan ? selectedPlan.name : ''
  modalVisible.value = true
  errors.value = {}
}

function closeModal() {
  modalVisible.value = false
  form.value = {
    name: '',
    address: '',
    plan: '',
  }
}

//import { cottageService } from '../services/api' // Correct import of default export

async function submitCottage() {
  alert("We have temporarily suspended automatic cottage generation to ensure we provide the best possible service to our current clients. However, we would love to have you! Please contact us at cottagepilot@gmail.com to join our waiting list, and we will do our best to accommodate you as soon as possible.")
  /*try {
    const response = await cottageService.getCottagePaymentLink(form.value.name, form.value.address, form.value.plan)
    console.log(response)
    if (response.payment_link){
      window.location.href = response.payment_link
    } else {
      alert('No payment link received.')
      closeModal()
    }
  } catch (error: any) {
    error.value = error instanceof Error ? error.message : 'Failed to fetch paymentlink'
    console.error(error)
  }*/
  
}
</script>

<style scoped>
/* Add any additional styling if needed */
</style>
