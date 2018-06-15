const models = require('../models')
const bcrypt = require('bcryptjs')

const User = models.User

function createUser (values) {
  return User.findOne({
    where: {
      id: values.id
    }
  }).then(user => {
    if (user === null) {
      return User.create(values).then(models.unwrapInstance)
    }
  })
}

function updateUser (values) {
  return User.findOne({
    where: {
      id: values.id
    }
  }).then(user => {
    if (user) {
      return user.updateAttributes(values).then(models.unwrapInstance)
    } else {
      return null
    }
  })
}

function fetchUser (values) {
  return User.findOne({
    where: values
  }).then(user => {
    if (user) {
      return models.unwrapInstance(user)
    } else {
      return null
    }
  })
}

function checkUserWithPassword (user, password) {
  return new Promise(resolve => {
    bcrypt.compare(password, user.password, (err, isMatch) => {
      if (err) {
        resolve(null)
      } else if (isMatch) {
        resolve(user)
      } else {
        resolve(null)
      }
    })
  })
}

async function publicRegisterUser (user) {
  let errors = []
  if (!user.name) {
    errors.push('no user name')
  }
  if (!user.email) {
    errors.push('no email')
  }
  if (!user.password) {
    errors.push('no Password')
  }

  if (errors.length > 0) {
    throw errors.join(', ').join(errors)
  }

  let values = {
    name: user.name,
    email: user.email,
    password: user.password
  }

  try {
    await createUser(values)
    return {
      success: true
    }
  } catch (e) {
    throw new Error('Couldn\'t register, is your email already in use?')
  }
}

/**
 * Updates user where the id field is used to identify the user.
 * @param {Object} user
 * @promise {User}
 */
async function loginUpdateUser (user) {
  const keys = ['id', 'name', 'email', 'password']
  let values = {}
  for (let key of keys) {
    if (user[key]) {
      values[key] = user[key]
    }
  }
  if (!values) {
    throw new Error('No values to update')
  }
  if (!values.id) {
    throw new Error('No user.id to identify user')
  }

  try {
    console.log('>> handlers.updateUser', values)
    await updateUser(values)
    return {
      success: true
    }
  } catch (err) {
    throw new Error('Couldn\'t update user - ' + err.toString())
  }
}

async function publicResetPassword (tokenId, password) {
  let values = {
    id: tokenId,
    password
  }
  if (!values.id) {
    throw new Error('No user.id to identify user')
  }

  try {
    console.log('>> handlers.publicResetPassword', values)
    await updateUser(values)
    return {
      success: true
    }
  } catch (err) {
    throw new Error(`Update failure ${err}`)
  }
}

module.exports = {
  createUser,
  fetchUser,
  updateUser,
  checkUserWithPassword,
  publicRegisterUser,
  loginUpdateUser,
  publicResetPassword
}
