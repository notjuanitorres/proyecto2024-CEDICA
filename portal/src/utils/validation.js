import * as yup from 'yup'

export const contactSchema = yup.object({
  name: yup.string()
    .required('El nombre es obligatorio')
    .min(2, 'El nombre debe tener al menos 2 caracteres')
    .max(50, 'El nombre debe tener menos de 50 caracteres'),
  email: yup.string()
    .required('El correo electrónico es obligatorio')
    .email('Debe ser un correo electrónico válido'),
  message: yup.string()
    .required('El mensaje es obligatorio')
    .min(10, 'El mensaje debe tener al menos 10 caracteres')
    .max(500, 'El mensaje debe tener menos de 500 caracteres')
})
