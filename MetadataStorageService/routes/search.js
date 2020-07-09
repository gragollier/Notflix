const express = require('express');
const client = require('../elasticsearch/client');
const router = express.Router();

router.post('/user-search', async (req, res) => {
    const rawQuery = req.body.query;
    console.info(`Search query: ${rawQuery}`);

    const cleanedQuery = rawQuery.split('*').join('').split('?').join('');
    console.info(`Edited query: ${cleanedQuery}`);
    
    let body = { 
        "query": {
            "term": {
                "live": true
            }
        },
        size: 250
    };
    if (cleanedQuery) {
        body = {
            query: {
                bool: {
                    filter: {
                        bool: {
                            must: [
                                {
                                    "term": {
                                        "live": true
                                    }
                                }
                            ]
                        }
                    },
                    must: {
                        multi_match: {
                            query: cleanedQuery,
                            fields: [
                                "search_field^5",
                                "search_field.ngram"
                            ]
                        }    
                    }

                }
            },
            size: 250
        };
    }

    const result = await client.search({
        index: 'metadata',
        body: body
    });

    res.json(result.body.hits.hits.map(x => x["_source"]));
});

module.exports = router;
