const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.send('Estás en la página de usuarios.');
});

module.exports = router;
