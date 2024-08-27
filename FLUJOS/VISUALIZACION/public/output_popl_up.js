const { Client } = require('@elastic/elasticsearch');
const ForceGraph3D = require('3d-force-graph');
const fs = require('fs');
const path = require('path');

// Configuración de la conexión a Elasticsearch
const client = new Client({ node: 'http://localhost:9200' });

// Definir la clase Graph
class Graph {
  constructor(containerId) {
    this.graph = ForceGraph3D()(document.getElementById(containerId));
    this.maxNodes = 200; // Número máximo de nodos a mostrar inicialmente
    this.minSimilarity = 5; // Umbral mínimo de similitud por defecto (5%)
  }

  // Configurar el número máximo de nodos
  setMaxNodes(maxNodes) {
    this.maxNodes = maxNodes;
  }

  // Configurar el umbral mínimo de similitud
  setMinSimilarity(minSimilarity) {
    this.minSimilarity = minSimilarity;
  }

  // Cargar nodos desde Elasticsearch con filtros opcionales
  async loadNodes(subtematica = '', palabraClave = '', fechaInicio = '', fechaFin = '') {
    const query = {
      bool: {
        must: [
          { match: { tema: 'demografía' } }
        ],
        filter: []
      }
    };

    if (subtematica) {
      query.bool.must.push({ match: { subtema: subtematica } });
    }

    if (palabraClave) {
      query.bool.must.push({ match: { contenido: palabraClave } });
    }

    if (fechaInicio && fechaFin) {
      query.bool.filter.push({
        range: {
          fecha: {
            gte: fechaInicio,
            lte: fechaFin
          }
        }
      });
    }

    const response = await client.search({
      index: 'info',
      body: {
        query: query,
        size: this.maxNodes, // Limitar el número de resultados
        sort: { importancia: 'desc' } // Ordenar por importancia
      }
    });

    return response.body.hits.hits.map(hit => ({
      id: hit._source.archivo,
      group: hit._source.tipo,
      tema: hit._source.tema,
      content: hit._source.contenido,
      fecha: hit._source.fecha
    }));
  }

  // Cargar enlaces desde los archivos de relaciones
  loadLinks(relacionesPath) {
    const links = [];
    const archivosRelaciones = fs.readdirSync(relacionesPath);

    archivosRelaciones.forEach(archivo => {
      const fullPath = path.join(relacionesPath, archivo);
      const data = fs.readFileSync(fullPath, 'utf-8');
      const lines = data.split('\n');

      lines.forEach(line => {
        const [source, target, similarity] = line.split(',');
        if (parseFloat(similarity) >= this.minSimilarity) { // Filtrar por similitud mayor al umbral establecido
          links.push({
            source: path.basename(source, '.txt'),
            target: path.basename(target, '.txt'),
            value: parseFloat(similarity)
          });
        }
      });
    });

    return links;
  }

  // Crear los datos del gráfico
  createGraphData(nodes, links) {
    return {
      nodes,
      links
    };
  }

  // Mostrar el contenido del nodo al hacer hover o click
  showNodeContent(nodeContent) {
    const contentDiv = document.getElementById('contentDisplay');
    contentDiv.innerText = nodeContent;
  }

  // Configurar y dibujar el gráfico
  async drawGraph(relacionesPath, subtematica = '', palabraClave = '', fechaInicio = '', fechaFin = '') {
    const nodes = await this.loadNodes(subtematica, palabraClave, fechaInicio, fechaFin);
    const links = this.loadLinks(relacionesPath);
    const graphData = this.createGraphData(nodes, links);

    this.graph
      .graphData(graphData)
      .backgroundColor('black')
      .nodeLabel('id')
      .nodeAutoColorBy('group')
      .nodeVal(5)
      .linkColor(() => 'yellow') // Color de los enlaces
      .onNodeClick(node => {
        this.showNodeContent(node.content);
      })
      .onNodeHover(node => {
        if (node) {
          this.showNodeContent(node.content);
        }
      })
      .forceEngine('d3')
      .d3Force('charge').strength(-200)
      .d3Force('link').distance(50);
  }
}

// Uso
const myGraph = new Graph('canvasContainer');

// Manejar la lógica de la barra lateral
document.getElementById('paramForm').addEventListener('submit', function (event) {
  event.preventDefault(); // Evitar recarga de página

  const maxNodes = parseInt(document.getElementById('nodos').value);
  const subtematica = document.getElementById('param2').value;
  const palabraClave = document.getElementById('param1').value;
  const fechaInicio = document.getElementById('fecha_inicio').value;
  const fechaFin = document.getElementById('fecha_fin').value;
  const complejidad = parseInt(document.getElementById('complejidad').value);

  // Configurar el número máximo de nodos
  myGraph.setMaxNodes(maxNodes);

  // Configurar el umbral mínimo de similitud (ajustado con la barra de complejidad)
  const minSimilarity = 15 - complejidad * 1.25; // Rango de 15% a 2.5% dependiendo de la complejidad
  myGraph.setMinSimilarity(minSimilarity);

  // Dibujar el gráfico con los nuevos parámetros
  myGraph.drawGraph('/ruta/al/directorio/de/relaciones', subtematica, palabraClave, fechaInicio, fechaFin);
});

// Inicializar el gráfico con los parámetros por defecto
myGraph.drawGraph('/ruta/al/directorio/de/relaciones');
