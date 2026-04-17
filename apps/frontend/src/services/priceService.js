import api from './api'

export const priceService = {
  predict(params) {
    return api.post('/price/predict', params)
  }
}
