const express = require('express');
const path    = require('path');

const app = express();

app.use(express.static(path.join(__dirname, 'public')));

app.use(express.json());

app.get('/api/scores',         require('./api/scores'));
app.get('/api/events',         require('./api/events'));
app.get('/api/digest/:date?',  require('./api/digest'));
app.get('/api/pending',        require('./api/pending'));
app.delete('/api/pending',     require('./api/pending'));
app.post('/api/monitor',       require('./api/monitor'));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Black Sea Monitor running at http://localhost:${PORT}`));
