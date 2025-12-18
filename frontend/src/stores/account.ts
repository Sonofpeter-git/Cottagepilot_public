import { defineStore } from 'pinia'
import { ref, computed, nextTick } from 'vue'
import type { Account } from '../types'
import { accountService } from '../services/api' // Correct import of default export
import { useRouter } from 'vue-router'

export const useAccountStore = defineStore('account', () => {
  const account = ref<Account | null>(null)
  const userLoggedIn = ref(false)
  const authToken = ref('')
  const loading = ref(false)
  const error = ref<string | null>(null)
  const router = useRouter()

  const isUserAuthenticated = computed(() => {
    if (localStorage.getItem('auth_token')  || userLoggedIn.value){
      return  true
    } else {
      return false
     }
    })

  async function login(username: string, password: string) {
    loading.value = true;
    const csrf = await accountService.get_csrf()
    localStorage.setItem('csrf', csrf)

    const response = await accountService.login(username, password)
    await updateAuthVariables(response.token, response.cottageInstanceActive)
    account.value = response.account
    loading.value = false;
    nextTick(() => {
      router.push('/choose-cottage/')
    });
    return true
  }

  function updateAuthVariables(token:string, cottageInstanceActive:string){
    localStorage.setItem('auth_token', token)
    userLoggedIn.value = true
    localStorage.setItem('cottageInstanceActive', cottageInstanceActive)
    authToken.value = token

    
  }

  async function fetchAccount() {
    loading.value = true
    error.value = null
    try {
      account.value = await accountService.getAccount() // Call the function to get the Promise resolved
      return account.value
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch account'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  async function fetchCottageUsers() {
    loading.value = true
    error.value = null
    try {
      return await accountService.fetchCottageUsers() // Call the function to get the Promise resolved
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch account'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  async function updateAccount(updates: Partial<Account>) {
    loading.value = true
    error.value = null
    try {
      if (!account.value) throw new Error('No account loaded')
      account.value = await accountService.updateAccount(updates)
      return account.value
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update account'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /*async function changePassword(oldPwd: string, newPwd: string) {
    loading.value = true
    error.value = null
    try {
      const result = await accountService.changePassword(oldPwd, newPwd)
      return result
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to change password'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }*/

  function clearAccount() {
    account.value = null
  }

  function logout() {
    clearAccount()
    localStorage.removeItem('auth_token')
    localStorage.removeItem('csrf')
    localStorage.removeItem('cottageInstanceActive')
    window.location.href = '/login'
  }

  return {
    account,
    loading,
    error,
    userLoggedIn,
    authToken,
    fetchAccount,
    fetchCottageUsers,
    clearAccount,
    updateAccount,
    logout,
    login,
    updateAuthVariables,
    isUserAuthenticated,
  }
})
