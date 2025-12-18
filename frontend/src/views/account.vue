<script lang="ts">
import { defineComponent, reactive, ref, onMounted } from 'vue';
import { useAccountStore } from '../stores/account';
import { api } from '../services/api';

export default defineComponent({
  name: 'Account',
  setup() {
    const accountStore = useAccountStore()
    const user = ref()
    const cottage = ref()

    const passwordForm = reactive({
      old_password: '',
      new_password: '',
    });

    const message = ref('');
    const success = ref(false);
    const errors = ref<{ [key: string]: string[] }>({})

    const fetchProfiles = async () => {
      try {
        user.value = await accountStore.fetchAccount()

      } catch (error) {
        message.value = 'Failed to load profiles.';
        success.value = false;
      }

      try {
        const response = await api.get('/cottage/me/')
        cottage.value = response.data.results 
      } catch (error) {
        message.value = 'Failed to load cottage.';
        success.value = false;
      }
    };


    const updateProfile = async () => {
      try {
        user.value = await accountStore.updateAccount(user.value)
        
        message.value = 'Profile updated successfully.';
        success.value = true;
      } catch (error) {
        message.value = 'Failed to update profile.';
        success.value = false;
      }
    };

    const changePassword = async () => {
      try {
        const response = await api.post('/account/change-password/', {
          old_password: passwordForm.old_password,
          new_password: passwordForm.new_password,
        })

        if (response.data.status == 'true'){
          passwordForm.old_password = ''
          passwordForm.new_password = ''
          
          success.value = true;
          message.value = 'Password changed.';
        } else {
          errors.value = response.data.errors ?? {}
        }

      } catch (error) {
        message.value = 'Failed to change password.';
        success.value = false;
      }
    };

    const logout = async () => {
      accountStore.logout()
    }

    onMounted(() => {
      fetchProfiles();

    });

    return {
      user,
      passwordForm,
      message,
      success,
      errors,
      cottage,
      updateProfile,
      changePassword,
      logout,
    };
  },
});
</script>

<style scoped>
</style>

<template>
  <div class="max-w-3xl mx-auto p-4">
    <div v-if="user">
      <h1 class="text-2xl font-bold mb-4 text-secondary text-Title-font text-center mt-5">My account: {{user.username}}</h1>
      <form @submit.prevent="updateProfile" class="rounded-2xl p-8 rounded-md bg-popUpBg">
        <div class="mb-4">
          <label class="block mb-1 font-semibold text-secondary" for="username">Username</label>
          <input v-model="user.username" id="username" type="text" class="w-full rounded px-3 py-2 bg-secondary/10 text-secondary bg-popUpBg" />
        </div>
        <div class="mb-4">
          <label class="block mb-1 font-semibold text-secondary" for="email">Email</label>
          <input v-model="user.email" id="email" type="email" class="w-full rounded px-3 py-2 bg-secondary/10 text-secondary bg-popUpBg" />
        </div>
        <div class="mb-4">
          <label class="block mb-1 font-semibold text-secondary" for="first_name">First Name</label>
          <input v-model="user.first_name" id="first_name" type="text" class="w-full rounded px-3 py-2 bg-secondary/10 text-secondary bg-popUpBg" />
        </div>
        <div class="mb-4">
          <label class="block mb-1 font-semibold text-secondary" for="last_name">Last Name</label>
          <input v-model="user.last_name" id="last_name" type="text" class="w-full rounded px-3 py-2 bg-secondary/10 text-secondary bg-popUpBg" />
        </div>
        <button type="submit" class="text-secondary px-4 py-2 rounded hover:font-bold border-secondary border rounded">Update Profile</button>
      </form>
      <h2 class="text-xl text-secondary font-bold mt-8 mb-4">Change Password</h2>
      <form @submit.prevent="changePassword" class="rounded-2xl p-8 rounded-md bg-popUpBg">
        <div class="mb-4">
          <label class="block mb-1 font-semibold text-secondary" for="old_password">Old Password</label>
          <input v-model="passwordForm.old_password" id="old_password" autocomplete="current-password" type="password" class="w-full rounded px-3 py-2 bg-secondary/10 text-secondary bg-popUpBg" />
          <p v-if="errors.old_password" class="text-red-600 text-sm mt-1" v-for="(err, idx) in errors.old_password" :key="idx">{{ err }}</p>
        </div>
        <div class="mb-4">
          <label class="block mb-1 font-semibold text-secondary" for="new_password">New Password</label>
          <input v-model="passwordForm.new_password" id="new_password" autocomplete="new-password" type="password" class="w-full  rounded px-3 py-2 bg-secondary/10 text-secondary bg-popUpBg" />
          <p v-if="errors.new_password" class="text-red-600 text-sm mt-1" v-for="(err, idx) in errors.new_password" :key="idx">{{ err }}</p>
        </div>
        <button type="submit" class="text-secondary px-4 py-2 rounded hover:font-bold border-secondary border rounded">Change Password</button>
      </form>
      
      <div class="rounded-2xl p-8 mt-6 rounded-md bg-popUpBg">
        <div v-if="cottage">
          <div class="flex items-center">
            <label 
              class="block mb-1 font-semibold text-secondary w-full" 
              for="new_password"
            >
              Active Cottage:
            </label>
            
            <router-link 
              to="/choose-cottage" 
              class="font-semibold text-blue-500 hover:text-blue-700 ml-auto"
            >
              Change cottage
            </router-link>
        </div>
          <p class="text-secondary font-semibold flex">Name: <p class="pl-2 font-normal">{{ cottage.name }}</p></p>
          <p class="text-secondary font-semibold flex">Address: <p class="pl-2 font-normal">{{ cottage.address }}</p></p>
          <p class="text-secondary font-semibold flex">Owner: <p class="pl-2 font-normal">{{ cottage.ownerUsername }}</p></p>
          <p class="text-secondary font-semibold flex">Subscription: <p class="pl-2 font-normal">{{ cottage.stripe_subscription }}</p></p>
          <p class="text-secondary font-semibold flex">Subscription paid: <p class="pl-2 font-normal">{{ cottage.stripe_payment_status_int == 1 ? 'Yes' : 'No' }}</p></p>
          <div v-if="user.username == cottage.ownerUsername">
            <p class="text-secondary font-semibold flex">Invite members to cottage: <router-link 
              to="/invite-members-to-cottage" 
              class="text-semibold text-blue-500 hover:text-blue-700 pl-3"
            >
              Invite
            </router-link>
            </p>
          </div>
          <div v-else>
            <p class="text-secondary font-semibold flex">Only cottage owners can invite new members to cottage</p>
          </div>
          <p class="text-secondary pt-5">If you wish to change/cancel your subscription please contact cottagepilot@gmail.com</p>
          </div>
        <div v-else>
          <label 
              class="block mb-1 font-semibold text-secondary w-full" 
              for="new_password"
            >
              Active Cottage:
            </label>
          <p class="text-secondary pt-5">You dont have an active cottage in your profile. Please choose one:           <router-link 
            to="/choose-cottage" 
            class="font-semibold text-blue-500 hover:text-blue-700 ml-auto"
          >
            Change cottage
          </router-link></p>
        </div>  
        </div>
        <button @click="logout()" class="text-white rounded-2xl p-3 bg-highlight m-3 ml-0 border-2 border-highlight rounded hover:text-highlight hover:bg-transparent">Logout</button>
      <div v-if="message" class="mt-4 p-3 rounded" :class="{'bg-green-200 text-green-800': success, 'bg-red-200 text-red-800': !success}">
        {{ message }}
      </div>
    </div>
    <div v-else>
      <h2>No account found</h2>
    </div>
  </div>  
</template>