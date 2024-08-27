const User = require('../models/User');
const Post = require('../models/Post');
const Node = require('../models/Node');
const Flow = require('../models/Flow');
const Project = require('../models/Project');

module.exports = {
    users: async () => {
        //... tu código existente para obtener usuarios
    },

    posts: async () => {
        //... tu código existente para obtener posts
    },

    nodes: async () => {
        try {
            const nodes = await Node.find();
            return nodes.map(node => {
                return {
                    ...node._doc,
                    _id: node._id.toString(),
                    flow: getFlow.bind(this, node._doc.flow)
                };
            });
        } catch (err) {
            throw err;
        }
    },

    flows: async () => {
        try {
            const flows = await Flow.find();
            return flows.map(flow => {
                return {
                    ...flow._doc,
                    _id: flow._id.toString(),
                    nodes: getNodes.bind(this, flow._doc.nodes),
                    project: getProject.bind(this, flow._doc.project)
                };
            });
        } catch (err) {
            throw err;
        }
    },

    projects: async () => {
        try {
            const projects = await Project.find();
            return projects.map(project => {
                return {
                    ...project._doc,
                    _id: project._id.toString(),
                    flows: getFlows.bind(this, project._doc.flows)
                };
            });
        } catch (err) {
            throw err;
        }
    },
}

// Aquí necesitarías implementar las funciones auxiliares getPosts, getUser, getFlow, getNodes, getFlows y getProject.
