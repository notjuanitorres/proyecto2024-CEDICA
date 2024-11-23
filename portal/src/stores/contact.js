import { defineStore } from "pinia";


export const useContactStore = defineStore('contact', {
    state: () => ({
      submissions: [],
      loading: false,
      error: null,
    }),
    actions: {
      async submitContact(contactInformation) {
        this.loading = true;
        this.error = null;
        try {
          const apiUrl = import.meta.env.VITE_API_BASE_URL || "https://admin-grupo19.proyecto2024.linti.unlp.edu.ar/api"
          const response = await fetch(`${apiUrl}/contact/message`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(contactInformation),
          });
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          this.submissions.push(contactInformation);
          return true;
        } catch (error) {
          console.error('Submission error:', error);
          if (error.response) {
            this.error = error.response.data.message;
          } else if (error.request) {
            this.error = 'No se recibió respuesta';
          } else {
            this.error = 'Error enviando el mensaje';
          }
          return false;
        } finally {
          this.loading = false;
        }
      },
    },
  });
  