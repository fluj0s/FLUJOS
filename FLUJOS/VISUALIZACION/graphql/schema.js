const { buildSchema } = require('graphql');

module.exports = buildSchema(`
    type User {
        _id: ID!
        name: String!
        email: String!
        posts: [Post!]
    }

    type Post {
        _id: ID!
        title: String!
        content: String!
        creator: User!
    }

    type Node {
        _id: ID!
        name: String!
        flow: Flow!
    }

    type Flow {
        _id: ID!
        nodes: [Node!]!
        project: Project!
    }

    type Project {
        _id: ID!
        flows: [Flow!]!
    }

    type RootQuery {
        users: [User!]!
        posts: [Post!]!
        nodes: [Node!]!
        flows: [Flow!]!
        projects: [Project!]!
    }

    schema {
        query: RootQuery
    }
`);





// export const newsData = [
//     {
//       "id": "1",
//       "title": "BlackRock adquiere empresa de tecnología financiera",
//       "shares": 3500
//     },
//     {
//       "id": "2",
//       "title": "BlackRock lanza nuevo fondo de inversión en energías renovables",
//       "shares": 2900
//     },
//     {
//       "id": "3",
//       "title": "BlackRock reporta ganancias record en el último trimestre",
//       "shares": 4000
//     },
//     {
//       "id": "4",
//       "title": "BlackRock lidera ronda de financiamiento en startup de inteligencia artificial",
//       "shares": 2100
//     },
//     {
//       "id": "5",
//       "title": "CEO de BlackRock promueve inversiones sostenibles en cumbre global",
//       "shares": 2600
//     },
//     {
//       "id": "6",
//       "title": "BlackRock apunta a mercados emergentes con nuevo producto de inversión",
//       "shares": 2800
//     },
//     {
//       "id": "7",
//       "title": "BlackRock se compromete a reducir su huella de carbono en un 50% para 2030",
//       "shares": 3500
//     },
//     {
//       "id": "8",
//       "title": "BlackRock lidera el mercado de ETFs con fuerte crecimiento en el último año",
//       "shares": 3900
//     },
//     {
//       "id": "9",
//       "title": "BlackRock anuncia inversión millonaria en infraestructura de blockchain",
//       "shares": 3300
//     },
//     {
//       "id": "10",
//       "title": "BlackRock apoya iniciativa de transparencia financiera en G20",
//       "shares": 3000
//     }
//   ];
  