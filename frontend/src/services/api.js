/**
 * API Service Layer
 * Handles all backend API communication
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Store session ID in memory
let sessionId = null;

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 120 second timeout to prevent infinite waiting
});

// Add request interceptor to include session ID
api.interceptors.request.use((config) => {
  if (sessionId) {
    config.headers['X-Session-ID'] = sessionId;
  }
  return config;
});

// Add response interceptor to capture session ID from upload and handle errors
api.interceptors.response.use(
  (response) => {
    // Capture session ID from upload response if present
    if (response.config.url === '/upload' && response.data.message) {
      const match = response.data.message.match(/session: ([a-f0-9-]+)/);
      if (match) {
        sessionId = match[1];
        console.log('Session ID captured:', sessionId);
      }
    }
    return response;
  },
  (error) => {
    // Enhanced error handling
    console.error('API Error:', error);
    
    // If session expired, clear it
    if (error.response?.status === 401) {
      sessionId = null;
    }
    
    // Return a more informative error
    const errorMessage = error.response?.data?.detail || error.message || 'An error occurred';
    return Promise.reject(new Error(errorMessage));
  }
);

/**
 * Upload a PDF document
 * @param {File} file - PDF file to upload
 * @param {string} companyName - Name of the company
 * @returns {Promise} Upload response with document_id
 */
export const uploadDocument = async (file, companyName) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('company_name', companyName);

  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * Extract claims from uploaded document
 * @param {string} documentId - Document identifier
 * @returns {Promise} Claims extraction response
 */
export const extractClaims = async (documentId) => {
  const response = await api.post('/extract-claims', null, {
    params: { document_id: documentId },
  });

  return response.data;
};

/**
 * Verify claims with external data
 * @param {string} documentId - Document identifier
 * @returns {Promise} Verification response with evidence
 */
export const verifyClaims = async (documentId) => {
  const response = await api.post('/verify', null, {
    params: { document_id: documentId },
  });

  return response.data;
};

/**
 * Calculate risk score
 * @param {string} documentId - Document identifier
 * @returns {Promise} Scoring response with risk score
 */
export const scoreClaims = async (documentId) => {
  const response = await api.post('/score', null, {
    params: { document_id: documentId },
  });

  return response.data;
};

/**
 * Get map data for facility locations
 * @param {string} documentId - Document identifier
 * @returns {Promise} Map data with facility locations
 */
export const getMapData = async (documentId) => {
  const response = await api.get(`/map-data/${documentId}`);
  return response.data;
};

/**
 * Health check
 * @returns {Promise} Health status
 */
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;

// Made with Bob
