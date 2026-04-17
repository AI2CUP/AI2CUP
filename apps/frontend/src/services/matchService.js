import api from './api'

export const matchService = {
  getListings() {
    return api.get('/match')
  },
  
  findMatches(criteria) {
    return api.post('/match/find', criteria)
  }
}
