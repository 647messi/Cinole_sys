// src/api/request.ts

import axios from "axios"

const request = axios.create({
  baseURL: "http://localhost:5173",
  timeout: 10000,
})

export default request