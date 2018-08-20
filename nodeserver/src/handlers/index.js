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
    'filename': path.resolve('readme.md'),
    'data': {
      'success': true
    }
  }
  console.log('>> handlers.publicGetReadme', payload)
  return payload
}

async function publicDownloadLogo () {
  let payload = {
    'filename': path.resolve('../client/static/logo.png'),
    'data': {
      'success': true
    }
  }
  console.log('>> handlers.publicDownloadLogo', payload)
  return payload
}

async function deleteFileList (fileList) {
  for (let f of fileList) {
    if (fs.existsSync(f.path)) {
      console.log('>> handlers.deleteFileList', f.path)
      await del(f.path)
    }
  }
}

/**
 * Moves fileList to a time-stamped sub-directory in config.filesDir.
 * Optional checking function can throw Exceptions for bad files.
 * @param fileList
 * @promise - list of new paths
 */
async function storeFilesInConfigDir (fileList, checkFilesForError) {
  try {
    const timestampDir = String(new Date().getTime())
    const fullDir = path.join(config.filesDir, timestampDir)
    if (!fs.existsSync(fullDir)) {
      fs.mkdirSync(fullDir, 0o744)
    }

    if (checkFilesForError) {
      let error = checkFilesForError(fileList)
      if (error) {
        throw new Error(error)
      }
    }

    let targetPaths = []
    for (let file of fileList) {
      let basename = path.basename(file.originalname)
      let targetPath = path.join(timestampDir, basename)
      targetPaths.push(targetPath)

      let fullTargetPath = path.join(config.filesDir, targetPath)
      fs.renameSync(file.path, fullTargetPath)

      console.log(`>> handlers.storeFilesInConfigDir ${targetPath}`)
    }

    return targetPaths
  } catch (error) {
    await deleteFileList(fileList)
    throw error
  }
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
  publicUploadFiles,
})

module.exports = Object.assign(...handlers)
