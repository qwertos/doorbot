import logging
from logging.handlers import SysLogHandler
from qrfid import *
from qschedule import Schedule
import fcntl
import socket
import struct
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('/opt/doorbot/config.ini')

botname = config["General"]["Botname"]
LATCH_DELAY = int(config["General"]["LatchDelay"])


# global app logging
#

botlog = logging.getLogger(botname)
hdlr = logging.FileHandler('%s.log' % botname)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
# the file log gets all but debug info
hdlr.setLevel(logging.INFO)
botlog.addHandler(hdlr) 


# define a Handler which writes all messages  to the sys.stderr
#
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
# root logger should handle everything
#
botlog.setLevel(logging.DEBUG)

# remote syslog
syslog = SysLogHandler(address=(config["Syslog"]["IP"], int(config["Syslog"]["Port"])))
formatter = logging.Formatter('%(asctime)s : %(message)s', datefmt='%b %d %H:%M:%S')
syslog.setFormatter(formatter)
botlog.addHandler(syslog)




# define the rfid reader device type
#
#READER_TYPE = 'hid'

READER_TYPE = config["Reader"]["Type"]
READER_DEVICE = config["Reader"]["Device"]
READER_BAUD_RATE = int(config["Reader"]["BaudRate"])

#READER_TYPE = 'tormach'
#READER_DEVICE = '/dev/ttyACM0'


# authenticate.py
#
AUTHENTICATE_TYPE = 'json'
AUTHENTICATE_CSV_FILE = 'databases/rfid/CardData.csv'
AUTHENTICATE_JSON_FILE = 'databases/rfid/acl.json'
AUTHENTICATE_FILE = AUTHENTICATE_JSON_FILE

# qschedule.py
# specify 'Open' for 24/7 access or 'HobbyistRestricted' for hobbyists on weekend/nights only
schedule = Schedule.factory('Open')

# door_hw.py
#
#
RED_PIN = int(config["Hardware"]["Red"])
GREEN_PIN = int(config["Hardware"]["Green"])
DOOR_PIN = int(config["Hardware"]["Door"])
BEEP_PIN = int(config["Hardware"]["Beep"])

# mqtt
#
#
def getMacAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
    return ''.join('%02x' % b for b in info[18:24])
            

mqtt_broker_address = config["MQTT"]["BrokerAddress"]
mqtt_broker_port = int(config["MQTT"]["BrokerPort"])
mqtt_ssl_ca_cert = config["MQTT"]["SSLCACert"]
mqtt_ssl_client_cert = config["MQTT"]["SSLClientCert"]
mqtt_ssl_client_key = config["MQTT"]["SSLClientKey"]
mqtt_node_id = getMacAddr('eth0')
mqtt_prefix = config["MQTT"]["Prefix"] + mqtt_node_id
mqtt_listen_topic = config["MQTT"]["ListenTopic"]
mqtt_acl_update_topic = config["MQTT"]["ACLUpdateTopic"]

# ACL update
acl_update_script='/home/pi/doorbot/databases/auto_door_list.sh'
