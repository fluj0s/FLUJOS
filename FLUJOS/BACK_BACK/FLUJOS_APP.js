const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const { Client } = require('@elastic/elasticsearch');

let fetch;

// Importa node-fetch de forma dinámica
import('node-fetch').then(module => {
    fetch = module.default;
});

const app = express();
const port = 3000;

const client = new Client({ node: 'http://localhost:9200' });

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, '../VISUALIZACION/public')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../VISUALIZACION/public'));
});

const indexRoutes = require('../VISUALIZACION/routes/index');
const userRoutes = require('../VISUALIZACION/routes/users');
app.use('/', indexRoutes);
app.use('/users', userRoutes);

app.post('/add-news', async (req, res) => {
    const news = req.body;

    // Solicitar datos procesados de Flask
    const response = await fetch("http://localhost:5000/process-news", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(news)
    });

    const processedData = await response.json();

    // Combina la noticia original con los datos procesados
    const combinedData = {
        ...news,
        processedData: processedData
    };

    try {
        await client.index({
            index: 'news-index',
            body: combinedData
        });
        res.send({ message: 'News added successfully' });
    } catch (error) {
        res.status(500).send({ message: 'Error adding news to Elasticsearch', error });
    }
});

app.get('/search-news', async (req, res) => {
    const keyword = req.query.keyword;

    try {
        const { body } = await client.search({
            index: 'news-index',
            body: {
                query: {
                    match: { title: keyword }
                }
            }
        });
        res.send(body.hits.hits);
    } catch (error) {
        res.status(500).send({ message: 'Error searching news in Elasticsearch', error });
    }
});

app.listen(port, () => {
    console.log(`La aplicación está escuchando en http://localhost:${port}`);
});

