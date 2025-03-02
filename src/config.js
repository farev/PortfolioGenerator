const config = {
  apiBaseUrl: process.env.NODE_ENV === 'production' 
    ? '/api'
    : 'http://localhost:8000',
  // Add other configuration variables here
};

export default config; 