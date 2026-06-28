<script setup lang="ts">
import { reactive, ref } from 'vue'

defineProps<{
  msg: string
}>()

const form = reactive({
  name: '',
  email: '',
  message: '',
})

const submitted = ref(false)

function submitForm() {
  submitted.value = true
}
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <p class="intro">This is a simple form added to the starter Vue component.</p>

    <form class="contact-form" @submit.prevent="submitForm">
      <label>
        <span>Name</span>
        <input v-model="form.name" type="text" required />
      </label>

      <label>
        <span>Email</span>
        <input v-model="form.email" type="email" required />
      </label>

      <label>
        <span>Message</span>
        <textarea v-model="form.message" rows="4" required />
      </label>

      <button type="submit">Submit</button>
    </form>

    <p v-if="submitted" class="success">Thanks, {{ form.name || 'friend' }}! Your message has been received.</p>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

.intro {
  margin-bottom: 1rem;
  color: #4b5563;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 420px;
  margin: 0 auto;
  text-align: left;
}

.contact-form label {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-weight: 600;
  color: #374151;
}

.contact-form input,
.contact-form textarea {
  padding: 0.7rem 0.8rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font: inherit;
}

.contact-form button {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  background-color: #42b883;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.success {
  margin-top: 1rem;
  color: #047857;
  font-weight: 600;
}

.greetings h1,
.greetings p {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings p {
    text-align: left;
  }
}
</style>
