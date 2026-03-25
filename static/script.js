class UIController {
    constructor() {
        this.form = document.getElementById('predictForm');
        this.loader = document.getElementById('loader');
        this.predictBtn = document.getElementById('predictBtn');
        this.errorMsg = document.getElementById('formError');
        
        this.init();
    }

    init() {
        if (!this.form) return;

        // Auto-format numbers and validate on blur
        this.form.querySelectorAll('input[type="number"]').forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearError(input));
        });

        // Form Submission Interception
        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (this.validateAll()) {
                await this.submitData();
            }
        });
    }

    validateField(input) {
        let valid = true;
        const val = parseFloat(input.value);
        if (isNaN(val)) valid = false;
        if (input.id === 'tenure' && (val < 0 || val > 73)) valid = false;
        if (val < 0) valid = false;
        
        if (!valid) {
            input.classList.add('error-border');
        } else {
            input.classList.remove('error-border');
        }
        return valid;
    }

    clearError(input) {
        input.classList.remove('error-border');
        this.errorMsg.style.display = 'none';
    }

    validateAll() {
        let allValid = true;
        this.form.querySelectorAll('input[type="number"]').forEach(input => {
            if (!this.validateField(input)) allValid = false;
        });

        if (!allValid) {
            this.errorMsg.style.display = 'block';
            this.form.classList.add('shake');
            setTimeout(() => this.form.classList.remove('shake'), 400);
        }
        return allValid;
    }

    async submitData() {
        this.loader.classList.remove('hidden');
        this.predictBtn.style.opacity = '0';
        this.predictBtn.style.pointerEvents = 'none';
        
        // Let the CSS animation play a bit before navigating (simulate heavy processing visually for impact)
        setTimeout(() => {
            this.form.submit(); // Uses Native Form Post to render result.html directly (safest, highest compatibility backend-wise)
        }, 1200);
    }
}

// Shake Animation for errors
const style = document.createElement('style');
style.innerHTML = `
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-8px); }
  75% { transform: translateX(8px); }
}
.shake { animation: shake 0.4s ease-in-out; }
`;
document.head.appendChild(style);

document.addEventListener('DOMContentLoaded', () => {
    new UIController();
});
