<script setup lang="ts">
import { ref, onMounted } from "vue"
import { ElMessage, ElMessageBox } from "element-plus"
import {
  createReceivingOrder,
  getSuppliers,
  getMaterials,
  submitReceivingOrder,
  addSupplierApi,
  deleteSupplierApi
} from "@/api/receiving"

interface Supplier {
  id: number
  supplier_name: string
  origin: string
}

interface Material {
  id: number
  material_name: string
}

const form = ref({
  order_id: "",
  timestamp: new Date(),
  supplier_id: null as number | null,
  supplier_name: "",
  origin: "",
  material_id: null as number | null
})

const supplierDialogVisible = ref(false)
const addDialogVisible = ref(false)

const supplierList = ref<Supplier[]>([])
const materialList = ref<Material[]>([])

const selectedSupplier = ref<Supplier | null>(null)

const newSupplier = ref({
  supplier_name: "",
  origin: ""
})

async function loadSuppliers() {
  const res = await getSuppliers()
  supplierList.value = res.data
}

async function loadMaterials() {
  const res = await getMaterials()
  materialList.value = res.data
}

async function handleCreateOrder() {
  const res = await createReceivingOrder()

  form.value = {
    order_id: res.data.order_id,
    timestamp: new Date(),
    supplier_id: null,
    supplier_name: "",
    origin: "",
    material_id: null
  }

  ElMessage.success("New receiving order created")
}

function openSupplierDialog() {
  selectedSupplier.value = null
  supplierDialogVisible.value = true
}

function handleCurrentChange(row: Supplier | null) {
  selectedSupplier.value = row
}

function confirmSupplier() {
  if (!selectedSupplier.value) return

  form.value.supplier_id = selectedSupplier.value.id
  form.value.supplier_name = selectedSupplier.value.supplier_name
  form.value.origin = selectedSupplier.value.origin

  supplierDialogVisible.value = false
}

async function addSupplier() {
  if (!newSupplier.value.supplier_name || !newSupplier.value.origin) {
    ElMessage.warning("Please enter supplier name and origin")
    return
  }

  await addSupplierApi({
    supplier_name: newSupplier.value.supplier_name,
    origin: newSupplier.value.origin
  })

  newSupplier.value = {
    supplier_name: "",
    origin: ""
  }

  addDialogVisible.value = false

  await loadSuppliers()

  ElMessage.success("Supplier added")
}

async function deleteSupplier() {
  if (!selectedSupplier.value) return

  try {
    await ElMessageBox.confirm(
      "Are you sure you want to delete this supplier?",
      "Warning",
      { type: "warning" }
    )

    await deleteSupplierApi(selectedSupplier.value.id)

    if (form.value.supplier_id === selectedSupplier.value.id) {
      form.value.supplier_id = null
      form.value.supplier_name = ""
      form.value.origin = ""
    }

    selectedSupplier.value = null

    await loadSuppliers()

    ElMessage.success("Supplier deleted")
  } catch {
    ElMessage.info("Delete cancelled")
  }
}

async function submitForm() {
  if (!form.value.order_id) {
    ElMessage.warning("Please create a receiving order first")
    return
  }

  if (!form.value.supplier_id) {
    ElMessage.warning("Please select supplier")
    return
  }

  if (!form.value.material_id) {
    ElMessage.warning("Please select material")
    return
  }

  await submitReceivingOrder(form.value)

  ElMessage.success("Receiving order submitted")
}

onMounted(async () => {
  await loadSuppliers()
  await loadMaterials()
})
</script>

<template>
  <div class="page-container">
    <p class="page-title">form</p>

    <p>
      <RouterLink to="/home">Home</RouterLink>
    </p>

    <el-card class="form-card">
      <div class="card-header">
        <h2>收货单</h2>

        <el-button type="primary" @click="handleCreateOrder">
          创建收货单
        </el-button>
      </div>

      <el-form :model="form" label-width="120px">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="24" :md="12">
            <el-form-item label="Order ID">
              <el-input v-model="form.order_id" readonly />
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="12">
            <el-form-item label="Timestamp">
              <el-date-picker
                v-model="form.timestamp"
                type="datetime"
                placeholder="Select datetime"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="12">
            <el-form-item label="Supplier">
              <div class="supplier-row">
                <div class="supplier-display">
                  <div class="supplier-name">
                    {{ form.supplier_name || "No supplier selected" }}
                  </div>
                  <div class="supplier-origin">
                    Origin: {{ form.origin || "-" }}
                  </div>
                </div>

                <el-button type="primary" @click="openSupplierDialog">
                  Select
                </el-button>
              </div>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="12">
            <el-form-item label="Material">
              <el-select
                v-model="form.material_id"
                placeholder="Select material"
                style="width: 100%"
              >
                <el-option
                  v-for="material in materialList"
                  :key="material.id"
                  :label="material.material_name"
                  :value="material.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="success" @click="submitForm">
            Submit
          </el-button>
        </el-form-item>
      </el-form>

      <el-dialog
        v-model="supplierDialogVisible"
        title="Select Supplier"
        width="90%"
        class="supplier-dialog"
      >
        <div class="dialog-toolbar">
          <el-button type="primary" @click="addDialogVisible = true">
            Add
          </el-button>

          <el-button
            type="danger"
            :disabled="!selectedSupplier"
            @click="deleteSupplier"
          >
            Delete
          </el-button>
        </div>

        <el-table
          :data="supplierList"
          highlight-current-row
          @current-change="handleCurrentChange"
          style="width: 100%"
        >
          <el-table-column prop="supplier_name" label="Supplier Name" />
          <el-table-column prop="origin" label="Origin" />
        </el-table>

        <template #footer>
          <el-button @click="supplierDialogVisible = false">
            Cancel
          </el-button>

          <el-button
            type="primary"
            :disabled="!selectedSupplier"
            @click="confirmSupplier"
          >
            Confirm
          </el-button>
        </template>
      </el-dialog>

      <el-dialog
        v-model="addDialogVisible"
        title="Add Supplier"
        width="90%"
        class="add-supplier-dialog"
      >
        <el-form :model="newSupplier" label-width="120px">
          <el-form-item label="Supplier Name">
            <el-input v-model="newSupplier.supplier_name" />
          </el-form-item>

          <el-form-item label="Origin">
            <el-input v-model="newSupplier.origin" />
          </el-form-item>
        </el-form>

        <template #footer>
          <el-button @click="addDialogVisible = false">
            Cancel
          </el-button>

          <el-button type="primary" @click="addSupplier">
            Add
          </el-button>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<style scoped>
.page-container {
  width: 100%;
  min-height: 100vh;
  box-sizing: border-box;
  padding: 24px;
}

.page-title {
  margin: 0 0 8px;
}

.form-card {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  box-sizing: border-box;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.card-header h2 {
  margin: 0;
}

.supplier-row {
  display: flex;
  gap: 12px;
  width: 100%;
  align-items: stretch;
}

.supplier-display {
  flex: 1;
  min-height: 32px;
  padding: 8px 12px;
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  background-color: var(--el-fill-color-light);
  box-sizing: border-box;
}

.supplier-name {
  font-size: 14px;
  color: var(--el-text-color-primary);
}

.supplier-origin {
  margin-top: 4px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.dialog-toolbar {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-bottom: 12px;
}

:deep(.supplier-dialog) {
  max-width: 700px;
}

:deep(.add-supplier-dialog) {
  max-width: 500px;
}

@media (max-width: 768px) {
  .page-container {
    padding: 12px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .supplier-row {
    flex-direction: column;
  }

  :deep(.el-dialog) {
    width: 95% !important;
  }
}
</style>

<!-- <script setup lang="ts">
import { ref } from "vue"
import { ElMessage, ElMessageBox } from "element-plus"

interface Supplier {
  supplier_name: string
  origin: string
}

const form = ref({
  order_id: "GRN00001",
  timestamp: new Date(),
  supplier_name: "",
  origin: "",
  material_name: ""
})

const supplierDialogVisible = ref(false)
const addDialogVisible = ref(false)

const supplierList = ref<Supplier[]>([
  {
    supplier_name: "ABC Supplier",
    origin: "China"
  },
  {
    supplier_name: "XYZ Supplier",
    origin: "Australia"
  }
])

const materialNameList = ref([
  "Steel",
  "Aluminium",
  "Copper",
  "Plastic"
])

const selectedSupplier = ref<Supplier | null>(null)

const newSupplier = ref<Supplier>({
  supplier_name: "",
  origin: ""
})

function openSupplierDialog() {
  selectedSupplier.value = null
  supplierDialogVisible.value = true
}

function handleCurrentChange(row: Supplier | null) {
  selectedSupplier.value = row
}

function confirmSupplier() {
  if (!selectedSupplier.value) return

  form.value.supplier_name = selectedSupplier.value.supplier_name
  form.value.origin = selectedSupplier.value.origin

  supplierDialogVisible.value = false
}

function addSupplier() {
  if (!newSupplier.value.supplier_name || !newSupplier.value.origin) {
    ElMessage.warning("Please enter supplier name and origin")
    return
  }

  const exists = supplierList.value.some(
    item => item.supplier_name === newSupplier.value.supplier_name
  )

  if (exists) {
    ElMessage.warning("Supplier already exists")
    return
  }

  supplierList.value.push({
    supplier_name: newSupplier.value.supplier_name,
    origin: newSupplier.value.origin
  })

  newSupplier.value = {
    supplier_name: "",
    origin: ""
  }

  addDialogVisible.value = false
  ElMessage.success("Supplier added")
}

async function deleteSupplier() {
  if (!selectedSupplier.value) return

  try {
    await ElMessageBox.confirm(
      "Are you sure you want to delete this supplier?",
      "Warning",
      {
        type: "warning"
      }
    )

    supplierList.value = supplierList.value.filter(
      item =>
        selectedSupplier.value &&
        item.supplier_name !== selectedSupplier.value.supplier_name
    )

    if (form.value.supplier_name === selectedSupplier.value.supplier_name) {
      form.value.supplier_name = ""
      form.value.origin = ""
    }

    selectedSupplier.value = null
    ElMessage.success("Supplier deleted")
  } catch {
    ElMessage.info("Delete cancelled")
  }
}

function submitForm() {
  console.log("Receiving Order:", form.value)
  ElMessage.success("Receiving order submitted")
}
</script>

<template>
  <div class="page-container">
    <p class="page-title">form</p>

    <p>
      <RouterLink to="/home">Home</RouterLink>
    </p>

    <el-card class="form-card">
      <h2>收货单</h2>

      <el-form :model="form" label-width="120px">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="24" :md="12">
            <el-form-item label="Order ID">
              <el-input v-model="form.order_id" readonly />
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="12">
            <el-form-item label="Timestamp">
              <el-date-picker
                v-model="form.timestamp"
                type="datetime"
                placeholder="Select datetime"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="12">
            <el-form-item label="Supplier">
              <div class="supplier-row">
                <div class="supplier-display">
                  <div class="supplier-name">
                    {{ form.supplier_name || "No supplier selected" }}
                  </div>
                  <div class="supplier-origin">
                    Origin: {{ form.origin || "-" }}
                  </div>
                </div>

                <el-button type="primary" @click="openSupplierDialog">
                  Select
                </el-button>
              </div>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="12">
            <el-form-item label="Material">
              <el-select
                v-model="form.material_name"
                placeholder="Select material"
                style="width: 100%"
              >
                <el-option
                  v-for="material in materialNameList"
                  :key="material"
                  :label="material"
                  :value="material"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="success" @click="submitForm">
            Submit
          </el-button>
        </el-form-item>
      </el-form>

      <el-dialog
        v-model="supplierDialogVisible"
        title="Select Supplier"
        width="90%"
        class="supplier-dialog"
      >
        <div class="dialog-toolbar">
          <el-button type="primary" @click="addDialogVisible = true">
            Add
          </el-button>

          <el-button
            type="danger"
            :disabled="!selectedSupplier"
            @click="deleteSupplier"
          >
            Delete
          </el-button>
        </div>

        <el-table
          :data="supplierList"
          highlight-current-row
          @current-change="handleCurrentChange"
          style="width: 100%"
        >
          <el-table-column prop="supplier_name" label="Supplier Name" />
          <el-table-column prop="origin" label="Origin" />
        </el-table>

        <template #footer>
          <el-button @click="supplierDialogVisible = false">
            Cancel
          </el-button>

          <el-button
            type="primary"
            :disabled="!selectedSupplier"
            @click="confirmSupplier"
          >
            Confirm
          </el-button>
        </template>
      </el-dialog>

      <el-dialog
        v-model="addDialogVisible"
        title="Add Supplier"
        width="90%"
        class="add-supplier-dialog"
      >
        <el-form :model="newSupplier" label-width="120px">
          <el-form-item label="Supplier Name">
            <el-input v-model="newSupplier.supplier_name" />
          </el-form-item>

          <el-form-item label="Origin">
            <el-input v-model="newSupplier.origin" />
          </el-form-item>
        </el-form>

        <template #footer>
          <el-button @click="addDialogVisible = false">
            Cancel
          </el-button>

          <el-button type="primary" @click="addSupplier">
            Add
          </el-button>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<style scoped>
.page-container {
  width: 100%;
  min-height: 100vh;
  box-sizing: border-box;
  padding: 24px;
}

.page-title {
  margin: 0 0 8px;
}

.form-card {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  box-sizing: border-box;
}

.supplier-row {
  display: flex;
  gap: 12px;
  width: 100%;
  align-items: stretch;
}

.supplier-display {
  flex: 1;
  min-height: 32px;
  padding: 8px 12px;
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  background-color: var(--el-fill-color-light);
  box-sizing: border-box;
}

.supplier-name {
  font-size: 14px;
  color: var(--el-text-color-primary);
}

.supplier-origin {
  margin-top: 4px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.dialog-toolbar {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-bottom: 12px;
}

:deep(.supplier-dialog) {
  max-width: 700px;
}

:deep(.add-supplier-dialog) {
  max-width: 500px;
}

@media (max-width: 768px) {
  .page-container {
    padding: 12px;
  }

  .supplier-row {
    flex-direction: column;
  }

  :deep(.el-dialog) {
    width: 95% !important;
  }
}
</style> -->