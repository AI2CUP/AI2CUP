import api from './api'

export const qualityService = {
  analyze(imageFile) {
    const formData = new FormData()
    formData.append('file', imageFile)
    return api.post('/quality/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  }
}
