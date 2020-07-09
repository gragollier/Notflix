const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');

const searchRoute = require('./routes/search');
const videoRoute = require('./routes/video');

const app = express();
const port = process.env.port || 8000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false}));

app.use(morgan("dev"));

app.use('/api/v1/search', searchRoute);
app.use('/api/v1/video', videoRoute);

app.listen(port, () => {
    console.info(`Server started on port: ${port}`);
});
