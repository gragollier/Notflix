const express = require('express');
const elasticsearchClient = require('../elasticsearch/client');
const router = express.Router();

router.get('/video/:video_id', async (req, res) => {
    const id = req.params.video_id;
    try {
        const result = await elasticsearchClient.get({
            index: 'metadata',
            id: id
        });
        res.json(result.body._source);
    } catch (error) {
        console.error(`Error getting video by id: ${id}, ${error}`);
        res.sendStatus(500);
    }
});

router.post('/video', async (req, res) => {
    const id = req.body.id;
    const title = req.body.title;
    const subtitle = req.body.subtitle;
    const synopsis = req.body.synopsis;
    const live = false;
    const search_field = req.body.title + " " + req.body.synopsis;

    try {
        await elasticsearchClient.create({
            index: 'metadata',
            id: id,
            body: {
                id: id,
                title: title,
                subtitle: subtitle,
                synopsis: synopsis,
                search_field: search_field,
                live: live
            }
        });
        res.sendStatus(201);
    } catch (error) {
        console.error(`Error saving video: ${JSON.stringify(req.body)}, ${error}`);
        res.sendStatus(500);
    }
});

router.post('/video/:video_id/set_live', async (req, res) => {
    const id = req.params.video_id;
    await elasticsearchClient.update({
        index: 'metadata',
        id: id,
        body: {
            doc: {
                live: true
            }
        }
    });
    res.sendStatus(200);
});

module.exports = router;
