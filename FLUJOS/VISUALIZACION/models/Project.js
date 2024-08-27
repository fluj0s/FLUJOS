const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ProjectSchema = new Schema({
  user: { type: Schema.Types.ObjectId, ref: 'User' },
  nodes: [{ type: Schema.Types.ObjectId, ref: 'Node' }],
  flows: [{ type: Schema.Types.ObjectId, ref: 'Flow' }],
  // Aquí puedes incluir cualquier metadato del proyecto que necesites.
});

module.exports = mongoose.model('Project', ProjectSchema);


