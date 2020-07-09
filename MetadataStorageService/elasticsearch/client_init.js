const client = require('./client');
const initializeESMapping = require('./mapping_manager');

function client_init() {
    console.info("Setting timeout to initialize ES client in 15 seconds");
    setTimeout(() => {
        initializeESMapping();
    }, 15000);
}

module.exports = client_init;
