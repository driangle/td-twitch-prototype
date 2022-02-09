
DEBUG = False
DEFAULT_READONLY_BOT_NICKNAME = 'justinfan12345'

def onConnect(dat):
    global DEFAULT_READONLY_BOT_NICKNAME
    parameters = me.parent().par
    nickname = parameters.Botnickname if parameters.Botnickname else DEFAULT_READONLY_BOT_NICKNAME
    channel_name = parameters.Channelname
    access_token = parameters.Accesstoken
    auth_mode = 'authenticated' if access_token else 'anonymous'

    print('[twitch_websocket] Connected')
    print(f'[twitch_websocket] Joining channel [{channel_name}] as user [{nickname}], auth_mode: [{auth_mode}]')
    
    if access_token:
        oauth_token = f'oauth:{access_token}'
        dat.sendText('PASS {}'.format(oauth_token))
    dat.sendText('NICK {}'.format(nickname))
    dat.sendText('JOIN #{}'.format(channel_name))
    # dat.sendText('CAP REQ :twitch.tv/membership') # Request for an update on channel membership every 10 seconds
    # dat.sendText('CAP REQ :twitch.tv/commands') # Enables several Twitch-specific commands.
    dat.sendText('CAP REQ :twitch.tv/tags') # Adds IRC V3 message tags to several commands, if enabled with the commands capability.
    return

def onDisconnect(dat):
    print('[twitch_websocket] Disconnected')
    return


def onReceiveText(dat, rowIndex, data):
    global DEBUG
    if DEBUG:
        print('[twitch_websocket] onReceiveText ' + str(data))
    groups = data.split()
    # Message Format :<user>!<user>@<user>.tmi.twitch.tv PRIVMSG #<channel> :<message>
    if len(groups) >=3 and groups[2] == "PRIVMSG":
        message = " ".join(groups[4:]).lstrip(":")
        username = groups[1].split('!')[0].lstrip(":")
        tags = dict([tuple(tag.split('=')) for tag in groups[0].split(';')])
        op('fifo_messages').appendRow([username, tags['color'], message])
    return

def onReceivePing(dat, contents):
    dat.sendPong(contents)
    return

    