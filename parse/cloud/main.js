var request = require('request');

Parse.Cloud.define('ping', function(req, res) {
  res.success('pong');
});

Parse.Cloud.define('reportHacker', function(req, res) {
  //Grab Discord config info
  Parse.Config.get().then(function(config) {
    var config = Parse.Config.current();
    var discord_url = config.get('hacker_discord_url');

    if (discord_url == undefined) {
        console.log('Failed to post to Discord. hacker_discord_url is not defined');
        res.error('Failed to post to Discord. hacker_discord_url is not defined');
    }

    var message = (typeof req.params.message === undefined) ? '' : req.params.message;

    var config_username = config.get('discord_username');
    config_username = (typeof config_username === undefined) ? '' : config_username;
    var username = (typeof req.params.username === undefined) ? config_username : req.params.message;

    var config_icon_url = config.get('discord_icon_url');
    config_icon_url = (typeof config_icon_url === undefined) ? '' : config_icon_url;
    var icon_url = req.params.icon_url

    //Post to discord
    request.post(
      discord_url + '/slack',
      { json: {"text": message, "username": username, "icon_url": icon_url} },
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
