const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
app.use(bodyParser.json());
app.use(express.static('public'));

let content = {
    text: '',
    image: ''
};

// Đọc dữ liệu từ tệp JSON khi khởi động máy chủ
fs.readFile('content.json', (err, data) => {
    if (!err) {
        content = JSON.parse(data);
    }
});

app.get('/content', (req, res) => {
    res.json(content);
});

app.post('/content', (req, res) => {
    content.text = req.body.text;
    content.image = req.body.image;
    
    // Lưu dữ liệu vào tệp JSON
    fs.writeFile('content.json', JSON.stringify(content), (err) => {
        if (err) throw err;
    });

    res.sendStatus(200);
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
