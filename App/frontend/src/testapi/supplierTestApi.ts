import axios from "axios"

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  timeout: 10000,
})

export interface SupplierCreatePayload {
  supplier_name_cn: string
  supplier_name_en?: string
  contact_person?: string
  phone?: string
  email?: string
  address?: string
}

export async function createSupplier(payload: SupplierCreatePayload) {
  const response = await apiClient.post("/master/suppliers", payload)
  return response.data
}