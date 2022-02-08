# Overview

## Step 1: Register your app with Twitch

Go to: https://dev.twitch.tv/docs/authentication/#registration
Register your app with twitch following the instructions above. At the end of this process you will have an authentication (OAuth) token.
Alternatively you can go to: https://twitchapps.com/tmi/ as shortcut to generate a token.

1. Create a new application here: https://dev.twitch.tv/console/apps.
    - Enter https://localhost:8000
    - Go to "Manage" the application, and copy the `Client ID`
2. Start a local server, this will be used to exchange an authorization `code` for an access token.
2. Obtain an access token. In your browser go to:
GET https://id.twitch.tv/oauth2/authorize
    ?client_id=<your client ID>
    &redirect_uri=<your registered redirect URI>
    &response_type=code
    &scope=<space-separated list of scopes>

https://id.twitch.tv/oauth2/authorize
    ?client_id=kn1xf6cbrxtaqu0j9hz5tswgoz4dos
    &redirect_uri=https://localhost:8000
    &response_type=code
    &scope=channel:moderate%20chat:edit%20chat:read%20whispers:read%20whispers:edit

# Resources

* https://interactiveimmersive.io/blog/content-inputs/twitch-chat-in-touchdesigner/
* https://interactiveimmersive.io/blog/python/parsing-twitch-chat-commands-in-touchdesigner/