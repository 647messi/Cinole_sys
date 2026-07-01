<template>
  <el-dialog
    v-model="dialogVisible"
    title="New Supplier"
    width="760px"
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
      <el-divider content-position="left">Supplier Information</el-divider>

      <el-form-item label="Supplier CN Name" prop="supplier.supplier_name_cn">
        <el-input
          v-model="form.supplier.supplier_name_cn"
          placeholder="Please enter Chinese supplier name"
        />
      </el-form-item>

      <el-form-item label="Supplier EN Name">
        <el-input
          v-model="form.supplier.supplier_name_en"
          placeholder="Optional"
        />
      </el-form-item>

      <el-form-item label="Short Code">
        <el-input
          v-model="form.supplier.supplier_short_code"
          placeholder="Optional"
        />
      </el-form-item>

      <el-form-item label="Supplier Type">
        <el-input
          v-model="form.supplier.supplier_type_code"
          placeholder="Optional"
        />
      </el-form-item>

      <el-form-item label="Contact Name">
        <el-input
          v-model="form.supplier.contact_name"
          placeholder="Optional"
        />
      </el-form-item>

      <el-form-item label="Phone">
        <el-input
          v-model="form.supplier.phone"
          placeholder="Optional"
        />
      </el-form-item>

      <el-form-item label="Email">
        <el-input
          v-model="form.supplier.email"
          placeholder="Optional"
        />
      </el-form-item>

      <el-form-item label="Active">
        <el-switch v-model="form.supplier.is_active" />
      </el-form-item>

      <el-form-item label="Remark">
        <el-input
          v-model="form.supplier.remark"
          type="textarea"
          :rows="2"
          placeholder="Optional"
        />
      </el-form-item>

      <el-divider content-position="left">Origin Address</el-divider>

      <el-form-item label="Country">
        <el-input v-model="form.origin_address.country" placeholder="Optional" />
      </el-form-item>

      <el-form-item label="Province / State">
        <el-input
          v-model="form.origin_address.province"
          placeholder="Optional"
        />
      </el-form-item>

      <el-form-item label="City">
        <el-input v-model="form.origin_address.city" placeholder="Optional" />
      </el-form-item>

      <el-form-item label="District">
        <el-input
          v-model="form.origin_address.district"
          placeholder="Optional"
        />
      </el-form-item>

      <el-form-item label="Postal Code">
        <el-input
          v-model="form.origin_address.postal_code"
          placeholder="Optional"
        />
      </el-form-item>

      <el-form-item label="Detailed Address" prop="origin_address.detailed_address">
        <el-input
          v-model="form.origin_address.detailed_address"
          type="textarea"
          :rows="2"
          placeholder="Please enter detailed address"
        />
      </el-form-item>

      <el-form-item label="Full Address">
        <el-input :model-value="fullAddressPreview" disabled />
      </el-form-item>

      <el-form-item label="Default Address">
        <el-switch v-model="form.origin_address.is_default" />
      </el-form-item>

      <el-form-item label="Active">
        <el-switch v-model="form.origin_address.is_active" />
      </el-form-item>

      <el-form-item label="Address Remark">
        <el-input
          v-model="form.origin_address.remark"
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
  createSupplierWithOrigin,
  type CreateSupplierResult,
} from '@/api/supplier'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'created', value: CreateSupplierResult): void
}>()

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit('update:modelValue', value),
})

const formRef = ref<FormInstance>()
const submitting = ref(false)

const defaultForm = () => ({
  supplier: {
    supplier_name_cn: '',
    supplier_name_en: '',
    supplier_short_code: '',
    supplier_type_code: '',
    contact_name: '',
    phone: '',
    email: '',
    is_active: true,
    remark: '',
  },
  origin_address: {
    country: '',
    province: '',
    city: '',
    district: '',
    postal_code: '',
    detailed_address: '',
    is_default: true,
    is_active: true,
    remark: '',
  },
})

const form = reactive(defaultForm())

const rules: FormRules = {
  'supplier.supplier_name_cn': [
    {
      required: true,
      message: 'Please enter supplier Chinese name',
      trigger: 'blur',
    },
  ],
  'origin_address.detailed_address': [
    {
      required: true,
      message: 'Please enter detailed address',
      trigger: 'blur',
    },
  ],
}

const fullAddressPreview = computed(() => {
  return buildFullAddress(form.origin_address)
})

function resetForm() {
  Object.assign(form.supplier, defaultForm().supplier)
  Object.assign(form.origin_address, defaultForm().origin_address)
  formRef.value?.clearValidate()
}

async function submitForm() {
  if (!formRef.value) return

  await formRef.value.validate()

  const fullAddress = fullAddressPreview.value

  if (!fullAddress) {
    ElMessage.warning('Please enter origin address')
    return
  }

  submitting.value = true

  try {
    const result = await createSupplierWithOrigin({
      supplier: {
        supplier_name_cn: form.supplier.supplier_name_cn,
        supplier_name_en: form.supplier.supplier_name_en || null,
        supplier_short_code: form.supplier.supplier_short_code || null,
        supplier_type_code: form.supplier.supplier_type_code || null,
        contact_name: form.supplier.contact_name || null,
        phone: form.supplier.phone || null,
        email: form.supplier.email || null,
        is_active: form.supplier.is_active,
        remark: form.supplier.remark || null,
      },
      origin_address: {
        country: form.origin_address.country || null,
        province: form.origin_address.province || null,
        city: form.origin_address.city || null,
        district: form.origin_address.district || null,
        postal_code: form.origin_address.postal_code || null,
        detailed_address: form.origin_address.detailed_address || null,
        full_address: fullAddress,
        is_default: form.origin_address.is_default,
        is_active: form.origin_address.is_active,
        remark: form.origin_address.remark || null,
      },
    })

    ElMessage.success('Supplier created successfully')
    emit('created', result)
    dialogVisible.value = false
  } catch (error) {
    console.error(error)
    ElMessage.error('Failed to create supplier')
  } finally {
    submitting.value = false
  }
}
</script>