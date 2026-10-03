// Unified API Client with Cookie Authentication Support

const BASE_URL = import.meta.env.VITE_API_URL || ''; // Relative path leverages Vite dev server proxy to localhost:8000

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  const config = {
    ...options,
    headers,
    credentials: 'include', // Ensures httpOnly cookies are included in every request
  };

  if (options.body && typeof options.body === 'object') {
    config.body = JSON.stringify(options.body);
  }

  const response = await fetch(url, config);

  if (!response.ok) {
    let errorDetail = 'Request failed';
    try {
      const errJson = await response.json();
      errorDetail = errJson.detail || errJson.message || errorDetail;
    } catch {
      errorDetail = response.statusText || errorDetail;
    }
    const error = new Error(errorDetail);
    error.status = response.status;
    throw error;
  }

  // Check if response has body
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    return await response.json();
  }
  return null;
}

// 1. Authentication
export const authApi = {
  register: (data) => request('/api/auth/register', { method: 'POST', body: data }),
  login: (data) => request('/api/auth/login', { method: 'POST', body: data }),
  logout: () => request('/api/auth/logout', { method: 'POST' }),
  me: () => request('/api/auth/me', { method: 'GET' }),
};

// 2. Projects
export const projectsApi = {
  list: () => request('/api/projects', { method: 'GET' }),
  get: (id) => request(`/api/projects/${id}`, { method: 'GET' }),
  create: (data) => request('/api/projects', { method: 'POST', body: data }),
  update: (id, data) => request(`/api/projects/${id}`, { method: 'PUT', body: data }),
  delete: (id) => request(`/api/projects/${id}`, { method: 'DELETE' }),
};

// 3. Tasks
export const tasksApi = {
  list: (projectId) => request(`/api/projects/${projectId}/tasks`, { method: 'GET' }),
  create: (projectId, data) => request(`/api/projects/${projectId}/tasks`, { method: 'POST', body: data }),
  update: (taskId, data) => request(`/api/tasks/${taskId}`, { method: 'PUT', body: data }),
  delete: (taskId) => request(`/api/tasks/${taskId}`, { method: 'DELETE' }),
};

// 4. Components / Cost Tracker
export const componentsApi = {
  list: (projectId) => request(`/api/projects/${projectId}/components`, { method: 'GET' }),
  create: (projectId, data) => request(`/api/projects/${projectId}/components`, { method: 'POST', body: data }),
  update: (componentId, data) => request(`/api/components/${componentId}`, { method: 'PUT', body: data }),
  delete: (componentId) => request(`/api/components/${componentId}`, { method: 'DELETE' }),
  costs: (projectId) => request(`/api/projects/${projectId}/costs`, { method: 'GET' }),
};

// 5. Portfolio
export const portfolioApi = {
  get: (projectId) => request(`/api/projects/${projectId}/portfolio`, { method: 'GET' }),
  update: (projectId, data) => request(`/api/projects/${projectId}/portfolio`, { method: 'PUT', body: data }),
  addSection: (projectId, data) => request(`/api/projects/${projectId}/portfolio/sections`, { method: 'POST', body: data }),
  deleteSection: (sectionId) => request(`/api/portfolio/sections/${sectionId}`, { method: 'DELETE' }),
  addMedia: (projectId, data) => request(`/api/projects/${projectId}/portfolio/media`, { method: 'POST', body: data }),
  deleteMedia: (mediaId) => request(`/api/portfolio/media/${mediaId}`, { method: 'DELETE' }),
};

// 6. Public Showcase (unauthenticated)
export const publicApi = {
  getPortfolio: (slug) => request(`/api/public/portfolio/${slug}`, { method: 'GET' }),
};
