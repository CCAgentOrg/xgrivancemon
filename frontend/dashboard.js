const API = '/api/v1';
async function loadStats() {
    const r = await fetch(API + '/stats');
    const d = await r.json();
    document.getElementById('total-agents').textContent = d.total_agents;
    document.getElementById('today-runs').textContent = d.today_runs;
    document.getElementById('complaints-24h').textContent = d.complaints_24h;
    document.getElementById('avg-response').textContent = d.avg_response_time + 'h';
}
async function loadRuns() {
    const r = await fetch(API + '/agent-runs?limit=10');
    const runs = await r.json();
    document.getElementById('runs').innerHTML = runs.map(run => 
        `<div class="bg-gray-800 p-3 rounded mb-2">${run.authority_handle}: ${run.complaints_collected} complaints</div>`
    ).join('');
}
loadStats();
loadRuns();
