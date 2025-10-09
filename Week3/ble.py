#sudo env PATH="$PATH" python ble.py
from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(0.5)
n=0
addr = []
for dev in devices:
    print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
    addr.append(dev.addr)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print (" %s = %s" % (desc, value))
        
number = input('Enter your device number: ')
print ('Device', number)
num = int(number)
print (addr[num])
#
print ("Connecting...")
dev = Peripheral(addr[num], 'random')
#
print ("Services...")
for svc in dev.services:
    print (str(svc))
#
try:
    testService = dev.getServiceByUUID(UUID(0x1808))
    for ch in testService.getCharacteristics():
        pass
        #print (str(ch))
    #
    for ch in dev.getCharacteristics(uuid=UUID(0x2A34)):
        if (ch.supportsRead()):
            print (ch.read())
            descs = ch.getDescriptors()
            for desc in descs:
                print(desc.uuid.getCommonName(), desc.read())

                if (desc.uuid.getCommonName() == "Client Characteristic Configuration"):
                    pass
                    print(desc.uuid.getCommonName())
                    print("CCCD =", desc.read())
                    print(f"Trying to write {b'\x0001'} into CCCD....")
                    desc.write(b'\x01\x00', True)
                    print("Now CCCD =", desc.read())
                
            while True:
                if dev.waitForNotifications(1.0):
                    print("Get notification!")
                    continue
                print("Waiting")

    # try:
    #     dev.writeCharacteristic(0x2A34,bytes('aa','utf-8'), True)
    #     print("writing done")
    #     while True:
    #         if dev.waitForNotifications(1.0):
    #             print("Notification")
    #             continue
    #     print("Waiting")
    # finally:
    #     dev.disconnect()
    #     print ("Disconnected")
    #
finally:
    dev.disconnect() 
