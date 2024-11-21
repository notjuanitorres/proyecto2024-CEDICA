import { defineStore } from "pinia";


export const useContactStore = defineStore('contact', {
    state: () => ({
        submissions: [],
        loading: false,
        error: null
    }),

    actions: {
        async submitContact(contactInformation) {
            this.loading = true;
            this.error = null;
            try {
                await new Promise(resolve => setTimeout(resolve, 1000));
                this.submissions.push(contactInformation);
                return true;
            } catch {
                this.error = "Failed to submit the contact form"
                return false 
            } finally {
                this.loading = false;
            }
        }
    }
})