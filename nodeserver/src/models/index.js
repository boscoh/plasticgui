'use strict'

const fs = require('fs')
const path = require('path')
const Sequelize = require('sequelize')
const env = process.env.NODE_ENV || 'development'
const config = require('../config')[env]

const basename = path.basename(__filename)

const models = {}

models.config = config.db
models.Sequelize = Sequelize
models.sequelize = new Sequelize(models.config.database, models.config.username, models.config.password, models.config)

models.unwrapInstance = function (instance) {
  if (instance === null) {
    return null
  } else {
    return instance.get({
      plain: true
    })
  }
}

models.sequelize.define()

fs
  .readdirSync(__dirname)
  .filter(file => {
    return (file.indexOf('.') !== 0) && (file !== basename) && (file.slice(-3) === '.js')
  })
  .forEach(file => {
    const model = models.sequelize['import'](path.join(__dirname, file))
    models[model.name] = model
  })

Object.keys(models).forEach(modelName => {
  if (models[modelName].associate) {
    models[modelName].associate(models)
  }
})

async function init () {
  await models.sequelize.sync()
  console.log('> Models.init done')
}

init()

module.exports = models
