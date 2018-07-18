const path = require('path')

module.exports = {
  secretKey: 'plasticgui-secret',
  development: {
    filesDir: path.join(__dirname, '..', 'files'),
    ip: 'localhost',
    port: 3000,
    db: {
      host: 'localhost',
      dialect: 'sqlite',
      storage: path.join(__dirname, '..', 'database.sqlite')
    },
    client: {
      host: 'http://localhost:8080'
    },
    email: {
      transport: {
        host: 'smtp.csiro.au',
        port: 25
      },
      resetEmail: 'group18@csiro.au'
    }
  }
}
