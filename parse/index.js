var express = require('express');
var ParseServer = require('parse-server').ParseServer;
var ParseDashboard = require('parse-dashboard');
var path = require('path');

var databaseUri = process.env.DATABASE_URI || process.env.MONGODB_URI;

if (!databaseUri) {
  console.log('DATABASE_URI not specified, falling back to localhost.');
}

// Configuration
var app_id = process.env.APP_ID || 'pirates-online-rewritten';
var master_key = process.env.MASTER_KEY || 'b20IJn45;vwQM]V3!lUZ/x<4~tWWYC591L|{nTV&hJ3@i<u},7;)J`.Y1D~oqM3'; //Add your master key here. Keep it secret!
var server_url = process.env.SERVER_URL || 'http://127.0.0.1:1337/por-parse'; // Don't forget to change to https if needed
var app_name = process.env.APP_NAME || 'Pirates Online Rewritten';

// Parse Server
var api = new ParseServer({
  databaseURI: databaseUri || 'mongodb://localhost:27017/parse',
  cloud: process.env.CLOUD_CODE_MAIN || __dirname + '/cloud/main.js',
  appId: app_id,
  masterKey: master_key,
  serverURL: server_url,
  liveQuery: {
    classNames: ["Posts", "Comments"] // List of classes to support for query subscriptions
  }
});

//Parse Dashboard
var dashboard = new ParseDashboard({
    "apps": [
      {
        "serverURL": "http://127.0.0.1:1337/por-parse",
        "appId": "pirates-online-rewritten",
        "masterKey": "b20IJn45;vwQM]V3!lUZ/x<4~tWWYC591L|{nTV&hJ3@i<u},7;)J`.Y1D~oqM3",
        "clientKey": "test",
        "appName": "Pirates Online Rewritten",
        "iconName": "por.png",
        "production": true
      }
    ],
    "users": [
      {
          "user": "admin",
          "pass": "payagU4a"
      }
    ],
    "iconsFolder": "icons"
});

// Client-keys like the javascript key or the .NET key are not necessary with parse-server
// If you wish you require them, you can set them as options in the initialization above:
// javascriptKey, restAPIKey, dotNetKey, clientKey

var app = express();

// Serve static assets from the /public folder
app.use('/public', express.static(path.join(__dirname, '/public')));

// Serve the Parse API on the /por-parse URL prefix
var mountPath = process.env.PARSE_MOUNT || '/por-parse';
app.use(mountPath, api);
console.log('Starting api at prefix:' + mountPath);

// Server the Parse Dashboard on the /admin URL prefix
mountPath = process.env.DASHBOARD_MOUNT || '/admin';
app.use(mountPath, dashboard);
console.log('Starting dashboard at prefix:' + mountPath);

var port = process.env.PORT || 1337;
var httpServer = require('http').createServer(app);
httpServer.listen(port, function() {
    console.log('parse server running on port ' + port + '.');
});

// This will enable the Live Query real-time server
ParseServer.createLiveQueryServer(httpServer);
