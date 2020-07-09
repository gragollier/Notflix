const express = require('express');
const edgeNodeProviderServiceClient = require('../clients/edge_node_provider_service_client');
const metadataStorageServiceClient = require('../clients/metadata_storage_service_client');

const router = express.Router();

router.get('/location/:id', async (req, res) => {
    const id = req.params.id;
    const response = await edgeNodeProviderServiceClient.getEdgeNode(id);
    res.json(response);
});

router.get('/:id', async (req, res) => {
    const id = req.params.id;
    const response = await metadataStorageServiceClient.getVideoInfo(id);
    res.json(response);
});

module.exports = router;
