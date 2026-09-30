'use strict';

const express = require('express');
const cors = require('cors');

const PORT = 90;
const HOST = '0.0.0.0';

var charcount = require('./charcount');

const app = express();
app.use(cors());

app.get('/', (req, res) => {
    const text = req.query.text;
    if (text !== undefined && typeof text !== "string") {
        return res.status(400).json({ error: "text must be a string" });
    }

    if (text) {
        const answer = charcount.counter(text);

        const output = {
            'error': false,
            'string': `Contains ${answer} characters`,
            'answer': answer
        };

        res.json(output);
    } else {
        res.send('charcount is running');
    }
});

app.listen(PORT, HOST, () => {
    console.log(`Server is running at http://${HOST}:${PORT}`);
});
