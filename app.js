
var express = require('express')
var app = express()
var port = process.env.VCAP_APP_PORT || 3000;
var path = require('path');
var server = require('http').createServer(app);
var io = require('socket.io')(server);
var bodyParser = require('body-parser');
var multer  = require('multer');
var upload = multer({ dest: 'uploads/' });
var fs = require('fs');
app.use(express.static('public'))

// ----
var sessions = {};

//Auth ----
var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/')
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '.jpg') //Appending .jpg
  }
})

var upload = multer({ storage: storage });

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.get('/', function(req, res){
  res.sendFile(path.join(__dirname,'/index.html'));
});

app.post('/upload', upload.single('image'), function (req, res, next) {
    
    var filename = req.file.filename;



}); 

io.on('connection', function(socket) {
  console.log("Client connect at " + socket.id);

  sessions[socket.id] = {};


  socket.on('disconnect', function(item) {
    console.log("disconnected from client " + socket.id);
    delete sessions[socket.id];
    //update dashboard sockets 
  });

  socket.on('broadcastDraw', function(data){
    Object.keys(io.sockets.sockets).forEach(function(item) {
      if (item != socket.id) {
        io.to(item).emit('draw', data)
      }
  });
  })
});

server.listen(port, function () {
  console.log("server running on port: " + port.toString())
})

