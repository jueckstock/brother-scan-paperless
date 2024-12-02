from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
import time

def add_menu_entry(button, func, user, host, appnum,
                   duration=360, brid=''):
    global cmdGen, authData, transportTarget
    cmd = 'TYPE=BR;BUTTON=%s;USER="%s";FUNC=%s;HOST=%s;APPNUM=%s;DURATION=%s;BRID=%s;'%(button, user, func, host, appnum, duration, brid)
    #print('Registering:', cmd)
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
        authData, transportTarget,
        ('1.3.6.1.4.1.2435.2.3.9.2.11.1.1.0', rfc1902.OctetString(cmd))
    )
    # See http://www.oidview.com/mibs/2435/BROTHER-MIB.html

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1] or '?'))

def launch(args, config):
    global cmdGen, authData, transportTarget
    cmdGen = cmdgen.CommandGenerator()
    authData = cmdgen.CommunityData('internal', mpModel=0)
    transportTarget = cmdgen.UdpTransportTarget((args.scanner_addr, 161))
    addr = (args.advertise_addr, args.advertise_port)
    print('Advertising %s:%d to %s' % (addr + (args.scanner_addr,)))
    for func, users in config['menu'].items():
        for user, entry in users.items():
            print('Entry:', func.upper(), user, entry)
    while(1):
        appnum = 1
        for func, users in config['menu'].items():
            for user, entry in users.items():
                add_menu_entry('SCAN', func.upper(), user,
                               '%s:%d'%(addr), appnum)
                appnum += 1
        time.sleep(60)
