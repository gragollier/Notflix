const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const elasticsearchClientInit = require('./elasticsearch/client_init');

const app = express();
const port = process.env.port || 4000;

app.use(bodyParser.json());
app.use(morgan("dev"));

const searchRoute = require('./routes/search');
const storeRoute = require('./routes/store');

app.use('/v1/search', searchRoute);
app.use('/v1/store', storeRoute);

app.listen(port, () => {
    console.info(`Server started on port: ${port}`);
    
    console.info('Initializing Elasticsearch client');
    elasticsearchClientInit();
});
