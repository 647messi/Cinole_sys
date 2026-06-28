import request from "./request"

export function createReceivingOrder() {
  return request.post("/receiving-orders/new")
}

export function getSuppliers() {
  return request.get("/suppliers")
}

export function addSupplierApi(data: {
  supplier_name: string
  origin: string
}) {
  return request.post("/suppliers", data)
}

export function deleteSupplierApi(supplierId: number) {
  return request.delete(`/suppliers/${supplierId}`)
}

export function getMaterials() {
  return request.get("/materials")
}

export function submitReceivingOrder(data: any) {
  return request.post("/receiving-orders", data)
}