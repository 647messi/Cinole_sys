import { http, unwrap } from './http'
import { API_PREFIX } from './config'

export interface Material {
  id: number
  material_id?: string | null
  material_code?: string | null
  material_name_cn: string
  material_name_en?: string | null
  is_active?: boolean
}

export async function searchMaterials(keyword = ''): Promise<Material[]> {
  const res = await http.get(`${API_PREFIX.master}/raw_materials_dict`, {
    params: {
      keyword,
      is_active: true,
    },
  })

  return unwrap<Material[]>(res)
}