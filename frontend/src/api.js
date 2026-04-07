/**
 * Centralização da API para facilitar o deploy e desenvolvimento.
 * O Vite injeta variáveis que começam com VITE_ em import.meta.env
 */
const rawApiBase = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
// Garante que não termine com barra para não duplicar nas chamadas
export const API_BASE = rawApiBase.endsWith('/') ? rawApiBase.slice(0, -1) : rawApiBase

export const getHeaders = (token = null) => {
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`
  return headers
}
