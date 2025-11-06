import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:3000/api',
  timeout: 10000,
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const login = async (username, password) => {
  const { data } = await axios.post('http://127.0.0.1:8000/api/auth/token/', { username, password })
  localStorage.setItem('access', data.access)
  localStorage.setItem('refresh', data.refresh)
}

export const fetchMenu = async (q = '') => {
  const { data } = await API.get('menu/', { params: q ? { search: q } : {} })
  return data
}