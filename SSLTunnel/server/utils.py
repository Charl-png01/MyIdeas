import time
import datetime
import threading

from pypacker.layer4 import tcp

print_lock = threading.Lock()  # mutex lock for display access

def print_packet_meta(packet, ptype='', show_time=True):
    '''
    Print packet data
    packet: a pypacker IP object
    ptype: string indicating packet type
    show_time: whether to print current timestamp
    '''
    if packet.__class__.__name__ != "IP":
        print_msg("Cannot print non-IPv4 packet")

    if show_time:
        time_str = "\033[91m\033[1m%s\033[0m" % datetime.datetime.fromtimestamp(int(time.time()))
    else:
        time_str = ' '*19

    
    try:
        src_ip = packet.src_s
        dst_ip = packet.dst_s
    except:
        print_msg("Error parsing packet!")
        return

    try:
        src_port = packet[tcp.TCP].sport
        dst_port = packet[tcp.TCP].dport
        seq = hex(packet[tcp.TCP].seq)
        ack = hex(packet[tcp.TCP].ack)
    except:
        src_port = dst_port = seq = ack = 'NA'

    if ptype.startswith("I-")  or ptype.startswith("L-"):
        c_head = '\033[93m'
    elif ptype.startswith("T-"):
        c_head = '\033[96m'
    else:
        c_head = '\033[94m'


    with print_lock:
        print(time_str + "  " + c_head + ptype.ljust(8) + src_ip.ljust(16) + "    " + dst_ip.ljust(16) + "   ", end="")
        if src_port != 'NA':
            print(str(src_port)+" > "+str(dst_port) + "|" + seq + ":" + ack + '\033[0m')
        else:
            print("UDP\033[0m")


def print_msg(msg):
    '''
    Print a message with current timestamp
    msg: the message string
    '''
    time_str = "\033[91m\033[1m%s\033[0m" % datetime.datetime.fromtimestamp(int(time.time()))
    with print_lock:
        print(time_str + "  " + "\033[91m\033[1m" + msg + "\033[0m")


