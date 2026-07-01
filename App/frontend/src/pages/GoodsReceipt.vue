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
          <RemoteSearchSelect
            v-model="form.supplier_id"
            placeholder="Search or select supplier"
            :fetch-options="fetchSupplierOptions"
            :extra-options="supplierExtraOptions"
            @change="handleSupplierChange"
            @clear="handleSupplierClear"
          >
            <template #action>
              <el-button
                type="primary"
                link
                @click="createSupplierVisible = true"
              >
                + New Supplier
              </el-button>
            </template>
          </RemoteSearchSelect>
        </el-form-item>

        <el-form-item label="Origin Address" prop="origin_address_id">
          <RemoteSearchSelect
            :key="form.supplier_id || 'no-supplier'"
            v-model="form.origin_address_id"
            placeholder="Search or select origin address"
            :disabled="!form.supplier_id"
            :fetch-options="fetchOriginOptions"
            :extra-options="originExtraOptions"
            @change="handleOriginChange"
            @clear="handleOriginClear"
          >
            <template #action>
              <el-button
                type="primary"
                link
                :disabled="!form.supplier_id"
                @click="createOriginVisible = true"
              >
                + New Origin Address
              </el-button>
            </template>
          </RemoteSearchSelect>
        </el-form-item>

        <el-form-item label="Material" prop="material_id">
          <RemoteSearchSelect
            v-model="form.material_id"
            placeholder="Search or select material"
            :fetch-options="fetchMaterialOptions"
            @change="handleMaterialChange"
            @clear="handleMaterialClear"
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

    <CreateSupplierDialog
      v-model="createSupplierVisible"
      @created="handleSupplierCreated"
    />

    <CreateOriginAddressDialog
      v-model="createOriginVisible"
      :supplier-id="form.supplier_id"
      :supplier-name="form.supplier_name"
      @created="handleOriginCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'

import RemoteSearchSelect from '@/components/common/RemoteSearchSelect.vue'
import CreateSupplierDialog from '@/components/CreateSupplierDialog.vue'
import CreateOriginAddressDialog from '@/components/CreateOriginAddressDialog.vue'

import type { SelectOption } from '@/types/select'

import {
  fetchSupplierOptions,
  fetchOriginAddressOptions,
  fetchMaterialOptions,
} from '@/api/selectOptions'

import {
  getOriginAddressLabel,
  type Supplier,
  type OriginAddress,
  type CreateSupplierResult,
} from '@/api/supplier'

import type { Material } from '@/api/material'

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

const createSupplierVisible = ref(false)
const createOriginVisible = ref(false)

const createdReceipt = ref<CreateGoodsReceiptResult | null>(null)

const supplierExtraOptions = ref<SelectOption<Supplier>[]>([])
const originExtraOptions = ref<SelectOption<OriginAddress>[]>([])

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

function addSupplierExtraOption(supplier: Supplier) {
  const option: SelectOption<Supplier> = {
    label: supplier.supplier_name_en
      ? `${supplier.supplier_name_cn} / ${supplier.supplier_name_en}`
      : supplier.supplier_name_cn,
    value: supplier.supplier_id,
    raw: supplier,
  }

  supplierExtraOptions.value = [
    option,
    ...supplierExtraOptions.value.filter((item) => item.value !== option.value),
  ]
}

function addOriginExtraOption(origin: OriginAddress) {
  const option: SelectOption<OriginAddress> = {
    label: getOriginAddressLabel(origin),
    value: origin.id,
    raw: origin,
  }

  originExtraOptions.value = [
    option,
    ...originExtraOptions.value.filter((item) => item.value !== option.value),
  ]
}

async function fetchOriginOptions(keyword: string) {
  if (!form.value.supplier_id) {
    return []
  }

  return fetchOriginAddressOptions(form.value.supplier_id, keyword)
}

function handleSupplierChange(option: SelectOption<Supplier> | null) {
  if (!option) {
    handleSupplierClear()
    return
  }

  form.value.supplier_id = option.raw.supplier_id
  form.value.supplier_name = option.raw.supplier_name_cn

  form.value.origin_address_id = null
  form.value.origin_address = ''
  originExtraOptions.value = []
}

function handleSupplierClear() {
  form.value.supplier_id = null
  form.value.supplier_name = ''

  form.value.origin_address_id = null
  form.value.origin_address = ''
  originExtraOptions.value = []
}

function handleOriginChange(option: SelectOption<OriginAddress> | null) {
  if (!option) {
    handleOriginClear()
    return
  }

  form.value.origin_address_id = option.raw.id
  form.value.origin_address = getOriginAddressLabel(option.raw)
}

function handleOriginClear() {
  form.value.origin_address_id = null
  form.value.origin_address = ''
}

function handleMaterialChange(option: SelectOption<Material> | null) {
  if (!option) {
    handleMaterialClear()
    return
  }

  form.value.material_id = option.raw.id
  form.value.material_name_cn = option.raw.material_name_cn
}

function handleMaterialClear() {
  form.value.material_id = null
  form.value.material_name_cn = ''
}

function handleSupplierCreated(result: CreateSupplierResult) {
  addSupplierExtraOption(result.supplier)
  addOriginExtraOption(result.origin_address)

  form.value.supplier_id = result.supplier.supplier_id
  form.value.supplier_name = result.supplier.supplier_name_cn

  form.value.origin_address_id = result.origin_address.id
  form.value.origin_address = getOriginAddressLabel(result.origin_address)
}

function handleOriginCreated(origin: OriginAddress) {
  addOriginExtraOption(origin)

  form.value.origin_address_id = origin.id
  form.value.origin_address = getOriginAddressLabel(origin)
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
    const result = await createGoodsReceipt({
      receipt_time: formatDateTime(form.value.receipt_time),

      supplier_id: form.value.supplier_id,
      supplier_name: form.value.supplier_name,

      origin_address_id: form.value.origin_address_id,
      origin_address: form.value.origin_address,

      material_id: form.value.material_id,
      material_name_cn: form.value.material_name_cn,
    })

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
  supplierExtraOptions.value = []
  originExtraOptions.value = []

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