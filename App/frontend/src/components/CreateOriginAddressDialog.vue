<template>
  <el-dialog
    v-model="dialogVisible"
    title="New Origin Address"
    width="680px"
    :close-on-click-modal="false"
    @closed="resetForm"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="150px"
      label-position="right"
    >
      <el-form-item label="Supplier">
        <el-input :model-value="supplierName" disabled />
      </el-form-item>

      <el-divider content-position="left">Origin Address</el-divider>

      <el-form-item label="Country">
        <el-input v-model="form.country" placeholder="Optional" />
      </el-form-item>

      <el-form-item label="Province / State">
        <el-input v-model="form.province" placeholder="Optional" />
      </el-form-item>

      <el-form-item label="City">
        <el-input v-model="form.city" placeholder="Optional" />
      </el-form-item>

      <el-form-item label="District">
        <el-input v-model="form.district" placeholder="Optional" />
      </el-form-item>

      <el-form-item label="Postal Code">
        <el-input v-model="form.postal_code" placeholder="Optional" />
      </el-form-item>

      <el-form-item label="Detailed Address" prop="detailed_address">
        <el-input
          v-model="form.detailed_address"
          type="textarea"
          :rows="2"
          placeholder="Please enter detailed address"
        />
      </el-form-item>

      <el-form-item label="Full Address">
        <el-input :model-value="fullAddressPreview" disabled />
      </el-form-item>

      <el-form-item label="Default Address">
        <el-switch v-model="form.is_default" />
      </el-form-item>

      <el-form-item label="Active">
        <el-switch v-model="form.is_active" />
      </el-form-item>

      <el-form-item label="Remark">
        <el-input
          v-model="form.remark"
          type="textarea"
          :rows="2"
          placeholder="Optional"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="dialogVisible = false">Cancel</el-button>
      <el-button type="primary" :loading="submitting" @click="submitForm">
        Create
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import {
  buildFullAddress,
  createOriginAddress,
  type OriginAddress,
} from '@/api/supplier'

const props = defineProps<{
  modelValue: boolean
  supplierId: string | null
  supplierName: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'created', value: OriginAddress): void
}>()

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit('update:modelValue', value),
})

const formRef = ref<FormInstance>()
const submitting = ref(false)

const defaultForm = () => ({
  country: '',
  province: '',
  city: '',
  district: '',
  postal_code: '',
  detailed_address: '',
  is_default: false,
  is_active: true,
  remark: '',
})

const form = reactive(defaultForm())

const rules: FormRules = {
  detailed_address: [
    {
      required: true,
      message: 'Please enter detailed address',
      trigger: 'blur',
    },
  ],
}

const fullAddressPreview = computed(() => {
  return buildFullAddress(form)
})

function resetForm() {
  Object.assign(form, defaultForm())
  formRef.value?.clearValidate()
}

async function submitForm() {
  if (!props.supplierId) {
    ElMessage.warning('Please select supplier first')
    return
  }

  if (!formRef.value) return

  await formRef.value.validate()

  const fullAddress = fullAddressPreview.value

  if (!fullAddress) {
    ElMessage.warning('Please enter origin address')
    return
  }

  submitting.value = true

  try {
    const result = await createOriginAddress(props.supplierId, {
      country: form.country || null,
      province: form.province || null,
      city: form.city || null,
      district: form.district || null,
      postal_code: form.postal_code || null,
      detailed_address: form.detailed_address || null,
      full_address: fullAddress,
      is_default: form.is_default,
      is_active: form.is_active,
      remark: form.remark || null,
    })

    ElMessage.success('Origin address created successfully')
    emit('created', result)
    dialogVisible.value = false
  } catch (error) {
    console.error(error)
    ElMessage.error('Failed to create origin address')
  } finally {
    submitting.value = false
  }
}
</script>