const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    chromeWebSecurity: false,
    env: {
      DB_URI: 'mysql+pymysql://admin:spmg8t8password@database-spm.ct8js8kifsfg.ap-southeast-1.rds.amazonaws.com:3306/spm',
      VITE_BASE_URL: 'http://0.0.0.0:8000'
    },
  },
})