<script setup lang="ts">
import { 
  EnvelopeIcon, 
  MapPinIcon,
} from '@heroicons/vue/24/outline'

const contactInfo = [
  {
    icon: EnvelopeIcon,
    title: 'Email Us',
    details: 'cottagepilot@gmail.com',
    description: 'Send us an email and we\'ll respond within 24 hours.'
  },
  /*{
    icon: PhoneIcon,
    title: 'Call Us',
    details: '+358 44',
    description: 'Mon-Fri from 8am to 6pm PST.'
  },*/
  /*{
    icon: MapPinIcon,
    title: 'Visit Us',
    details: '123 Tech Street, San Francisco, CA 94105',
    description: 'Come visit our headquarters in downtown SF.'
  },
  {
    icon: ChatBubbleLeftRightIcon,
    title: 'Live Chat',
    details: 'Available 24/7',
    description: 'Get instant help from our support team.'
  }*/
]
</script>

<template>
  <div class="min-h-screen py-16 px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-7xl">
      <!-- Header -->
      <div class="text-center mb-16">
        <h1 class="text-4xl sm:text-5xl font-bold text-secondary mb-6">
          Get in Touch
        </h1>
        <p class="text-xl text-secondary/80 max-w-3xl mx-auto">
          Have questions about SensorHub? We'd love to hear from you. 
          Send us a message and we'll respond as soon as possible.
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-1 gap-12">
        
        <!-- Contact Information -->
        <div class="space-y-8">
          <div
            v-for="info in contactInfo"
            :key="info.title"
            class="bg-popUpBg rounded-lg p-6 hover:scale-105 transition-all duration-300 text-secondary"
          >
            <div class="flex items-start gap-4 rounded-md">
              <div class="p-3 bg-secondary-500/20 rounded-lg">
                <component :is="info.icon" class="w-6 h-6 text-secondary-400" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-secondary mb-2">{{ info.title }}</h3>
                <p class="text-secondary-400 font-medium mb-1">{{ info.details }}</p>
                <p class="text-secondary/70 text-sm">{{ info.description }}</p>
              </div>
            </div>
          </div>

          <!-- Map placeholder -->
          <div class="rounded-lg p-6 rounded-md bg-popUpBg">
            <h3 class="text-lg font-semibold text-secondary mb-4">Our Location</h3>
            <div class="aspect-video bg-secondary/10 rounded-lg flex items-center justify-center">
              <div class="text-center">
                <MapPinIcon class="w-12 h-12 text-secondary/40 mx-auto mb-2" />
                <p class="text-secondary/60">Interactive map coming soon</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- FAQ Section -->
      <div class="mt-16 rounded-md p-8">
        <h2 class="text-3xl font-bold text-secondary text-center mb-12">
          Frequently Asked Questions
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 class="text-lg font-semibold text-secondary mb-3">
              How quickly do you respond to inquiries?
            </h3>
            <p class="text-secondary/70">
              We typically respond to all inquiries within 24 hours during business days. 
              For urgent technical issues, we offer 24/7 support for enterprise customers.
            </p>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-secondary mb-3">
              Can I schedule a demo?
            </h3>
            <p class="text-secondary/70">
              Absolutely! Send us an email and lets schedule that demo for you.
            </p>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-secondary mb-3">
              Do you offer technical support?
            </h3>
            <p class="text-secondary/70">
              Yes, we provide comprehensive technical support including documentation, 
              video tutorials, and direct support from our engineering team.
            </p>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-secondary mb-3">
              What about partnership opportunities?
            </h3>
            <p class="text-secondary/70">
              We're always interested in strategic partnerships. Contact us to discuss 
              integration opportunities, reseller programs, and technology partnerships.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>