<script setup lang="ts">
import CalendarComponent from '../components/calendar/calendarComponent.vue'
</script>

<template>
  <div class="min-h-screen py-8 px-4 sm:px-6 lg:px-8 text-secondary">
        <div class="mx-auto max-w-7xl">
          <div class="mb-8">
            <h1 class="text-3xl font-bold text-secondary mb-3">Calendar Dashboard</h1>
            <p class="text-secondary">View your scheduled events and reservations at a glance.</p>
          </div>
          <div class="p-5 rounded-md bg-popUpBg">
            <CalendarComponent></CalendarComponent>
          </div>
        </div>
      </div>
</template>
