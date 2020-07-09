const axios = require('axios');
const config = require('../utils/config');

const client = {};

client.getEdgeNode = async (id) => {
    const res = await axios.get(config.edgeNodeProviderService.host + `/v1/video/${id}`);
    return res.data;
}

module.exports = client;