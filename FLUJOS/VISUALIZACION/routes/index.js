//Las rutas en Express.js son maneras de definir cómo responde tu aplicación a las solicitudes de los clientes 
//en ciertos endpoints URI,
// que son caminos o rutas a los que los clientes pueden acceder. Las rutas pueden ser creadas y manejadas en el archivo principal de tu aplicación
//, pero para proyectos más grandes, generalmente se separan en su propio archivo o módulo para mantener el código organizado y legible.
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.send('Estás en la página de inicio.');
});

module.exports = router;
