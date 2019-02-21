const models = require('../models')
const Custom = models.Custom
const unwrapInstance = models.unwrapInstance

async function createCustom(attr, data) {
  let custom = await Custom.create({ attr, data })
  return unwrapInstance(custom)
}

function findCustom(customId) {
  return Custom.findOne({ where: { id: customId } })
}

function fetchCustom(customId) {
  return findCustom(customId).then(unwrapInstance)
}

function deleteCustom(customId) {
  return Custom.destroy({ where: { id: customId } })
}

async function saveCustom(CustomId, values) {
  let Custom = await findCustom(CustomId)
  let custom = await Custom.updateAttributes(values)
  return unwrapInstance(custom)
}

async function getTaskCustom() {
  let customInstance = await Custom.findOne({ where: { type: 'task' } })
  if (!customInstance) {
    customInstance = await Custom.create({ attr: { n: 0 }, type: 'task' })
  }
  return unwrapInstance(customInstance)
}

/**
 * Example of using Custom to record button pushes
 *
 * @returns {Promise<{attr: *}>}
 */
async function publicPushTask() {
  let custom = await getTaskCustom()
  custom.attr.n += 1
  await saveCustom(custom.id, custom)
  return { attr: custom.attr }
}

module.exports = {
  createCustom,
  findCustom,
  fetchCustom,
  deleteCustom,
  saveCustom,
  publicPushTask
}
