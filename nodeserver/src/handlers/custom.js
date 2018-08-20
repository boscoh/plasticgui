const models = require('../models')
const Custom = models.Custom
const unwrapInstance = models.unwrapInstance

async function createCustom (attr, data) {
  let custom = await Custom.create({
    attr,
    data
  })
  return unwrapInstance(custom)
}

function findCustom (CustomId) {
  return Custom.findOne({
    where: {
      id: CustomId
    }
  })
}

function fetchCustom (CustomId) {
  return findCustom(CustomId).then(unwrapInstance)
}

function deleteCustom (CustomId) {
  return Custom.destroy({
    where: {
      CustomId
    }
  })
}

async function saveCustom (CustomId, values) {
  let Custom = await findCustom(CustomId)
  let custom = await Custom.updateAttributes(values)
  return unwrapInstance(custom)
}

/**
 * Example of using Custom to record button pushes
 *
 * @returns {Promise<{attr: *}>}
 */
async function publicPushTask () {
  let customInstance = await Custom.findOne(
    {where: {type: 'task'}})

  if (!customInstance) {
    customInstance = await Custom.create(
      {attr: {n: 0}, type: 'task'})
  }

  let attr = customInstance.attr

  attr.n += 1
  customInstance.updateAttributes({attr})

  return {attr}
}

module.exports = {
  createCustom,
  findCustom,
  fetchCustom,
  deleteCustom,
  saveCustom,
  publicPushTask
}
