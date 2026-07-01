<template>
  <div class="goods-receipt-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>New Goods Receipt</span>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="150px"
        label-position="right"
      >
        <el-form-item label="Receipt Time" prop="receipt_time">
          <el-input :model-value="formattedReceiptTime" disabled />
        </el-form-item>

        <el-form-item label="Supplier" prop="supplier_id">
          <SelectSupplier
            v-model:supplier-id="form.supplier_id"
            v-model:supplier-name="form.supplier_name"
            @supplier-created="handleSupplierCreated"
          />
        </el-form-item>

        <el-form-item label="Origin Address" prop="origin_address_id">
          <SelectOriginAddress
            v-model:origin-id="form.origin_address_id"
            v-model:origin-address="form.origin_address"
            :supplier-id="form.supplier_id"
            :supplier-name="form.supplier_name"
          />
        </el-form-item>

        <el-form-item label="Material" prop="material_id">
          <SelectMaterial
            v-model:material-id="form.material_id"
            v-model:material-name="form.material_name_cn"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="submitting"
            @click="submitForm"
          >
            Submit
          </el-button>

          <el-button @click="resetForm">
            Reset
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-if="createdReceipt" class="result-card">
      <template #header>
        <span>Created Receipt</span>
      </template>

      <el-descriptions :column="1" border>
        <el-descriptions-item label="Receipt ID">
          {{ createdReceipt.receipt_id }}
        </el-descriptions-item>

        <el-descriptions-item label="Receipt Time">
          {{ createdReceipt.receipt_time }}
        </el-descriptions-item>

        <el-descriptions-item label="Supplier">
          {{ createdReceipt.supplier_name }}
        </el-descriptions-item>

        <el-descriptions-item label="Origin Address">
          {{ createdReceipt.origin_address }}
        </el-descriptions-item>

        <el-descriptions-item label="Material">
          {{ createdReceipt.material_name_cn }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'

import SelectSupplier from '@/components/SelectSupplier.vue'
import SelectOriginAddress from '@/components/SelectOriginAddress.vue'
import SelectMaterial from '@/components/SelectMaterial.vue'

import {
  getOriginAddressLabel,
  type CreateSupplierResult,
} from '@/api/supplier'

import {
  createGoodsReceipt,
  type CreateGoodsReceiptResult,
} from '@/api/goodsReceipt'

interface GoodsReceiptForm {
  receipt_time: Date

  supplier_id: string | null
  supplier_name: string

  origin_address_id: number | null
  origin_address: string

  material_id: number | null
  material_name_cn: string
}

const formRef = ref<FormInstance>()
const submitting = ref(false)
const createdReceipt = ref<CreateGoodsReceiptResult | null>(null)

const createDefaultForm = (): GoodsReceiptForm => ({
  receipt_time: new Date(),

  supplier_id: null,
  supplier_name: '',

  origin_address_id: null,
  origin_address: '',

  material_id: null,
  material_name_cn: '',
})

const form = ref<GoodsReceiptForm>(createDefaultForm())

const rules: FormRules = {
  receipt_time: [
    {
      required: true,
      message: 'Receipt time is required',
      trigger: 'change',
    },
  ],
  supplier_id: [
    {
      required: true,
      message: 'Please select supplier',
      trigger: 'change',
    },
  ],
  origin_address_id: [
    {
      required: true,
      message: 'Please select origin address',
      trigger: 'change',
    },
  ],
  material_id: [
    {
      required: true,
      message: 'Please select material',
      trigger: 'change',
    },
  ],
}

const formattedReceiptTime = computed(() => {
  return formatDateTime(form.value.receipt_time)
})

function formatDateTime(date: Date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hour = String(date.getHours()).padStart(2, '0')
  const minute = String(date.getMinutes()).padStart(2, '0')
  const second = String(date.getSeconds()).padStart(2, '0')

  return `${year}-${month}-${day} ${hour}:${minute}:${second}`
}

function handleSupplierCreated(result: CreateSupplierResult) {
  form.value.supplier_id = result.supplier.supplier_id
  form.value.supplier_name = result.supplier.supplier_name_cn

  form.value.origin_address_id = result.origin_address.id
  form.value.origin_address = getOriginAddressLabel(result.origin_address)
}

async function submitForm() {
  if (!formRef.value) return

  await formRef.value.validate()

  if (!form.value.supplier_id) {
    ElMessage.warning('Please select supplier')
    return
  }

  if (!form.value.origin_address_id) {
    ElMessage.warning('Please select origin address')
    return
  }

  if (!form.value.material_id) {
    ElMessage.warning('Please select material')
    return
  }

  submitting.value = true

  try {
    const payload = {
      receipt_time: form.value.receipt_time.toISOString(),

      supplier_id: form.value.supplier_id,
      supplier_name: form.value.supplier_name,

      origin_address_id: form.value.origin_address_id,
      origin_address: form.value.origin_address,

      material_id: form.value.material_id,
      material_name_cn: form.value.material_name_cn,
    }

    const result = await createGoodsReceipt(payload)

    createdReceipt.value = result

    ElMessage.success(`Goods receipt created: ${result.receipt_id}`)
  } catch (error) {
    console.error(error)
    ElMessage.error('Failed to create goods receipt')
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  form.value = createDefaultForm()
  createdReceipt.value = null
  formRef.value?.clearValidate()
}
</script>

<style scoped>
.goods-receipt-page {
  padding: 16px;
}

.card-header {
  font-weight: 600;
}

.result-card {
  margin-top: 16px;
}
</style>