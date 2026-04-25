import api from './api';

export const checkHealth = async () => {
  const response = await api.get('/health');
  return response;
};

export const checkMLHealth = async () => {
  const response = await api.get('/ml/health');
  return response;
};