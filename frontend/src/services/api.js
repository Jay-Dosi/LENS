/**
 * API Service Layer
 * Handles all backend API communication
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
 * Health check
 * @returns {Promise} Health status
 */
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;

// Made with Bob
