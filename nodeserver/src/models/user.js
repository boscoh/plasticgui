'use strict'
const bcrypt = require('bcryptjs')

module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('User', {
    id: {
      primaryKey: true,
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4
    },
    name: DataTypes.STRING,
    email: {
      type: DataTypes.STRING,
      unique: true
    },
    password: {
      type: DataTypes.STRING,
      set (val) {
        let saltedPassword = bcrypt.hashSync(val, bcrypt.genSaltSync(10))
        this.setDataValue('password', saltedPassword)
      }
    },
    isAdmin: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false
    }
  })
  User.associate = function (models) {
    User.hasMany(models.Custom)
  }
  return User
}
