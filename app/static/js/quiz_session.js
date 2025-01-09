import QuizSessionTTS from './quiz_session_tts.js';
import TextToSpeechEngine from "./text_to_speech_engine.js";

class QuizSession {
    constructor() {
        this.loggingEnabled = true; // Set this to false to disable logging
        this.retryButton = document.getElementById('retryButton');
        this.nextQuestionButton = document.getElementById('nextQuestionButton');
        this.resultText = document.getElementById('resultText');
        this.actionButtons = document.getElementById('actionButtons');
        this.recordButton = document.getElementById('recordButton');

        this.setupEventListeners();
        // Initialize TTS with error logging
        this.initializeTTS().catch(error => {
            console.error('Failed to initialize TTS:', error);
        });
    }

    log(message) {
        if (this.loggingEnabled) {
            console.log(message);
        }
    }

    setupEventListeners() {
        if (this.retryButton) {
            this.retryButton.addEventListener('click', () => this.resetQuestion());
        } else {
            console.error("Retry Button not found")
        }

        if (this.nextQuestionButton) {
            this.nextQuestionButton.addEventListener('click', () => this.loadNextQuestion());
        } else {
            console.error("Next Question Button not found")
        }
    }

    async initializeTTS() {
        try {
            // Initialize TTS for the question
            const quizSessionTTS = await QuizSessionTTS.init();
            if (quizSessionTTS && typeof quizSessionTTS.readQuestion === 'function') {
                // Attempt to read the question
                quizSessionTTS.readQuestion();
            } else {
                this.log('QuizSessionTTS initialized but readQuestion is not available');
            }
        } catch (error) {
            console.error('Failed to initialize QuizSessionTTS:', error);
        }
    }

    resetQuestion() {
        // Reset the UI for retrying the current question
        this.resultText.textContent = '';
        //this.actionButtons.style.display = 'none';
        //this.recordButton.disabled = false;
        this.hideActionButtons();
        // Stop any ongoing TTS
        this.log('Stopping speech');
        const textToSpeechInstance = TextToSpeechEngine.getInstance();
        textToSpeechInstance.stopSpeaking();
        this.stopAudio();
    }

    stopAudio() {
        const audioPlayer = document.getElementById('audioPlayer');
        if (audioPlayer) {
            audioPlayer.pause(); // Pauziraj trenutnu reprodukciju
            audioPlayer.currentTime = 0; // Resetuj na početak
        }
    }

    showActionButtons() {
        if (this.actionButtons) {
            this.actionButtons.classList.remove('d-none');
        } else {
            console.error('Action buttons element not found');
        }
    }

    hideActionButtons() {
        if (this.actionButtons) {
            this.actionButtons.classList.add('d-none');
        } else {
            console.error('Action buttons element not found');
        }
    }

    loadNextQuestion() {
        // Proveri trenutni status "autoReadResults" iz localStorage
        const autoReadEnabled = localStorage.getItem('autoReadResults') === 'true';
        this.log(`Auto-read enabled for next question: ${autoReadEnabled}`);

        // Redirect to the next question
        if (typeof nextQuestionUrl !== 'undefined') {
            window.location.href = nextQuestionUrl;
            // Kada se novo pitanje učita, automatski ga pročitaj (ako je uključeno)
            if (autoReadEnabled) {
                // Koristi TTS za čitanje pitanja nakon učitavanja
                setTimeout(() => {
                    const quizSessionTTS = QuizSessionTTS; // Osiguraj da je TTS već inicijalizovan
                    if (quizSessionTTS && typeof quizSessionTTS.readQuestion === 'function') {
                        quizSessionTTS.readQuestion();
                    } else {
                        console.error('QuizSessionTTS or readQuestion is not available');
                    }
                }, 1000); // Dodaj mali delay ako je potrebno da se DOM osveži
            }

        } else {
            console.error('nextQuestionUrl is not defined');
        }
    }
}

// Initialize the QuizSession directly as the module will defer execution until the DOM is ready
// Create and export a singleton instance
const quizSessionInstance = new QuizSession();
export default quizSessionInstance;