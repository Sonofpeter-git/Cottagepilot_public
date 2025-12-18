<script setup lang="ts">
type Testimonial = {
  name: string;
  role: string;
  company: string;
  image: string;
  content: string;
  rating: number;
};

const testimonials: Testimonial[] = [
    {
      name: 'David Thompson',
      role: 'CTO, TechCorp Industries',
      company: 'TechCorp Industries',
      image: 'https://images.pexels.com/photos/1043471/pexels-photo-1043471.jpeg?auto=compress&cs=tinysrgb&w=400',
      content: 'SensorHub has transformed how we monitor our manufacturing equipment. The real-time alerts have prevented multiple costly breakdowns.',
      rating: 5
    },
    {
      name: 'Maria Garcia',
      role: 'Operations Manager',
      company: 'Smart Buildings Co.',
      image: 'https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=400',
      content: 'The analytics dashboard gives us insights we never had before. We\'ve reduced energy costs by 30% since implementing SensorHub.',
      rating: 5
    },
    {
      name: 'James Wilson',
      role: 'Research Director',
      company: 'AgriTech Solutions',
      image: 'https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=400',
      content: 'Perfect for our agricultural monitoring needs. The platform scales beautifully from small greenhouses to large farm operations.',
      rating: 5
    },
    {
      name: 'Lisa Chen',
      role: 'Facility Manager',
      company: 'Metro Hospital',
      image: 'https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=400',
      content: 'Critical for maintaining optimal conditions in our medical facilities. The reliability and accuracy are exactly what we needed.',
      rating: 5
    },
    {
      name: 'Robert Kim',
      role: 'Environmental Engineer',
      company: 'EcoMonitor Inc.',
      image: 'https://images.pexels.com/photos/1043474/pexels-photo-1043474.jpeg?auto=compress&cs=tinysrgb&w=400',
      content: 'Excellent platform for environmental monitoring. The data visualization tools help us identify trends and patterns quickly.',
      rating: 5
    },
    {
      name: 'Sarah Johnson',
      role: 'IT Director',
      company: 'Global Logistics',
      image: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=400',
      content: 'Integration was seamless and the support team is outstanding. We\'re monitoring thousands of sensors across multiple locations.',
      rating: 5
    }
  ]


const stats = [
  /*{ value: '500+', label: 'Happy Customers' },
  { value: '10,000+', label: 'Sensors Monitored' },*/
  { value: '99%', label: 'Uptime' },
  { value: '24/7', label: 'Support' }
]
</script>

<template>
  <div class="min-h-screen py-16 px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-7xl">
      <!-- Header -->
      <div class="text-center mb-16">
        <h1 class="text-4xl sm:text-5xl font-bold text-secondary mb-6">
          What Our Customers Say
        </h1>
        <p class="text-xl text-secondary/80 max-w-3xl mx-auto">
          Don't just take our word for it. Here's what industry leaders are saying about SensorHub.
        </p>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-2 md:grid-cols-2 gap-8 mb-16">
        <div
          v-for="stat in stats"
          :key="stat.label"
          class="text-center"
        >
          <div class="text-3xl sm:text-4xl font-bold text-secondary mb-2">{{ stat.value }}</div>
          <div class="text-secondary/70">{{ stat.label }}</div>
        </div>
      </div>

      <!-- Testimonials Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
        <div
          v-for="testimonial in testimonials"
          :key="testimonial.name"
          class="glass-effect rounded-lg p-6 hover:scale-105 transition-all duration-300"
        >
          <!-- Rating -->
          <div class="flex mb-4">
            <span
              v-for="i in testimonial.rating"
              :key="i"
              class="text-yellow-400 text-lg"
            >
              ★
            </span>
          </div>

          <!-- Content -->
          <blockquote class="text-secondary/80 mb-6">
            "{{ testimonial.content }}"
          </blockquote>

          <!-- Author -->
          <div class="flex items-center gap-4">
            <img
              :src="testimonial.image"
              :alt="testimonial.name"
              class="w-12 h-12 rounded-full object-cover"
            />
            <div>
              <div class="font-semibold text-secondary">{{ testimonial.name }}</div>
              <div class="text-sm text-secondary/60">{{ testimonial.role }}</div>
              <div class="text-sm text-primary-400">{{ testimonial.company }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- CTA Section -->
      <div class="glass-effect rounded-2xl p-8 text-center">
        <h2 class="text-3xl font-bold text-secondary mb-4">
          Ready to Join Our Success Stories?
        </h2>
        <p class="text-secondary/80 mb-8 max-w-2xl mx-auto">
          Start your free trial today and see why thousands of companies trust SensorHub 
          for their IoT monitoring needs.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button class="bg-primary-600 text-secondary border-2 border-secondary px-8 py-3 rounded-lg font-semibold hover:bg-white transition-colors">
            Start Free Trial
          </button>
          <button class="border-2 border-secondary text-secondary px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary-600 transition-colors">
            Schedule Demo
          </button>
        </div>
      </div>
    </div>
  </div>
</template>