const client = require('./client');
const mapping = require('./mapping.json');

async function initializeESMapping() {
    for (const index in mapping) {
        try {
            console.info(`Writing mapping for ${index}: ${JSON.stringify(mapping[index])}`);
            await client.indices.create({
                index: index,
                body: mapping[index]
            });
        } catch (error) {
            console.info(`Error creating elasticsearch index (${index}), this is probably because it already exists: ${error}`);
        }
    }
}

module.exports = initializeESMapping;