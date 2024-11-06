// Validation patterns
const VALIDATION_PATTERNS = {
    letters: {
        pattern: /^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+(?:[\s'-]?[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+)*$/,
        message: 'Solo se permiten letras y espacios'
    },
    numbers: {
        pattern: /^[0-9]+$/,
        message: 'Solo se permiten números'
    },
    alphanumeric: {
        pattern: /^[A-Za-z0-9áéíóúñÁÉÍÓÚÑ\s\-\.]+$/,
        message: 'Solo se permiten letras, números, espacios y guiones'
    },
    email: {
        pattern: /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
        message: 'Ingrese un email válido'
    },
    phone: {
        pattern: /^\d{6,15}$/,
        message: 'El número debe tener entre 6 y 15 dígitos'
    },
    extended_phone: {
        pattern: /^[0-9\-\+\s\(\)]{8,20}$/,
        message: 'El número debe tener entre 8 y 20 dígitos'
    },
    decimal: {
        pattern: /^\d*\.?\d+$/,
        message: 'Ingrese un número decimal válido'
    },
    dni: {
        pattern: /^\d{8}$/,
        message: 'El DNI debe tener 8 dígitos'
    },
    country_code: {
        pattern: /^\d{1,3}$/,
        message: 'El código de país debe tener entre 1 y 3 dígitos'
    },
    area_code: {
        pattern: /^\d{1,4}$/,
        message: 'El código de área debe tener entre 1 y 4 dígitos'
    },
    phone_number: {
        pattern: /^\d{6,15}$/,
        message: "El número de teléfono debe tener entre 6 y 15 dígitos"
    },
    date: {
        pattern: /^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/(19|20)\d{2}$/,
        message: 'Ingrese una fecha válida en formato DD/MM/YYYY'
    },
    title: {
        pattern: /^.{0,100}$/,
        message: 'El titulo no puede exceder los 100 caracteres'
    },
    url: {
         pattern: /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/,
         message: 'Ingrese una URL válida'
    },
    no:{
        pattern: /^.*$/,
        message: 'Este campo es válido siempre'
    }
};

class FormValidator {
    constructor(form) {
        this.form = form;
        this.initialize();
    }

    initialize() {
        // Find all inputs that need validation
        const inputs = this.form.querySelectorAll('[data-validate]');
        
        // Add validation events to each input
        inputs.forEach(input => {
            input.addEventListener('input', () => this.validateInput(input));
            input.addEventListener('blur', () => this.validateInput(input));
        });

        // Add form submit validation
        this.form.addEventListener('submit', (e) => {
            let isValid = true;
            inputs.forEach(input => {
                if (!this.validateInput(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }

    validateInput(input) {
        const validations = input.dataset.validate.split(' ');
        const value = input.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Check if field is required
        if (validations.includes('required') && value === '') {
            isValid = false;
            errorMessage = 'Este campo es requerido';
        }

        // Check for maxLength in validations
        const maxLengthValidation = validations.find(v => v.startsWith('maxLength='));
        if (maxLengthValidation) {
            // Extract the maximum length value
            const maxLength = parseInt(maxLengthValidation.split('=')[1], 10);
            if (value.length > maxLength) {
                isValid = false;
                errorMessage = `Máximo ${maxLength} caracteres`;
            }
        }

        // Check for maxLength in validations
        const minLengthValidation = validations.find(v => v.startsWith('minLength='));
        if (minLengthValidation) {
            // Extract the minimum length value
            const minLength = parseInt(minLengthValidation.split('=')[1], 10);
            if (value.length < minLength) {
                isValid = false;
                errorMessage = `Mínimo ${minLength} caracteres`;
            }
        }

        // Check patterns
        for (const validation of validations) {
            if (VALIDATION_PATTERNS[validation] && value !== '') {
                if (!VALIDATION_PATTERNS[validation].pattern.test(value)) {
                    isValid = false;
                    errorMessage = VALIDATION_PATTERNS[validation].message;
                    break;
                }
            }
        }

        // Check date format and past-date if specified
        if (input.type === 'date' && validations.includes('past-date')) {
            const [year, month, day] = value.split('-');  // assuming ISO format YYYY-MM-DD from HTML date input
            const inputDate = new Date(year, month - 1, day);  // create Date object
            const today = new Date();
            today.setHours(0, 0, 0, 0);  // set today to start of day

            if (inputDate > today) {
                isValid = false;
                errorMessage = 'La fecha no puede ser futura';
            }
        }

        // Check min/max values for number inputs
        if (input.type === 'number') {
            const num = parseFloat(value);
            const min = parseFloat(input.dataset.min);
            const max = parseFloat(input.dataset.max);

            if (!isNaN(min) && num < min) {
                isValid = false;
                errorMessage = `El valor mínimo es ${min}`;
            }
            if (!isNaN(max) && num > max) {
                isValid = false;
                errorMessage = `El valor máximo es ${max}`;
            }
        }

        this.setInputStatus(input, isValid, errorMessage);
        return isValid;
    }

    setInputStatus(input, isValid, message = '') {
        // Remove existing status classes
        input.classList.remove('is-success', 'is-danger');

        // Add appropriate status class
        input.classList.add(isValid ? 'is-success' : 'is-danger');

        // Find or create help text element
        let helpElement = input.parentElement.querySelector('.help');
        if (!helpElement && message) {
            helpElement = document.createElement('p');
            helpElement.className = 'help';
            input.parentElement.appendChild(helpElement);
        }

        // Update help text
        if (helpElement) {
            helpElement.textContent = message;
            helpElement.classList.remove('is-success', 'is-danger');
            helpElement.classList.add(isValid ? 'is-success' : 'is-danger');
        }
    }
}

// Add CSS styles
document.head.insertAdjacentHTML('beforeend', `
    <style>
        .input.is-success, .select.is-success select {
            border-color: #48c774;
        }
        
        .input.is-danger, .select.is-danger select {
            border-color: #f14668;
        }
        
        .help.is-success {
            color: #48c774;
        }
        
        .help.is-danger {
            color: #f14668;
        }
    </style>
`);

// Initialize validation on all forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => new FormValidator(form));
});
