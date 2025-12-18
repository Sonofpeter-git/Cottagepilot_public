<template>
  <div class="min-h-screen text-secondary bg-extraNeutral">
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-primary to-secondary text-secondary py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl text-primary md:text-6xl font-bold mb-6">
            CottagePilot Blog
          </h1>
          <p class="text-xl md:text-2xl mb-8 text-secondary max-w-3xl mx-auto">
            Expert insights on smart cottage management, vacation rental optimization, and sustainable living
          </p>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <section class="py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid gap-8 lg:grid-cols-3">
          <!-- Featured Post -->
          <div class="lg:col-span-2 ">
            <article class="bg-popUpBg rounded-lg shadow-lg overflow-hidden">
              <a href="/blogs/smart-cottage/">
                <img 
                  src="https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=400&fit=crop" 
                  alt="Smart cottage management"
                  class="w-full h-64 object-cover"
                >
                <div class="p-6">
                  <div class="flex items-center mb-2">
                    <span class="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">Featured</span>
                    <span class="text-gray-500 text-sm ml-2">5 min read</span>
                  </div>
                  <h2 class="text-2xl font-bold text-gray-900 mb-3">
                    How to Turn Your Cabin into a Smart Home: The Ultimate Guide to Remote Cottage Management
                  </h2>
                  <p class="text-gray-600 mb-4">
                    Tired of wondering what's happening at your remote cottage while you're away? Learn how to turn your traditional cabin into a smart, connected sanctuary—where leaks, mold, and maintenance surprises are a thing of the past. With the right tech (and one powerful dashboard), managing your getaway has never been this easy. 🔧📡✨
                  </p>
                </div>
              </a>
            </article>
          </div>

          <!-- Sidebar -->
          <div class="space-y-6">
            <!-- Search -->
            <div class="bg-popUpBg rounded-lg shadow p-6">
              <h3 class="text-lg font-semibold mb-4">Search Articles</h3>
              <input 
                type="text" 
                placeholder="Search tips..."
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              >
            </div>

            <!-- Categories -->
            <div class="bg-popUpBg rounded-lg shadow p-6">
              <h3 class="text-lg font-semibold mb-4">Categories</h3>
              <div class="space-y-2">
                <button class="w-full text-left px-3 py-2 text-sm bg-gray-100 rounded hover:bg-blue-100">
                  Smart Home
                </button>
                <button class="w-full text-left px-3 py-2 text-sm bg-gray-100 rounded hover:bg-blue-100">
                  Maintenance
                </button>
                <button class="w-full text-left px-3 py-2 text-sm bg-gray-100 rounded hover:bg-blue-100">
                  Rental Tips
                </button>
                <button class="w-full text-left px-3 py-2 text-sm bg-gray-100 rounded hover:bg-blue-100">
                  Sustainability
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- All Posts Grid -->
        <div class="mt-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-8">All Articles</h2>
          <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <a 
              v-for="post in posts" 
              :href="post.href"
              :key="post.id"
              class="bg-popUpBg rounded-lg shadow hover:shadow-lg transition-shadow"
            >
              <img :src="post.image" :alt="post.title" class="w-full h-48 object-cover">
              <div class="p-6">
                <div class="flex items-center mb-2">
                  <span class="bg-teal-100 text-teal-800 text-xs font-medium px-2.5 py-0.5 rounded">{{ post.category }}</span>
                  <span class="text-gray-500 text-sm ml-2">{{ post.readTime }}</span>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ post.title }}</h3>
                <p class="text-gray-600 text-sm mb-4">{{ post.excerpt }}</p>
              </div>
            </a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';

interface Author {
  name: string;
  avatar: string;
}

interface BlogPost {
  id: number;
  title: string;
  excerpt: string;
  category: string;
  readTime: string;
  image: string;
  author: Author;
  slug: string;
  href: string;
}

export default defineComponent({
  name: 'Blogs',
  setup() {
    const searchQuery = ref('');
    const selectedCategory = ref('All');

    const categories = ref(['All', 'Management', 'Technology', 'Sustainability', 'Tips']);

    const posts = ref<BlogPost[]>([
      {
        id: 1,
        title: 'How to Turn Your Cabin into a Smart Home: The Ultimate Guide to Remote Cottage Management',
        excerpt: "Tired of wondering what's happening at your remote cottage while you're away? Learn how to turn your traditional cabin into a smart, connected sanctuary—where leaks, mold, and maintenance surprises are a thing of the past. With the right tech (and one powerful dashboard), managing your getaway has never been this easy. 🔧📡✨",
        category: 'Management',
        readTime: '5 min read',
        image: 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=400&fit=crop',
        author: {
          name: '',
          avatar: '',
        },
        slug: 'essential-cottage-management-tips',
        href: '/blogs/smart-cottage/'
      },
      {
        id: 2,
        title: 'How Smart Home Automation Can Save You Time and Money',
        excerpt: 'Explore the benefits of integrating smart home devices into your cottage to automate routine tasks and improve energy efficiency.',
        category: 'Technology',
        readTime: '6 min read',
        image: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&h=400&fit=crop',
        author: {
          name: '',
          avatar: '',
        },
        slug: 'smart-home-automation-benefits',
        href: '/blogs/automation-saves-time/'
      },
    ]);

    const filteredPosts = computed(() => {
      return posts.value.filter(post => {
        const matchesCategory = selectedCategory.value === 'All' || post.category === selectedCategory.value;
        const matchesSearch = post.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || post.excerpt.toLowerCase().includes(searchQuery.value.toLowerCase());
        return matchesCategory && matchesSearch;
      });
    });

    return {
      searchQuery,
      selectedCategory,
      categories,
      filteredPosts,
      posts
    };
  },
});
</script>

<style scoped>
/* Add any additional styles here if needed */
</style>
