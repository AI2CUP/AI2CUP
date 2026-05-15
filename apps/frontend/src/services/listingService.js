import api from './api'

export const listingService = {
  /**
   * Get all active listings (public, no auth required).
   */
  getListings(filters = {}) {
    const params = new URLSearchParams()
    if (filters.region) params.append('region', filters.region)
    if (filters.max_grade) params.append('max_grade', filters.max_grade)
    const qs = params.toString()
    return api.get(`/listings${qs ? '?' + qs : ''}`)
  },

  /**
   * Create a new listing (auth required).
   */
  createListing(data) {
    return api.post('/listings', data)
  },

  /**
   * Get the current user's listings (auth required).
   */
  getMyListings() {
    return api.get('/listings/my')
  },

  /**
   * Update an existing listing (auth required, owner only).
   */
  updateListing(id, data) {
    return api.put(`/listings/${id}`, data)
  },

  /**
   * Delete a listing (auth required, owner only).
   */
  deleteListing(id) {
    return api.delete(`/listings/${id}`)
  },
}
