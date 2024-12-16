import LanguageUtils from './language_utils.js';
import TextToSpeechEngine from './text_to_speech_engine.js';

class SpeechRecognitionHandler {
    constructor(submitUrl, questionId, sessionId) {
        this.submitUrl = submitUrl;
        this.questionId = questionId;
        this.sessionId = sessionId;
        this.finalTranscript = '';
        this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        this.resultElement = document.getElementById('resultText');
        this.recordButton = document.getElementById('recordButton');
        this.feedbackContainer = document.getElementById('feedbackContainer');
        this.feedbackText = document.getElementById('feedbackText');
        this.processingFeedback = document.getElementById('processingFeedback');
        this.actionButtons = document.getElementById('actionButtons');
        this.loggingEnabled = false; // Set this to false to disable logging
        this.textToSpeechInstance = TextToSpeechEngine.getInstance(); // Ensure we use an instance

        this.setupRecognition();
        this.addRecordButtonListeners();
    }

    log(message) {
        if (this.loggingEnabled) {
            console.log(message);
        }
    }

    setupRecognition() {

        this.recognition.lang = LanguageUtils.getPreferredLanguage();
        this.recognition.interimResults = true;
        this.recognition.continuous = true;

        this.recognition.onresult = this.handleSpeechRecognitionResult.bind(this);
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.stopRecording();
        };
        //this.recognition.onend = this.stopRecording.bind(this);
         this.recognition.onend = () => {
            this.log('Recognition ended');
            //this.stopRecording();
        };
    }

    handleSpeechRecognitionResult(event) {
        this.interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                this.finalTranscript += transcript + ' ';
            } else {
                this.interimTranscript += transcript;
            }
        }
        this.resultElement.innerHTML = `${this.finalTranscript}<i style="color: #999;">${this.interimTranscript}</i>`;
    }

    startRecording() {
        this.log("startRecording")
        this.finalTranscript = '';
        this.recognition.lang = LanguageUtils.getPreferredLanguage();
        this.log('Recognizing in ' + this.recognition.lang);
        this.recognition.start();
        this.recordButton.textContent = 'Release to Stop';
        this.resultElement.textContent = '';
        this.feedbackContainer.style.display = 'none';
    }

    stopRecording() {

        this.log("stopRecording");

        this.recognition.stop();
        this.recordButton.textContent = 'Push to Answer';
        let completeText =this.finalTranscript+""+this.interimTranscript;
        if (completeText.trim()) {
            this.log("sending request!");
            this.sendTranscriptToServer(completeText.trim());
        }else {
            this.log("not sending request!");
        }
    }

    sendTranscriptToServer(transcript) {
        this.log("sendTranscriptToServer")
        this.processingFeedback.style.display = 'block';
        this.recordButton.disabled = true;

        const formData = new FormData();
        formData.append('text', transcript);
        formData.append('question_id', this.questionId);
        formData.append('session_id', this.sessionId);

        fetch(this.submitUrl, {
            method: 'POST',
            body: formData
        })
            .then(response => response.text())
            .then(result => this.handleFetchResponse(result))
            .catch(error => this.handleFetchError(error))
            .finally(() => this.handleFetchFinally());
    }

    handleFetchResponse(result) {
        this.processingFeedback.style.display = 'none';
        this.feedbackContainer.style.display = 'block';
        this.feedbackText.textContent = result;
        this.actionButtons.classList.remove('d-none');

        const autoReadCheckbox = document.getElementById('autoReadResults');
        if (autoReadCheckbox && autoReadCheckbox.checked) {
            this.textToSpeechInstance.speakWithoutBuffering(result);

        }
    }

    handleFetchError(error) {
        console.error('Error:', error);
        this.processingFeedback.style.display = 'none';
        this.feedbackContainer.style.display = 'block';
        this.feedbackText.textContent = 'Error: ' + error.message;
    }

    handleFetchFinally() {
        this.recordButton.disabled = false;
    }

    addRecordButtonListeners() {
        this.log("addRecordButtonListeners")
        this.recordButton.addEventListener('mousedown', this.startRecording.bind(this));
        this.recordButton.addEventListener('mouseup', this.stopRecording.bind(this));
        //this.recordButton.addEventListener('mouseleave', this.stopRecording.bind(this));

        // this.recordButton.addEventListener('touchstart', (e) => {
        //     e.preventDefault();
        //     this.startRecording();
        // });
        // this.recordButton.addEventListener('touchend', this.stopRecording.bind(this));
    }
}

window.initSpeechRecognition = (submitUrl, questionId, sessionId) => new SpeechRecognitionHandler(submitUrl, questionId, sessionId);
