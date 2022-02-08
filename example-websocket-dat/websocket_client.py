# me - this DAT
# dat - the WebSocket DAT

def onConnect(dat):
    print("onConnect")
    return

def onConnectionReady(dat):
    print("onConnectionReady")
    return

# me - this DAT
# dat - the WebSocket DAT

def onDisconnect(dat):
    print('onDisconnect')
    return

# me - this DAT
# dat - the DAT that received a message
# rowIndex - the row number the message was placed into
# message - a unicode representation of the text
# 
# Only text frame messages will be handled in this function.

def onReceiveText(dat, rowIndex, message):
    print('onReceiveText')
    print(message)
    return


# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message contents
# 
# Only binary frame messages will be handled in this function.

def onReceiveBinary(dat, contents):
    print('onReceiveBinary')
    print(contents)
    return

# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message contents
# 
# Only ping messages will be handled in this function.

def onReceivePing(dat, contents):
    print('onReceivePing')
    dat.sendPong(contents)
    return

# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message content
# 
# Only pong messages will be handled in this function.

def onReceivePong(dat, contents):
    print('onReceivePong')
    print(contents)
    return
    