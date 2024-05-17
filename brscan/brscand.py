#!/usr/bin/env python3

# (C) 2013 Francois Cauwe
# (C) 2015-2018 Esben Haabendal

# Global libs
import sys
import time
import threading
import argparse
import socket
import yaml

from yaml import CLoader

# Private libs
from . import listen
from . import snmp


def main():
    print("YOLO")
    parser = argparse.ArgumentParser(
        description='Brother network scanner server')
    parser.add_argument('bind_addr', metavar='BIND_ADDR',
                        type=str,
                        help='IP/host to bind UDP socket to')
    parser.add_argument('-p', '--bind-port', metavar='PORT',
                        type=int, default=54925,
                        help='UDP port number to bind UDP socket to')
    parser.add_argument('-A', '--advertise-addr', metavar='ADDR',
                        type=str, default=None,
                        help='IP/host to advertise to scanner')
    parser.add_argument('-P', '--advertise-port', metavar='PORT',
                        type=int, default=None,
                        help='UDP port number to advertise to scanner')
    parser.add_argument('scanner_addr', metavar='SCANNER_ADDR',
                        type=str,
                        help='IP address of scanner')
    parser.add_argument('-c', '--config', metavar='FILE',
                        type=str, default='brother-scan.yaml',
                        help='Configuration file')
    args = parser.parse_args()
    if args.advertise_addr is None:
        args.advertise_addr = args.bind_addr
    if args.advertise_port is None:
        args.advertise_port = args.bind_port

    # Resolv hosts
    print("Resolving hosts...")
    args.bind_addr = socket.gethostbyname(args.bind_addr)
    args.advertise_addr = socket.gethostbyname(args.advertise_addr)
    args.scanner_addr = socket.gethostbyname(args.scanner_addr)

    # Loading global configuration
    print("Loading config...")
    try:
        with open(args.config) as configfile:
            config = yaml.load(configfile, Loader=CLoader)
    except FileNotFoundError as e:
        print('Error: %s: %s' % (e.strerror, e.filename))
        sys.exit(1)

    # Start Listen
    print("Starting 'Listen' thread...")
    listenThread = threading.Thread(target=listen.launch, args=(args, config))
    listenThread.start()
    time.sleep(1)

    # Start Snmp
    print("Starting 'SNMP' thread...")
    snmpThread = threading.Thread(target=snmp.launch, args=(args, config))
    snmpThread.start()

    # Wait for closing
    print("brscand started!")
    snmpThread.join()
    listenThread.join()


if __name__ == '__main__':
    main()
