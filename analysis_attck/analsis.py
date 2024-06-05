import pyshark

# Load the pcapng file
file_path = 'irc_backdoor_exploit.pcapng'
capture = pyshark.FileCapture(file_path)

# Initialize variables
attacker_ip = None
victim_ip = None
attack_port = None
attack_attempts = 0
attack_payload_packets = []

# Loop through the packets to identify the details
for packet in capture:
    try:
        # Extract IP layer information
        ip_layer = packet['ip']
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst

        # Extract TCP layer information
        tcp_layer = packet['tcp']
        src_port = tcp_layer.srcport
        dst_port = tcp_layer.dstport

        # Check if the packet contains the attack payload
        if "irc" in packet and "PRIVMSG" in str(packet.irc):
            attack_attempts += 1
            attack_payload_packets.append(int(packet.number))

            if not attacker_ip:
                attacker_ip = src_ip
                victim_ip = dst_ip
                attack_port = dst_port

    except AttributeError:
        # Continue processing if any packet does not have the expected layers
        continue

# Print results
print("Attacker IP:", attacker_ip)
print("Victim IP:", victim_ip)
print("Attack Port:", attack_port)
print("Number of Attack Attempts:", attack_attempts)
print("Packets Containing Attack Payload:", attack_payload_packets)
