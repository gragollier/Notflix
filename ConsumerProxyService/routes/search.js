const express = require('express');
const metadataStorageServiceClient = require('../clients/metadata_storage_service_client');

const router = express.Router();

router.post('/search', async (req, res) => {
    const result = await metadataStorageServiceClient.userSearch(req.body);
    res.json(result);
});

module.exports = router;