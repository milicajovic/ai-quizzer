// mode_switcher.js

class ModeSwitcher {
    constructor() {
        this.modeToggle = document.getElementById('mode-toggle');
        this.modeLabel = this.modeToggle.nextElementSibling;
        this.init();
    }

    init() {
        if (this.modeToggle) {
            this.modeToggle.addEventListener('change', this.toggleMode.bind(this));
        }
    }

    toggleMode() {
        const newMode = this.modeToggle.checked ? 'text' : 'audio';
        const isToggle = true; // Dodaj is_toggle kao deo URL-a
        this.updateLabel(newMode); 
        const params = new URLSearchParams(window.location.search);
        params.set('set_mode', newMode);
        params.set('q_id', QUESTION_ID);
        window.location.href = `${window.location.pathname}?${params.toString()}`;
    }

    updateLabel(mode) {
        this.modeLabel.textContent = mode === 'text' ? 'Switch to Audio Mode' : 'Switch to Text Mode';
    }

    disableModeToggle() {
        if (this.modeToggle) {
            this.modeToggle.disabled = true;
        }
    }

    enableModeToggle() {
        if (this.modeToggle) {
            this.modeToggle.disabled = false;
        }
    }
}

export default new ModeSwitcher();