import axios from 'axios'
import { API_PREFIX } from './config'

const http = axios.create({
  baseURL: '',
  timeout: 15000,
})

export interface Material {
  id: number
  material_id?: string | null
  material_code?: string | null
  material_name_cn: string
  material_name_en?: string | null
  is_active?: boolean
}

function unwrap<T>(res: any): T {
  return res?.data?.data ?? res?.data ?? res
}

export async function searchMaterials(keyword = ''): Promise<Material[]> {
  const res = await http.get(`${API_PREFIX.master}/master/materials`, {
    params: {
      keyword,
      is_active: true,
    },
  })

  return unwrap<Material[]>(res)
}