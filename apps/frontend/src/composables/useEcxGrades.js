export function useEcxGrades() {
  const grades = {
    1: { label: 'Grade 1 - Specialty', amharic: 'ልዩ ደረጃ', color: 'bg-amber-100 text-amber-800 border-amber-200' },
    2: { label: 'Grade 2 - Very Good', amharic: 'በጣም ጥሩ', color: 'bg-green-100 text-green-800 border-green-200' },
    3: { label: 'Grade 3 - Good', amharic: 'ጥሩ', color: 'bg-yellow-100 text-yellow-800 border-yellow-200' },
    4: { label: 'Grade 4 - Commercial', amharic: 'ንግድ', color: 'bg-orange-100 text-orange-800 border-orange-200' },
    5: { label: 'Grade 5 - Below Standard', amharic: 'ከደረጃ በታች', color: 'bg-red-100 text-red-800 border-red-200' },
  }
  
  const getGradeInfo = (gradeNum) => {
    return grades[gradeNum] || { 
      label: `Grade ${gradeNum}`, 
      amharic: '', 
      color: 'bg-gray-100 text-gray-800 border-gray-200' 
    }
  }
  
  return {
    grades,
    getGradeInfo
  }
}
