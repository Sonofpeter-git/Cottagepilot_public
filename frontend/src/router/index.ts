import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Pricing from '../views/Pricing.vue'
//import Testimonials from '../views/Testimonials.vue'
import Story from '../views/Story.vue'
import SensorData from '../views/SensorData.vue'
import Dashboard from '../views/Sensor-Dashboard.vue'
import Contact from '../views/Contact.vue'
import Login from '../views/Login.vue'
import TaskList from '../views/Tasks.vue'
import TaskDetails from '../views/TaskDetails.vue'
import Account from '../views/account.vue'
import ManageSensors from '../views/manage-sensors.vue'
import notekeeping from '../views/notekeeping.vue'
import calendar from '../views/calendar.vue'
import HomeDashboard from '../views/HomeDashboard.vue'
import AddOrCreateCottage from '../views/AddOrCreateCottage.vue'
import PasswordResetForm from '../views/password_reset/PasswordResetForm.vue'
import PasswordResetRequest from '../views/password_reset/PasswordResetRequest.vue'
import inviteMembersToCottage from '../views/InviteMembersToCottage.vue'
import chooseCottage from '../views/chooseCottage.vue'
import privacyPolicy from '../views/policies/privacyPolicy.vue'
import termsOfService from '../views/policies/termsOfService.vue'
import refundPolicy from '../views/policies/refundPolicy.vue'
import blogs from '../views/blogs/blogs.vue'
import smart_cottage from '../views/blogs/smart_cottage.vue'
import Automation_saves_time from '../views/blogs/Automation_saves_time.vue'

import { useAccountStore } from '../stores/account'
//!ADD AUTHENTICATION TO ROUTER

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    //blogs
    {
      path: '/blogs/',
      name: 'blogs',
      component: blogs
    },
    {
      path: '/blogs/smart-cottage/',
      name: 'smart_cottage',
      component: smart_cottage
    },
    {
      path: '/blogs/automation-saves-time/',
      name: 'blogs/automation-saves-time',
      component: Automation_saves_time
    },
    //Before Cottage
    {
      path: '/add-or-create-cottage/',
      name: 'add-or-create-cottage',
      component: AddOrCreateCottage,
      meta: { requiresAuth: true }
    },
    {
      path: '/choose-cottage/',
      name: 'chooseCottage',
      component: chooseCottage,
      meta: { requiresAuth: true }
    },


    {
      path: '/dashboard/',
      name: 'Dashboard',
      component: HomeDashboard,
      meta: { requiresAuth: true, isCottageRequired: true }
    },
    {
      path: '/about/',
      name: 'About',
      component: About
    },
    {
      path: '/pricing/',
      name: 'Pricing',
      component: Pricing
    },
    /*{
      path: '/testimonials',
      name: 'Testimonials',
      component: Testimonials
    },*/
    {
      path: '/story/',
      name: 'Story',
      component: Story
    },
    {
      path: '/sensor-data/:id?/',
      name: 'SensorData',
      component: SensorData,
      props: true,
      meta: { requiresAuth: true, isCottageRequired: true }
    },
    {
      path: '/sensor-dashboard/',
      name: 'sensor-dashboard',
      component: Dashboard,
      meta: { requiresAuth: true, isCottageRequired: true }
    },
    {
      path: '/manage-sensors/',
      name: 'manage-sensors',
      component: ManageSensors,
      meta: { requiresAuth: true, isCottageRequired: true }
    },
    {
      path: '/contact/',
      name: 'Contact',
      component: Contact
    },
    {
      path: '/login/',
      name: 'Login',
      component: Login
    },
    {
      path: '/task-list/',
      name: 'task-list',
      component: TaskList,
      meta: { requiresAuth: true, isCottageRequired: true }
    },
    {
      path: '/task/:id/',
      name: 'taskDetails',
      component: TaskDetails,
      meta: { requiresAuth: true, isCottageRequired: true }
    },
    {
      path: '/account/',
      name: 'account',
      component: Account,
      meta: { requiresAuth: true }
    },
    {
      path: '/notes/',
      name: 'notes',
      component: notekeeping,
      meta: { requiresAuth: true, isCottageRequired: true }
    },
    {
      path: '/calendar/',
      name: 'calendar',
      component: calendar,
      meta: { requiresAuth: true, isCottageRequired: true }
    },
    //Password_reset
    {
      path: '/forgot-password/',
      name: 'PasswordResetRequest',
      component: PasswordResetRequest,
    },
    {
      path: '/reset-password/:uid/:token',
      name: 'PasswordResetForm',
      component: PasswordResetForm,
    },

    //Invite membersToCottage
    {
      path: '/invite-members-to-cottage/',
      name: 'invite-members-to-cottage',
      component: inviteMembersToCottage,
    },

    //Policies
    {
      path: '/privacy-policy/',
      name: 'privacy-policy',
      component: privacyPolicy,
    },
    {
      path: '/terms-of-service/',
      name: 'terms-of-service',
      component: termsOfService,
    },
    {
      path: '/refund-policy/',
      name: 'refund-policy',
      component: refundPolicy,
    },
  ],
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

router.beforeEach((to, _from, next) => {
  const accountStore = useAccountStore();
  const isAuthRequired = to.meta.requiresAuth;
  const isCottageRequired = to.meta.isCottageRequired;
  const cottageActive = localStorage.getItem('cottageInstanceActive') === 'true';

  if (isAuthRequired && !accountStore.isUserAuthenticated) {
    return next({ name: 'Login' });
  }


  if (isCottageRequired) {
    if (cottageActive == false) {
      return next({ name: 'chooseCottage' });
    }
  }

  return next(); // Proceed to the route
});


export default router
