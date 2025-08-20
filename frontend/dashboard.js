// CI/CD Health Dashboard JavaScript
const API_BASE = 'http://localhost:8000';

// DOM elements
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const dashboardContent = document.getElementById('dashboardContent');
const refreshBtn = document.getElementById('refreshBtn');

// Dashboard state
let currentBuilds = [];
let currentMetrics = null;
let autoRefreshInterval = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initialized, loading data...');
    loadDashboard();
    
    // Add refresh button event
    refreshBtn.addEventListener('click', loadDashboard);
    
    // Start auto-refresh
    startAutoRefresh();
});

// Main function to load dashboard data
async function loadDashboard() {
    try {
        console.log('Starting to load dashboard...');
        showLoading();
        
        // Test backend connectivity first
        console.log('Testing backend connectivity...');
        const healthCheck = await fetch(`${API_BASE}/health`);
        if (!healthCheck.ok) {
            throw new Error(`Backend health check failed: ${healthCheck.status}`);
        }
        console.log('Backend is healthy');
        
        // Load metrics and builds in parallel
        console.log('Fetching metrics and builds...');
        const [metrics, builds] = await Promise.all([
            fetchMetrics(),
            fetchBuilds()
        ]);
        
        console.log('Data fetched successfully:', { metrics, builds });
        
        // Update UI
        updateMetrics(metrics);
        updateBuildsTable(builds.builds || []);
        
        // Store current data
        currentMetrics = metrics;
        currentBuilds = builds.builds || [];
        
        showDashboard();
        updateLastUpdated();
        
    } catch (error) {
        console.error('Failed to load dashboard:', error);
        const errorMessage = error.message || 'Failed to fetch dashboard data';
        console.error('Error details:', errorMessage);
        showError(errorMessage);
    }
}

// Fetch metrics from API
async function fetchMetrics() {
    console.log('Fetching metrics from:', `${API_BASE}/api/metrics/summary`);
    const response = await fetch(`${API_BASE}/api/metrics/summary`);
    console.log('Metrics response status:', response.status);
    
    if (!response.ok) {
        const errorText = await response.text();
        console.error('Metrics API error:', errorText);
        throw new Error(`Metrics API error: ${response.status} - ${errorText}`);
    }
    
    const data = await response.json();
    console.log('Metrics data received:', data);
    return data;
}

// Fetch builds from API
async function fetchBuilds() {
    console.log('Fetching builds from:', `${API_BASE}/api/builds`);
    const response = await fetch(`${API_BASE}/api/builds`);
    console.log('Builds response status:', response.status);
    
    if (!response.ok) {
        const errorText = await response.text();
        console.error('Builds API error:', errorText);
        throw new Error(`Builds API error: ${response.status} - ${errorText}`);
    }
    
    const data = await response.json();
    console.log('Builds data received:', data);
    return data;
}

// Update metrics display
function updateMetrics(metrics) {
    if (!metrics) {
        console.warn('No metrics data to display');
        return;
    }
    
    console.log('Updating metrics display with:', metrics);
    
    // Update summary cards
    const successRateEl = document.getElementById('successRate');
    const failureRateEl = document.getElementById('failureRate');
    const avgBuildTimeEl = document.getElementById('avgBuildTime');
    const lastBuildStatusEl = document.getElementById('lastBuildStatus');
    
    if (successRateEl) {
        successRateEl.textContent = `${(metrics.success_rate * 100).toFixed(1)}%`;
    }
    
    if (failureRateEl) {
        failureRateEl.textContent = `${(metrics.failure_rate * 100).toFixed(1)}%`;
    }
    
    if (avgBuildTimeEl) {
        avgBuildTimeEl.textContent = metrics.avg_build_time_seconds ? 
            `${Math.round(metrics.avg_build_time_seconds / 60)}m` : 'N/A';
    }
    
    if (lastBuildStatusEl) {
        lastBuildStatusEl.textContent = metrics.last_build_status || 'Unknown';
    }
}

// Update builds table
function updateBuildsTable(builds) {
    console.log('Updating builds table with:', builds);
    const tbody = document.getElementById('buildsTableBody');
    
    if (!tbody) {
        console.error('Builds table body not found');
        return;
    }
    
    tbody.innerHTML = '';
    
    if (!builds || builds.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center" style="padding: 40px;">
                    No builds available
                </td>
            </tr>
        `;
        return;
    }
    
    builds.forEach(build => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>
                <span class="status-badge status-${build.status.toLowerCase()}">
                    ${build.status}
                </span>
            </td>
            <td>
                <strong>#${build.external_id}</strong><br>
                <small>${build.provider_name || 'Unknown Provider'}</small>
            </td>
            <td>${build.branch || 'main'}</td>
            <td>${formatDuration(build.duration_seconds)}</td>
            <td>${formatRelativeTime(build.started_at)}</td>
            <td>
                <button class="btn btn-secondary btn-sm" onclick="viewBuildDetails(${build.id})">
                    View Details
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Format duration in human readable format
function formatDuration(seconds) {
    if (!seconds) return '--';
    if (seconds < 60) return `${seconds}s`;
    if (seconds < 3600) return `${Math.round(seconds / 60)}m`;
    return `${Math.round(seconds / 3600)}h`;
}

// Format relative time
function formatRelativeTime(dateString) {
    if (!dateString) return '--';
    
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    
    return date.toLocaleDateString();
}

// View build details (simple alert for now)
function viewBuildDetails(buildId) {
    const build = currentBuilds.find(b => b.id === buildId);
    if (build) {
        const details = `
Build Details:
- ID: #${build.external_id}
- Status: ${build.status}
- Branch: ${build.branch || 'N/A'}
- Duration: ${formatDuration(build.duration_seconds)}
- Started: ${formatRelativeTime(build.started_at)}
- Provider: ${build.provider_name || 'Unknown'}
        `;
        alert(details);
    } else {
        alert(`Build with ID ${buildId} not found`);
    }
}

// Show/hide UI states
function showLoading() {
    console.log('Showing loading state');
    loadingState.style.display = 'block';
    errorState.style.display = 'none';
    dashboardContent.style.display = 'none';
}

function showError(message) {
    console.log('Showing error state:', message);
    document.getElementById('errorMessage').textContent = message;
    loadingState.style.display = 'none';
    errorState.style.display = 'block';
    dashboardContent.style.display = 'none';
}

function showDashboard() {
    console.log('Showing dashboard content');
    loadingState.style.display = 'none';
    errorState.style.display = 'none';
    dashboardContent.style.display = 'block';
}

// Auto-refresh functionality
function startAutoRefresh() {
    // Clear existing interval
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    
    // Start new interval (refresh every 30 seconds)
    autoRefreshInterval = setInterval(() => {
        console.log('Auto-refreshing dashboard...');
        loadDashboard();
    }, 30000);
    
    console.log('Auto-refresh started (30 second interval)');
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
        console.log('Auto-refresh stopped');
    }
}

// Update last updated timestamp
function updateLastUpdated() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    console.log(`Dashboard updated at: ${timeString}`);
}

// Network status handling
window.addEventListener('online', function() {
    console.log('Network connection restored');
    if (errorState.style.display === 'block') {
        loadDashboard();
    }
});

window.addEventListener('offline', function() {
    console.log('Network connection lost');
    showError('Network connection lost. Please check your internet connection.');
});

// Global error handling
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    showError(`JavaScript error: ${event.error?.message || 'Unknown error'}`);
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showError(`Promise error: ${event.reason?.message || 'Unknown promise error'}`);
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    stopAutoRefresh();
});
