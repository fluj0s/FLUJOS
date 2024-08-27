const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const FlowSchema = new Schema({
  sourceNode: { type: Schema.Types.ObjectId, ref: 'Node' },
  targetNode: { type: Schema.Types.ObjectId, ref: 'Node' },
  intensity: Number,
  // Aquí puedes incluir cualquier metadato del flujo que necesites.
});

module.exports = mongoose.model('Flow', FlowSchema);
