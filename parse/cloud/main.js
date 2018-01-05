var request = require('request');

Parse.Cloud.define('hello', function(req, res) {
  res.success('Hi');
});

Parse.Cloud.define('reportHacker', function(req, res) {

  //Grab Discord hacker log url
  Parse.Config.get().then(function(config) {
    var config = Parse.Config.current();
    var discord_url = config.get('hacker_discord_url');

    if (discord_url == undefined) {
        console.log('Failed to post to Discord. hacker_discord_url is not defined');
        res.error('Failed to post to Discord. hacker_discord_url is not defined');
    }

    //Post to discord
    request.post(
      discord_url + '/slack',
      { json: {"text": "Hello World!", "username": "Parse", "icon_url": "https://seeklogo.com/images/P/parse-logo-2D3985615E-seeklogo.com.png"} },
      function(error, response, body) {
        if (error) {
          res.error(body);
        } else {
          res.success(config.result);
        }
      });
  }, function(error) {
      console.log('Failed to fetch config.');
      res.error('Failed to fetch parse config. Webhook not posted');
  });
});
