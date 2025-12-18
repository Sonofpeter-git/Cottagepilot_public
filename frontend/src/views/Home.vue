<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { ChartBarIcon, CpuChipIcon, CloudIcon, ShieldCheckIcon } from '@heroicons/vue/24/outline'

const features = [
  {
    name: 'Smart Calendar',
    description: 'Keep track of all your cottage-related activities, from family visits to maintenance tasks, with an easy-to-use calendar designed specifically for seasonal living.',
    icon: CloudIcon,
  },
  {
    name: 'Shared Task List',
    description: 'Organize and assign chores like firewood hauling, cleaning, or water checks – and share them with your cottage users so nothing gets forgotten.',
    icon: ChartBarIcon,
  },
  {
    name: 'Quick Notes',
    description: 'Save important reminders, codes, or shopping lists in one place – accessible anytime, from anywhere.',
    icon: CpuChipIcon,
  },
  {
    name: 'Sensor Integration',
    description: 'Connect temperature, humidity, or motion sensors to monitor your cottage remotely and stay informed about its condition year-round.',
    icon: ShieldCheckIcon,
  },
]
</script>

<template>
  <div class="min-h-screen bg-extraNeutral">
    <!-- Hero Section -->
    <section class="relative py-20 px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-7xl text-center">
        <h1 class="text-4xl sm:text-6xl font-bold text-primary mb-6 animate-fade-in">
          Cottagepilot – Your
          <span class="block gradient-text">Smart Cottage Assistant</span>
        </h1>
        <p class="text-xl text-black mb-8 max-w-3xl mx-auto animate-slide-up">
          Simplify your cottage life with our all-in-one platform.  
          Manage tasks, track visits, and monitor sensors effortlessly — all in real time, wherever you are.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up">
          <RouterLink
            to="/dashboard"
            class="bg-white text-secondary px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-all duration-200 transform hover:scale-105"
          >
            Get Started
          </RouterLink>
          <RouterLink
            to="/about"
            class="border-2 border-borderColor text-secondary px-8 py-3 rounded-lg font-semibold bg-popUpBg hover:bg-white hover:text-primary transition-all duration-200"
          >
            Learn More
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-7xl">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-secondary mb-4">
            Essential Features for Smart Cottage Living
          </h2>
          <p class="text-xl text-secondary max-w-2xl mx-auto">
            Tools to simplify your cottage management — from tasks and notes to real-time sensor monitoring.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div
            v-for="feature in features"
            :key="feature.name"
            class="bg-popUpBg p-6 rounded-xl text-center hover:scale-105 transition-all duration-300"
          >
            <div class="w-12 h-12 mx-auto mb-4 text-secondary">
              <component :is="feature.icon" class="w-full h-full" />
            </div>
            <h3 class="text-xl font-semibold text-secondary mb-2">{{ feature.name }}</h3>
            <p class="text-secondary">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-20 px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-7xl">
        <div class="bg-popUpBg rounded-2xl p-8">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div class="text-4xl font-bold text-secondary mb-2">🇫🇮</div>
              <div class="text-primary/80">Developed in Finland</div>
            </div>
            <div>
              <div class="text-4xl font-bold text-secondary mb-2">99%</div>
              <div class="text-primary/80">Uptime</div>
            </div>
            <div>
              <div class="text-4xl font-bold text-secondary mb-2">24/7</div>
              <div class="text-primary/80">Customer service</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-4xl text-center">
        <h2 class="text-3xl sm:text-4xl font-bold text-secondary mb-6">
          Ready to Simplify Your Cottage Life?
        </h2>
        <p class="text-xl text-secondary mb-8">
          Join countless cottage owners who trust Cottagepilot to organize, monitor, and enhance their getaway experience.
        </p>
        <RouterLink
          to="/pricing"
          class="bg-secondary text-primary px-8 py-4 rounded-lg font-semibold hover:bg-secondary transition-all duration-200 transform hover:scale-105 inline-block"
        >
          View Pricing Plans
        </RouterLink>
      </div>
    </section>
  </div>
</template>
<style>
.gradiant_1{
  background: linear-gradient(135deg, var(--primary-color) 20%,  var(--secondary-color) 100%);
}
.gradiant_2{
  background: linear-gradient(135deg, var(--secondary-color) 40% ,var(--primary-color) 100%);
}
</style>
