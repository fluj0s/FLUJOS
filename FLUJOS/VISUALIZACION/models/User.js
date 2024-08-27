const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const UserSchema = new Schema({
  username: String,
  password: String,
  // Aquí puedes incluir cualquier metadato del usuario que necesites.
});

module.exports = mongoose.model('User', UserSchema);
