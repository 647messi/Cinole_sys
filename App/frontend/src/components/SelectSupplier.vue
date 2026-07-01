<template>
  <div class="select-supplier">
    <el-select
      v-model="selectedSupplierId"
      filterable
      remote
      clearable
      reserve-keyword
      placeholder="Search or select supplier"
      :remote-method="remoteSearch"
      :loading="loading"
      style="width: 100%"
      @change="handleChange"
      @clear="handleClear"
    >
      <el-option
        v-for="item in supplierOptions"
        :key="item.supplier_id"
        :label="getSupplierLabel(item)"
        :value="item.supplier_id"
      />
    </el-select>

    <div class="action-row">
      <el-button type="primary" link @click="createDialogVisible = true">
        + New Supplier
      </el-button>
    </div>

    <CreateSupplierDialog
      v-model="createDialogVisible"
      @created="handleSupplierCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import CreateSupplierDialog from './CreateSupplierDialog.vue'
import {
  searchSuppliers,
  getOriginAddressLabel,
  type Supplier,
  type CreateSupplierResult,
} from '@/api/supplier'

const props = defineProps<{
  supplierId: string | null
  supplierName: string
}>()

const emit = defineEmits<{
  (e: 'update:supplierId', value: string | null): void
  (e: 'update:supplierName', value: string): void
  (e: 'supplier-created', value: CreateSupplierResult): void
}>()

const selectedSupplierId = ref<string | null>(props.supplierId)
const supplierOptions = ref<Supplier[]>([])
const loading = ref(false)
const createDialogVisible = ref(false)

let searchTimer: number | undefined

watch(
  () => props.supplierId,
  (newValue) => {
    selectedSupplierId.value = newValue
  },
)

onMounted(() => {
  loadSuppliers('')
})

function getSupplierLabel(item: Supplier) {
  if (item.supplier_name_en) {
    return `${item.supplier_name_cn} / ${item.supplier_name_en}`
  }

  return item.supplier_name_cn
}

function remoteSearch(query: string) {
  window.clearTimeout(searchTimer)

  searchTimer = window.setTimeout(() => {
    loadSuppliers(query)
  }, 300)
}

async function loadSuppliers(keyword: string) {
  loading.value = true

  try {
    supplierOptions.value = await searchSuppliers(keyword)
  } catch (error) {
    console.error(error)
    ElMessage.error('Failed to load suppliers')
  } finally {
    loading.value = false
  }
}

function handleChange(value: string | null) {
  if (!value) {
    handleClear()
    return
  }

  const selected = supplierOptions.value.find(
    (item) => item.supplier_id === value,
  )

  emit('update:supplierId', value)
  emit('update:supplierName', selected?.supplier_name_cn ?? '')
}

function handleClear() {
  selectedSupplierId.value = null
  emit('update:supplierId', null)
  emit('update:supplierName', '')
}

function handleSupplierCreated(result: CreateSupplierResult) {
  const supplier = result.supplier

  if (!supplierOptions.value.some((item) => item.supplier_id === supplier.supplier_id)) {
    supplierOptions.value.unshift(supplier)
  }

  selectedSupplierId.value = supplier.supplier_id

  emit('update:supplierId', supplier.supplier_id)
  emit('update:supplierName', supplier.supplier_name_cn)
  emit('supplier-created', result)

  const addressLabel = getOriginAddressLabel(result.origin_address)

  if (addressLabel) {
    ElMessage.success(`Created supplier and origin: ${addressLabel}`)
  }
}
</script>

<style scoped>
.select-supplier {
  width: 100%;
}

.action-row {
  margin-top: 6px;
  display: flex;
  justify-content: flex-start;
}
</style>