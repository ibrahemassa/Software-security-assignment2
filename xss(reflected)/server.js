let http = require('http');
let url = require('url');
let fs = require('fs');

const PORT = 8080;

function clean(input){
  return input.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&apos;');
}

http.createServer(function(request, response) {
    let filename = './index.html';

    fs.readFile(filename, 'utf8', function(err, html) {
        if (err) {
            response.writeHead(404, { 'Content-Type': 'text/html' });
            return response.end('404 Not Found!');
        }

        let url_parts = url.parse(request.url, true);
        let params = url_parts.query;

        let paramHTML = '';
        for (let key in params) {
            clean_key = clean(key);
            clean_key_val = clean(params[key]);
            paramHTML += `${clean_key}: ${clean_key_val}<br>`;
        }
        

        if(paramHTML){
            html = html.replace('URL parameters will be displayed here.', paramHTML);
        }
        

        response.writeHead(200, { 'Content-Type': 'text/html' });
        response.write(html);
        response.end();
    });
}).listen(PORT);

console.log('Server running at http://localhost:' + PORT + '/');
