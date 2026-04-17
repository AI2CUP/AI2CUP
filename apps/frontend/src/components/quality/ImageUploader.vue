<template>
  <div 
    class="border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-200 bg-gray-50"
    :class="[
      isDragging ? 'border-emerald-500 bg-emerald-50 scale-[1.02]' : 'border-gray-300 hover:border-emerald-400',
      hasFile ? 'border-none p-0 overflow-hidden' : ''
    ]"
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="handleDrop"
  >
    <!-- Preview Mode -->
    <div v-if="hasFile" class="relative group w-full h-[300px] md:h-[400px]">
      <img :src="previewUrl" alt="Coffee beans preview" class="w-full h-full object-cover rounded-xl" />
      <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center rounded-xl backdrop-blur-sm">
        <button @click="clearFile" class="bg-red-500 text-white px-4 py-2 rounded-lg font-medium hover:bg-red-600 shadow-md">
          Remove Image
        </button>
      </div>
    </div>
    
    <!-- Upload Mode -->
    <div v-else class="flex flex-col items-center justify-center h-full min-h-[250px]">
      <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-sm mb-4 text-3xl">
        📸
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-1">Upload Bean Image</h3>
      <p class="text-gray-500 text-sm mb-6 max-w-sm">
        Drag and drop a clear photo of green coffee beans, or click to browse.
      </p>
      
      <input 
        type="file" 
        ref="fileInput" 
        class="hidden" 
        accept="image/jpeg, image/png, image/webp" 
        @change="handleFileChange" 
      />
      
      <button 
        type="button" 
        @click="$refs.fileInput.click()" 
        class="bg-white border text-gray-700 font-medium py-2 px-6 rounded-lg shadow-sm hover:bg-gray-50 transition-colors"
      >
        Browse Files
      </button>
      <p class="text-xs text-gray-400 mt-4">JPEG, PNG, WEBP up to 10MB</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['file-selected', 'cleared'])
const fileInput = ref(null)
const isDragging = ref(false)
const selectedFile = ref(null)
const previewUrl = ref(null)

const hasFile = computed(() => selectedFile.value !== null)

const processFile = (file) => {
  if (!file || !file.type.startsWith('image/')) {
    alert('Please upload a valid image file.')
    return
  }
  
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
  
  selectedFile.value = file
  previewUrl.value = URL.createObjectURL(file)
  emit('file-selected', file)
}

const handleFileChange = (e) => {
  const file = e.target.files[0]
  processFile(file)
}

const handleDrop = (e) => {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  processFile(file)
}

const clearFile = () => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
  selectedFile.value = null
  previewUrl.value = null
  if (fileInput.value) fileInput.value.value = ''
  emit('cleared')
}
</script>
