const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export interface MetricsSummary {
  window_days: number;
  success_rate: number;
  failure_rate: number;
  avg_build_time_seconds: number | null;
  last_build_status: string | null;
  last_updated: string;
}

export interface Build {
  id: number;
  external_id: string;
  status: string;
  branch: string;
  commit_sha: string | null;
  triggered_by: string | null;
  url: string | null;
  provider_id: number;
  duration_seconds: number | null;
  started_at: string | null;
  finished_at: string | null;
  raw_payload: any;
  created_at: string;
  provider_name: string | null;
  provider_kind: string | null;
}

export interface BuildListResponse {
  builds: Build[];
  total: number;
  limit: number;
  offset: number;
  has_more: boolean;
}

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  async getMetricsSummary(): Promise<MetricsSummary> {
    return this.request<MetricsSummary>('/api/metrics/summary');
  }

  async getBuilds(limit: number = 50, offset: number = 0, status?: string, provider?: string): Promise<BuildListResponse> {
    const params = new URLSearchParams({
      limit: limit.toString(),
      offset: offset.toString(),
    });

    if (status) params.append('status', status);
    if (provider) params.append('provider', provider);

    return this.request<BuildListResponse>(`/api/builds?${params.toString()}`);
  }

  async getBuild(id: number): Promise<Build> {
    return this.request<Build>(`/api/builds/${id}`);
  }

  async testAlert(message: string, apiKey: string): Promise<any> {
    return this.request('/api/alert/test', {
      method: 'POST',
      headers: {
        'X-API-KEY': apiKey,
      },
      body: JSON.stringify({ message }),
    });
  }

  async seedDatabase(apiKey: string, data?: any): Promise<any> {
    return this.request('/api/seed', {
      method: 'POST',
      headers: {
        'X-API-KEY': apiKey,
      },
      body: JSON.stringify(data || {}),
    });
  }
}

export const apiService = new ApiService();
export default apiService;
