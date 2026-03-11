// Dashboard JavaScript
const API_BASE = window.location.origin + '/api/v1';

// Fetch dashboard stats
async function loadStats() {
  try {
    const res = await fetch(`${API_BASE}/stats`);
    const stats = await res.json();
    
    document.getElementById('total-agents').textContent = stats.totalAgents || 0;
    document.getElementById('today-runs').textContent = stats.todayRuns || 0;
    document.getElementById('total-complaints').textContent = stats.totalComplaints || 0;
    document.getElementById('avg-response').textContent = (stats.avgResponseTime || 0) + 'h';
  } catch (e) {
    console.error('Failed to load stats:', e);
  }
}

// Fetch recent agent runs
async function loadAgentRuns() {
  try {
    const res = await fetch(`${API_BASE}/agent-runs`);
    const data = await res.json();
    const runs = data.agentRuns || [];
    
    const tbody = document.querySelector('#agent-runs tbody');
    tbody.innerHTML = runs.map(run => `
      <tr>
        <td>${run.agent_id}</td>
        <td>${new Date(run.created_at).toLocaleString()}</td>
        <td>${(run.duration_ms / 1000).toFixed(1)}s</td>
        <td><span class="badge ${run.status}">${run.status}</span></td>
        <td>${run.complaints_collected || 0}</td>
      </tr>
    `).join('');
  } catch (e) {
    console.error('Failed to load agent runs:', e);
  }
}

// Fetch complaints by authority
async function loadAuthorityChart() {
  try {
    const res = await fetch(`${API_BASE}/complaints/by-authority`);
    const data = await res.json();
    const authorities = data.complaintsByAuthority || [];
    
    // Simple bar chart
    const container = document.getElementById('authority-chart');
    const max = Math.max(...authorities.map(a => a.complaint_count), 1);
    
    container.innerHTML = authorities.slice(0, 6).map(auth => `
      <div class="bar-item">
        <span class="bar-label">${auth.name.substring(0, 15)}</span>
        <div class="bar" style="width: ${(auth.complaint_count / max * 100).toFixed(0)}%"></div>
        <span class="bar-value">${auth.complaint_count}</span>
      </div>
    `).join('');
  } catch (e) {
    console.error('Failed to load authority chart:', e);
  }
}

// Refresh all data
function refreshAll() {
  loadStats();
  loadAgentRuns();
  loadAuthorityChart();
}

// Initial load
document.addEventListener('DOMContentLoaded', () => {
  refreshAll();
  setInterval(refreshAll, 30000); // Auto-refresh every 30s
});
