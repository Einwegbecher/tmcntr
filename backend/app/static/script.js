let timerInterval;
let startTime;
let timerId;
let isRunning = false;

const timerDisplay = document.getElementById('timer-display');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const noteForm = document.getElementById('note-form');
const timerIdInput = document.getElementById('timer-id');

function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function updateTimer() {
    const now = new Date();
    const elapsedSeconds = Math.floor((now - startTime) / 1000);
    timerDisplay.textContent = formatTime(elapsedSeconds);
}

startBtn.addEventListener('click', async () => {
    if (isRunning) return;
    
    isRunning = true;
    startTime = new Date();
    
    // Start timer on server
    try {
        const response = await fetch('/start_timer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
        
        const data = await response.json();
        timerId = data.timer_id;
        timerIdInput.value = timerId;
        
        timerDisplay.classList.add('timer-running');
        startBtn.disabled = true;
        stopBtn.disabled = false;
        noteForm.style.display = 'block';
        
        timerInterval = setInterval(updateTimer, 1000);
    } catch (error) {
        console.error('Error starting timer:', error);
        isRunning = false;
    }
});

stopBtn.addEventListener('click', async () => {
    if (!isRunning) return;
    
    isRunning = false;
    clearInterval(timerInterval);
    
    timerDisplay.classList.remove('timer-running');
    startBtn.disabled = false;
    stopBtn.disabled = true;
    
    // Submit note form
    const note = document.getElementById('note').value;
    const formData = new FormData();
    formData.append('timer_id', timerId);
    formData.append('note', note);
    
    try {
        await fetch('/stop_timer', {
            method: 'POST',
            body: formData
        });
        
        // Reset form and display
        noteForm.reset();
        noteForm.style.display = 'none';
        timerDisplay.textContent = '00:00:00';
        
        // Refresh the page to show new entry
        window.location.reload();
    } catch (error) {
        console.error('Error stopping timer:', error);
    }
});

// Load recent slots on page load
async function loadRecentSlots() {
    try {
        const response = await fetch('/day?date=' + new Date().toISOString().split('T')[0]);
        const html = await response.text();
        // We'll just let the page load normally for now
    } catch (error) {
        console.error('Error loading recent slots:', error);
    }
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    // Auto-focus date inputs for better UX
    const dateInputs = document.querySelectorAll('input[type="date"], input[type="datetime-local"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            // Set to current date/time if empty
            if (input.type === 'datetime-local') {
                input.value = new Date().toISOString().slice(0, 16);
            } else {
                input.value = new Date().toISOString().split('T')[0];
            }
        }
    });
});
