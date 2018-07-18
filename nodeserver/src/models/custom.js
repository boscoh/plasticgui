const SequelizeJson = require('sequelize-json')

module.exports = (sequelize, DataTypes) => {
  const Custom = sequelize.define('Custom', {
    id: {
      primaryKey: true,
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4
    },
    attr: SequelizeJson(sequelize, 'Custom', 'attr'),
    type: DataTypes.STRING,
    data: DataTypes.BLOB
  })
  Custom.associate = function (models) {
    Custom.belongsTo(models.User)
  }
  return Custom
}
