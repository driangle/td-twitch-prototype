
def onOffToOn(channel, sampleIndex, val, prev):
    # Unlocking to allow changes to the TOP
    op('tex3d2_usernames').lock = False
    op('tex3d2_usernames').par.prefill.pulse()
    # Locking to save on CPU time
    op('tex3d2_usernames').lock = True
    return