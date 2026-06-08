<script setup lang="ts">
import { reactive, ref } from "vue"
import { createSupplier } from "@/testapi/supplierTestApi"

const loading = ref(false)
const successMessage = ref("")
const errorMessage = ref("")

const form = reactive({
  supplier_name_cn: "",
  supplier_name_en: "",
  contact_person: "",
  phone: "",
  email: "",
  address: "",
})

async function handleSubmit() {
  successMessage.value = ""
  errorMessage.value = ""

  if (!form.supplier_name_cn.trim()) {
    errorMessage.value = "Supplier Chinese name is required."
    return
  }

  loading.value = true

  try {
    const payload = {
      supplier_name_cn: form.supplier_name_cn.trim(),
      supplier_name_en: form.supplier_name_en.trim() || undefined,
      contact_person: form.contact_person.trim() || undefined,
      phone: form.phone.trim() || undefined,
      email: form.email.trim() || undefined,
      address: form.address.trim() || undefined,
    }

    const result = await createSupplier(payload)

    successMessage.value = `Supplier created successfully. ID: ${result.id ?? ""}`

    form.supplier_name_cn = ""
    form.supplier_name_en = ""
    form.contact_person = ""
    form.phone = ""
    form.email = ""
    form.address = ""
  } catch (error: any) {
    errorMessage.value =
      error.response?.data?.detail || "Failed to create supplier."
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="page">
    <section class="card">
      <h1>Supplier Registration</h1>

      <form @submit.prevent="handleSubmit" class="form">
        <div class="form-item">
          <label>Supplier Name CN *</label>
          <input v-model="form.supplier_name_cn" type="text" />
        </div>

        <div class="form-item">
          <label>Supplier Name EN</label>
          <input v-model="form.supplier_name_en" type="text" />
        </div>

        <div class="form-item">
          <label>Contact Person</label>
          <input v-model="form.contact_person" type="text" />
        </div>

        <div class="form-item">
          <label>Phone</label>
          <input v-model="form.phone" type="text" />
        </div>

        <div class="form-item">
          <label>Email</label>
          <input v-model="form.email" type="email" />
        </div>

        <div class="form-item">
          <label>Address</label>
          <textarea v-model="form.address" rows="3"></textarea>
        </div>

        <button type="submit" :disabled="loading">
          {{ loading ? "Submitting..." : "Create Supplier" }}
        </button>
      </form>

      <p v-if="successMessage" class="success">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </section>
  </main>
</template>

<style scoped>
.page {
  min-height: 100vh;
  padding: 40px;
  background: #f5f7fa;
}

.card {
  max-width: 640px;
  margin: 0 auto;
  padding: 32px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

h1 {
  margin-bottom: 24px;
  font-size: 24px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-size: 14px;
  font-weight: 600;
}

input,
textarea {
  padding: 10px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  font-size: 14px;
}

button {
  margin-top: 8px;
  padding: 12px 16px;
  border: none;
  border-radius: 6px;
  background: #27556e;
  color: white;
  font-size: 15px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.success {
  margin-top: 16px;
  color: #1f8f4d;
}

.error {
  margin-top: 16px;
  color: #d93025;
}
</style>