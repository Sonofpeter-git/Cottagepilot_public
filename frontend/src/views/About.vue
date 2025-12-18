<script setup lang="ts">
import { CheckIcon } from '@heroicons/vue/24/outline'

const features = [
  'Real-time sensor monitoring and data collection',
  'Advanced analytics',
  'Scalable cloud infrastructure with 99% uptime',
  'Mobile-responsive web interface',
  '24/7 technical support and monitoring'
]

const team = [
  {
    name: 'Niklas Pettersson',
    role: 'Sole Founder & CEO, CottagePilot.',
    image: 'https://media.licdn.com/dms/image/v2/D4D03AQFB7wP5ZaGoFg/profile-displayphoto-scale_200_200/B4DZsjVqrDHkAY-/0/1765824443167?e=1767830400&v=beta&t=6zKIFW_Ad9GJvTrKQAmDXjGCHLw97vjW1C9RO9KWB6I',
    bio: 'Sole founder of CottagePilot, with 3+ years of full-stack development experience. Passionate about building practical, user-focused tech solutions and driving early-stage products from idea to launch.'
  },
]
</script>

<template>
  <div class="min-h-screen py-16 px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-7xl">
      <!-- Hero Section -->
      <div class="text-center mb-16">
        <h1 class="text-4xl sm:text-5xl font-bold text-secondary mb-6">
          About SensorHub
        </h1>
        <p class="text-xl text-secondary/80 max-w-3xl mx-auto">
          We're revolutionizing IoT sensor management with cutting-edge technology, 
          making it easier than ever to monitor, analyze, and optimize your connected devices.
        </p>
      </div>

      <!-- Mission Section -->
      <div class="glass-effect rounded-2xl p-8 mb-16">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 class="text-3xl font-bold text-secondary mb-6">Our Mission</h2>
            <p class="text-secondary/80 mb-6">
              To democratize IoT sensor management by providing an intuitive, powerful platform 
              that enables businesses of all sizes to harness the full potential of their sensor data.
            </p>
            <p class="text-secondary/80">
              We believe that every organization should have access to enterprise-grade IoT 
              monitoring capabilities without the complexity and cost traditionally associated 
              with such systems.
            </p>
          </div>
          <div class="relative">
            <img
              src="https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg?auto=compress&cs=tinysrgb&w=800"
              alt="Mission"
              class="rounded-lg shadow-2xl"
            />
          </div>
        </div>
      </div>

      <!-- Features Section -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-secondary text-center mb-12">
          What Makes Us Different
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div
            v-for="feature in features"
            :key="feature"
            class="flex items-start gap-3 glass-effect p-6 rounded-lg"
          >
            <CheckIcon class="w-6 h-6 text-green-400 flex-shrink-0 mt-1" />
            <span class="text-secondary/80">{{ feature }}</span>
          </div>
        </div>
      </div>

      <!-- Team Section -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-secondary text-center mb-12">
          Meet Our Team
        </h2>
        <div class="grid-cols-1 md:grid-cols-3 gap-8">
          <div
            v-for="member in team"
            :key="member.name"
            class="glass-effect rounded-lg p-6 text-center"
          >
            <img
              :src="member.image"
              :alt="member.name"
              class="w-24 h-24 rounded-full mx-auto mb-4 object-cover"
            />
            <h3 class="text-xl font-semibold text-secondary mb-2">{{ member.name }}</h3>
            <p class="text-secondary-400 font-medium mb-3">{{ member.role }}</p>
            <p class="text-secondary/70 text-sm">{{ member.bio }}</p>
          </div>
        </div>
      </div>

      <!-- Values Section -->
      <div class="glass-effect rounded-2xl p-8">
        <h2 class="text-3xl font-bold text-secondary text-center mb-12">Our Values</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="w-16 h-16 bg-secondary-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-2xl">🚀</span>
            </div>
            <h3 class="text-xl font-semibold text-secondary mb-3">Innovation</h3>
            <p class="text-secondary/70">
              We continuously push the boundaries of what's possible in IoT technology.
            </p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-secondary-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-2xl">🤝</span>
            </div>
            <h3 class="text-xl font-semibold text-secondary mb-3">Reliability</h3>
            <p class="text-secondary/70">
              Our platform is built for mission-critical applications with 99% uptime.
            </p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-yellow-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-2xl">💡</span>
            </div>
            <h3 class="text-xl font-semibold text-secondary mb-3">Simplicity</h3>
            <p class="text-secondary/70">
              Complex technology made simple and accessible for everyone.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>