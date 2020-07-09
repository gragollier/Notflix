const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');

const app = express();
const port = process.env.port || 4500;

app.use(bodyParser.json());
app.use(morgan("dev"));

app.get('/v1/video/:video_id', async (req, res) => {
    const id = req.params.video_id;
    res.json({
        mpd: `http://localhost:8080/${id}/${id}_dash.mpd`
    });
});

app.listen(port, () => {
    console.info(`Server started on port: ${port}`);
});
