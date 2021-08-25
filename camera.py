from smbus import SMBus

def colour():
    counter += 1
    bus.write_i2c_block_data(address, 0, data)
    block = bus.read_i2c_block_data(address, 0, 20)
    print(block, block[19])
    time.sleep(0.1)
    '''
    sig = block[7]*256 + block[6]
    x = block[9]*256 + block[8]
    y = block[11]*256 + block[10]
    w = block[13]*256 + block[12]
    h = block[15]*256 + block[14]
    '''
    #print("sig: {} | x: {} | y: {} | w: {} | h: {}".format(sig, x, y, w, h))