// Quiz logic
checkAuth();

let currentQuestion = 0;
let answers = {};
let quizQuestions = [];

document.addEventListener('DOMContentLoaded', async () => {
    // Initialize quiz
    quizQuestions = [
        { id: 1, type: 'mcq', title: 'What is 2+2?', options: ['3', '4', '5', '6'], correct: 1 },
        { id: 2, type: 'coding', title: 'Write a function to sum two numbers', language: 'python' },
    ];
    
    displayQuestion();
    startTimer();
});

function displayQuestion() {
    if (currentQuestion >= quizQuestions.length) {
        submitQuiz();
        return;
    }
    
    const q = quizQuestions[currentQuestion];
    document.getElementById('questionTitle').textContent = q.title;
    
    if (q.type === 'mcq') {
        let html = '<div class="mcq-options">';
        q.options.forEach((opt, idx) => {
            html += `<label class="option-label"><input type="radio" name="answer" value="${idx}"> ${opt}</label>`;
        });
        html += '</div>';
        document.getElementById('questionContent').innerHTML = html;
    }
}

document.getElementById('nextBtn').addEventListener('click', () => {
    currentQuestion++;
    displayQuestion();
});

document.getElementById('submitBtn').addEventListener('click', submitQuiz);

function submitQuiz() {
    window.location.href = 'results.html';
}

function startTimer() {
    let timeLeft = 30 * 60;
    setInterval(() => {
        const mins = Math.floor(timeLeft / 60);
        const secs = timeLeft % 60;
        document.getElementById('timer').textContent = `Time: ${mins}:${secs.toString().padStart(2, '0')}`;
        timeLeft--;
        if (timeLeft < 0) submitQuiz();
    }, 1000);
}
