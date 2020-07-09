const { Client } = require('@elastic/elasticsearch');
const config = require('../utils/config');

const client = new Client({
    node: config.elasticsearch.hosts,
    maxRetries: 10,
    requestTimeout: 30000
});

module.exports = client;