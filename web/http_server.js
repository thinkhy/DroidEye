var http = require('http');
var socketio = require('socket.io');
var fs = require('fs');
var exec = require('child_process').exec;

var handler = function(req, res) {
    fs.readFile(__dirname + '/index.html', function(err, data) {
        if (err) {
            res.writeHead(500);
            return res.end('Error loading index.html');
        } else {
            res.writeHead(200);
            res.end(data);
        }
    });
};

var app = http.createServer(handler);
var io = socketio.listen(app);


io.sockets.on('connection', function (socket) {
  setInterval(function() {
    var timestamp = Date.now();

    var command="ls -l ..|wc -l";	
    exec(command, function(error, stdout, stderr) {
       console.log('Emitted: ' + stdout);
       socket.emit('timer', stdout);
    });

    // socket.emit('timer', timestamp);
    
  }, 2000);
  socket.on('submit', function(data) {
    console.log('Submitted: ' + data);
  });
});

// use process.env.PORT and process.env.IP for Cloud9
// or replace with your port and (optionally) IP as necessary
console.log("listenning on port 8081");
app.listen(9999, "0.0.0.0");

console.log('Server running!');

