// https://eslint.org/docs/user-guide/configuring

module.exports = {
  root: true,
  parserOptions: {
    parser: 'babel-eslint',
    ecmaVersion: 2017
  },
  env: {
    browser: false
  },
  extends: ['prettier-standard']
}
