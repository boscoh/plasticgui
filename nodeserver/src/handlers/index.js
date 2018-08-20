'use strict'
/**
 * Handlers are async functions that return a
 * JSON literal, or functions that return a Promise
 * that returns a JSON literal
 */

const fs = require('fs-extra')
const path = require('path')
const config = require('../config')

const basename = path.basename(__filename)
const dirname = path.dirname(__filename)
let handlers = []

fs
  .readdirSync(__dirname)
  .filter(file => {
    return (file.indexOf('.') !== 0) && (file !== basename) && (file.slice(-3) === '.js')
  })
  .forEach(file => {
    let handler = require(path.join(__dirname, file))
    handlers.push(handler)
  })

/**
 * App Specific handlers
 */

async function publicGetText () {
  return {
    'text': 'Example text from local webserver',
    'isRunning': true
  }
}

async function publicDownloadGetReadme () {
  let payload = {
    'filename': path.resolve(dirname, '../../../readme.md'),
    'data': {
      'success': true
    }
  }
  console.log('>> handlers.publicGetReadme', payload)
  return payload
}

async function publicDownloadLogo () {
  let payload = {
    'filename': path.resolve(dirname, '../../../client/static/logo.png'),
    'data': {
      'success': true
    }
  }
  console.log('>> handlers.publicDownloadLogo', payload)
  return payload
}

/**
 * Places uploaded files in the publicly accessible directory
 * config.development.filesDir using the timestamp as the
 * sub-directory for the files
 *
 * @param fileList
 * @returns {Promise<{files: Array}>}
 */
async function publicUploadFiles (fileList) {
  const timestampDir = String(new Date().getTime())
  const filesDir = config.development.filesDir

  const fullDir = path.join(filesDir, timestampDir)
  fs.ensureDirSync(fullDir)

  let targetPaths = []
  for (let file of fileList) {
    let basename = path.basename(file.originalname)
    let targetPath = path.join(timestampDir, basename)
    let fullTargetPath = path.join(filesDir, targetPath)
    fs.renameSync(file.path, fullTargetPath)
    targetPaths.push('/file/' + targetPath)
  }

  console.log('>> handlers.publicUploadFiles', targetPaths)
  return {files: targetPaths}
}

handlers.push({
  publicGetText,
  publicDownloadLogo,
  publicDownloadGetReadme,
  publicUploadFiles
})

module.exports = Object.assign(...handlers)
