<script setup>
import { ref, reactive } from 'vue'
import { useContactStore } from '@/stores/contact'
import { contactSchema } from '@/utils/validation'

const contactStore = useContactStore()
const submitStatus = ref({ type: null, message: '' })
const formData = reactive({
  name: '',
  email: '',
  message: '',
})
const errors = reactive({
  name: '',
  email: '',
  message: '',
})

const resetErrors = () => {
  errors.name = ''
  errors.email = ''
  errors.message = ''
}
const resetForm = () => {
  formData.name = ''
  formData.email = ''
  formData.message = ''
}
const setErrors = (err) => {
    if (err.name === 'ValidationError' && err.inner) {
      err.inner.forEach((error) => {
        errors[error.path] = error.message
      })
    } else {
      submitStatus.value = {
        type: 'error',
        message:
          contactStore.error ||
          'No hemos podido enviar el mensaje. Intente nuevamente en unos momentos',
      }
    }
}

const handleSubmit = async () => {
  resetErrors();
  contactStore.loading = true;
  try {
    await contactSchema.validate(formData, { abortEarly: false })
    const success = await contactStore.submitContact({ ...formData })
    if (success) {
      submitStatus.value = { type: 'success', message: 'Mensaje enviado! Pronto le responderemos' }
      resetForm()
    }
  } catch (err) {
    setErrors(err)
  } finally {
    contactStore.loading = false // End loading
  }
}
</script>

<template>
  <div class="container">
    <form @submit.prevent="handleSubmit" class="box">
      <h3 class="subtitle">Dejanos tu mensaje</h3>
      <div class="field">
        <label class="label">Nombre</label>
        <div class="control">
          <input
            v-model="formData.name"
            type="text"
            class="input"
            :class="{ 'is-danger': errors.name }"
            placeholder="Nombre Completo"
          />
        </div>
        <p v-if="errors.name" class="help is-danger">
          {{ errors.name }}
        </p>
      </div>

      <div class="field">
        <label class="label">Email</label>
        <div class="control">
          <input
            v-model="formData.email"
            type="email"
            class="input"
            :class="{ 'is-danger': errors.email }"
            placeholder="ingrese@email.com"
          />
        </div>
        <p v-if="errors.email" class="help is-danger">
          {{ errors.email }}
        </p>
      </div>

      <div class="field">
        <label class="label">Mensaje</label>
        <div class="control">
          <textarea
            v-model="formData.message"
            class="textarea"
            :class="{ 'is-danger': errors.message }"
            placeholder="Escriba su mensaje para nosotros!"
          ></textarea>
        </div>
        <p v-if="errors.message" class="help is-danger">
          {{ errors.message }}
        </p>
      </div>

      <div class="field">
        <div class="control">
          <button
            type="submit"
            class="button is-info is-outlined has-text-dark is-fullwidth"
            :class="{ 'is-loading': contactStore.loading }"
          >
            Enviar Mensaje
          </button>
        </div>
      </div>

      <div v-if="submitStatus.type === 'success'" class="notification is-success">
        {{ submitStatus.message }}
      </div>
      <div v-if="submitStatus.type === 'error'" class="notification is-danger">
        {{ submitStatus.message }}
      </div>
    </form>
  </div>
</template>
