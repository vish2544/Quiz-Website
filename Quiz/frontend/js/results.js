// Results logic
checkAuth();

document.addEventListener('DOMContentLoaded', async () => {
    const score = Math.floor(Math.random() * 100);
    document.getElementById('scoreValue').textContent = score;
    
    const html = `
        <p><strong>Questions Attempted:</strong> 10</p>
        <p><strong>Correct Answers:</strong> 7</p>
        <p><strong>Wrong Answers:</strong> 3</p>
        <p><strong>Time Taken:</strong> 15:32</p>
        <p><strong>Feedback:</strong> Great job! You scored well on this quiz.</p>
    `;
    document.getElementById('resultsDetails').innerHTML = html;
});
