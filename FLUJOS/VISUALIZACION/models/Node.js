const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const NodeSchema = new Schema({
  coordinates: { x: Number, y: Number, z: Number },
  type: String,
  // Aquí puedes incluir cualquier metadato del nodo que necesites.
});

module.exports = mongoose.model('Node', NodeSchema);
