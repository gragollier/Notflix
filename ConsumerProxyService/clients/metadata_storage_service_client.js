const axios = require('axios');
const config = require('../utils/config');

const client = {};

client.userSearch = async (body) => {
    const res = await axios.post(config.metadataStorageService.host + '/v1/search/user-search', body);
    return res.data;
}

client.getVideoInfo = async (id) => {
    const res = await axios.get(config.metadataStorageService.host + '/v1/store/video/' + id);
    return res.data;
}

module.exports = client;
