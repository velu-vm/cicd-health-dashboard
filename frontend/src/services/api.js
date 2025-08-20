const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async getMetricsSummary() {
    return this.request('/api/metrics/summary');
  }

  async getBuilds(limit = 50, offset = 0, status = '', branch = '') {
    const params = new URLSearchParams();
    if (limit) params.append('limit', limit);
    if (offset) params.append('offset', offset);
    if (status) params.append('status', status);
    if (branch) params.append('branch', branch);
    
    return this.request(`/api/builds?${params.toString()}`);
  }

  async getBuild(id) {
    return this.request(`/api/builds/${id}`);
  }

  async testAlert(channel, message, severity = 'info') {
    return this.request('/api/alert/test', {
      method: 'POST',
      body: JSON.stringify({ channel, message, severity }),
    });
  }

  async seedDatabase() {
    return this.request('/api/seed', {
      method: 'POST',
      body: JSON.stringify({}),
    });
  }
}

export const apiService = new ApiService();
