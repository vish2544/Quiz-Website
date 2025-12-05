// Dashboard initialization
checkAuth();

document.addEventListener('DOMContentLoaded', async () => {
    const statsDiv = document.getElementById('stats');
    try {
        statsDiv.innerHTML = `
            <p>Total Quizzes: 0</p>
            <p>Average Score: 0%</p>
            <p>Rank: --</p>
        `;
    } catch (err) {
        statsDiv.innerHTML = `<p>Error loading stats: ${err.message}</p>`;
    }
});
