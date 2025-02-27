const config = {
  apiBaseUrl: process.env.REACT_APP_API_BASE_URL || 
    (process.env.NODE_ENV === 'production' 
      ? 'https://folioai-api-ebgjedcfgyhbfxhe.centralus-01.azurewebsites.net'
      : 'http://localhost:8000'),
  // Add other configuration variables here
};

export default config; 