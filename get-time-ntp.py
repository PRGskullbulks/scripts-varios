#-------------------------------------------------------------------------------
# Name:        getNTPTime
# Purpose:
#
# Author:      william.florez
#
# Created:     29/01/2021
# Copyright:   (c) william.florez 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
"""
Get NTP time from server, exceptions handled.
"""
from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time

timeout=10
host = "pool.ntp.org"

def getNTPTime(host = "horalegal.inm.gov.co"):
        port = 123
        buf = 1024
        address = (host,port)
        msg = '\x1b' + 47 * '\0'

        # reference time (in seconds since 1900-01-01 00:00:00)
        TIME1970 = 2208988800 # 1970-01-01 00:00:00

        # connect to server
        client = socket.socket( AF_INET, SOCK_DGRAM)
        client.settimeout(timeout)
        try:
            print("conectando a {0}".format(host))
            client.sendto(msg.encode('utf-8'), address)
            msg, address = client.recvfrom( buf )
        except socket.timeout:
            print("timeout conectando a {0}".format(host))
            exit()
        except socket.gaierror:
            print("error de DNS, el host {0} no se resuelve correctamente".format(host))
            exit()
        except ConnectionResetError:
            print("conexión rechazada por el host {0}".format(host))
            exit()


        t = struct.unpack( "!12I", msg )[10]
        t -= TIME1970
        client.close()
        return time.ctime(t).replace("  "," ")

if __name__ == "__main__":
        print("la hora es: " + getNTPTime(host))