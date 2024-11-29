<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useContactStore } from '@/stores/contact'
import { contactSchema } from '@/utils/validation'
import { debounce } from 'lodash-es'

const siteKey = "6LdUfIUqAAAAAAc91MsZhitzI0rtLxN6WTgUyAj3"
const contactStore = useContactStore()

const formData = reactive({
  name: '',
  email: '',
  message: ''
})

const validationState = reactive({
  name: { valid: false, error: '' },
  email: { valid: false, error: '' },
  message: { valid: false, error: '' },
  recaptcha: { valid: false, error: '' }
})

const submitStatus = ref({ type: null, message: '' })

const isFormValid = computed(() => {
  return Object.values(validationState).every(field => field.valid)
})

const validateField = debounce(async (field) => {
  try {
    await contactSchema.validateAt(field, formData)
    validationState[field] = { valid: true, error: ''}
  } catch (err) {
    validationState[field] = { valid: false, error: err.message}
  }
}, 500) 

const validateName = () => validateField('name')
const validateEmail = () => validateField('email')
const validateMessage = () => validateField('message')

const validateRecaptcha = () => {
  const recaptchaResponse = window.grecaptcha.getResponse()
  
  if (recaptchaResponse) {
    validationState.recaptcha = { valid: true, error: ''}
  } else {
    validationState.recaptcha = { valid: false, error: ''}
  }
}

const handleSubmit = async () => {
  submitStatus.value = { type: null, message: '' }

  await Promise.all([
    validateField('name'),
    validateField('email'),
    validateField('message')
  ])

  validateRecaptcha()

  if (isFormValid.value) {
    try {
      contactStore.loading = true
      const recaptchaToken = window.grecaptcha.getResponse()
      
      const success = await contactStore.submitContact({
        ...formData,
        recaptchaToken
      })

      if (success) {
        resetForm()
        submitStatus.value = { 
          type: 'success', 
          message: 'Mensaje enviado! Pronto le responderemos' 
        }
      }
    } catch (error) {
      console.log(error)
      submitStatus.value = {
        type: 'error',
        message: 'No hemos podido enviar el mensaje. Intente nuevamente en unos momentos'
      }
    } finally {
      contactStore.loading = false
    }
  }
}

const resetForm = () => {
  Object.keys(formData).forEach(key => {
    formData[key] = ''
    validationState[key] = { valid: false, error: ''}
  })
  
  window.grecaptcha.reset()
}

const loadRecaptchaScript = () => {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = 'https://www.google.com/recaptcha/api.js'
    script.async = true
    script.defer = true
    script.onload = resolve
    script.onerror = reject
    document.head.appendChild(script)
  })
}

window.onRecaptchaSuccess = () => {
  validateRecaptcha()
}

window.onRecaptchaExpired = () => {
  validationState.recaptcha = { valid: false, error: 'reCAPTCHA has expired' }
}

onMounted(async () => {
  try {
    await loadRecaptchaScript()
  } catch (error) {
    console.error('Failed to load reCAPTCHA:', error)
  }
})
</script>

<template>
  <div class="section">
    <div class="container">
    <div v-if="submitStatus.type === 'success'" class="notification is-success">
      {{ submitStatus.message }}
    </div>
    <div v-if="submitStatus.type === 'error'" class="notification is-danger mt-4">
          {{ submitStatus.message }}
    </div>
      <form @submit.prevent="handleSubmit" class="box">
        <h2 class="title is-4 mb-5">Comunicate con nosotros</h2>

        <div class="field">
          <label class="label">Nombre</label>
          <div class="control">
            <input 
              v-model="formData.name" 
              @input="validateName"
              type="text"
              class="input"
              :class="{
                'is-success': validationState.name.valid,
                'is-danger': !validationState.name.valid && validationState.name.error
              }"
              placeholder="Tu nombre completo"
            />
          </div>
          <p 
            v-if="!validationState.name.valid && validationState.name.error" 
            class="help is-danger"
          >
            {{ validationState.name.error }}
          </p>
        </div>

        <div class="field">
          <label class="label">Email</label>
          <div class="control">
            <input 
              v-model="formData.email" 
              @input="validateEmail"
              type="email"
              class="input"
              :class="{
                'is-success': validationState.email.valid,
                'is-danger': !validationState.email.valid && validationState.email.error
              }"
              placeholder="tu@email.com"
            />
          </div>
          <p 
            v-if="!validationState.email.valid && validationState.email.error" 
            class="help is-danger"
          >
            {{ validationState.email.error }}
          </p>
        </div>

        <div class="field">
          <label class="label">Mensaje</label>
          <div class="control">
            <textarea 
              v-model="formData.message" 
              @input="validateMessage"
              class="textarea"
              :class="{
                'is-success': validationState.message.valid,
                'is-danger': !validationState.message.valid && validationState.message.error
              }"
              placeholder="Escribe tu mensaje"
            ></textarea>
          </div>
          <p 
            v-if="!validationState.message.valid && validationState.message.error && !submitStatus.type" 
            class="help is-danger"
          >
            {{ validationState.message.error }}
          </p>
        </div>

        <div 
          class="g-recaptcha" 
          :data-sitekey="siteKey"
          data-callback="onRecaptchaSuccess"
          data-expired-callback="onRecaptchaExpired"
        ></div>
        <p 
          v-if="validationState.recaptcha.error" 
          class="help is-danger"
        >
          {{ validationState.recaptcha.error }}
        </p>

        <div class="field">
          <div class="control">
            <button 
              type="submit" 
              class="button is-primary is-fullwidth mt-2 is-info is-outlined has-text-dark"
              :class="{ 
                'is-loading': contactStore.loading,
                'is-disabled': !isFormValid 
              }"
              :disabled="!isFormValid"
            >
              Enviar Mensaje
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>
