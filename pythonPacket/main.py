import dpkt
import socket
import matplotlib.pyplot as plt

def extract_dns_ip(pcap):
    for timestamp, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        if isinstance(eth.data, dpkt.ip.IP) and isinstance(eth.data.data, dpkt.udp.UDP):
            udp = eth.data.data
            if udp.sport == 53 or udp.dport == 53:
                dns = dpkt.dns.DNS(udp.data)

                # Check if there are answer records in the DNS response
                if dns.an:
                    return socket.inet_ntoa(dns.an[0].ip)
    return None

def extract_features(pcap, target_ip):
    features = []
    first_packet_time = None

    for timestamp, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        if isinstance(eth.data, dpkt.ip.IP):
            ip = eth.data
            if socket.inet_ntoa(ip.src) == target_ip or socket.inet_ntoa(ip.dst) == target_ip:
                if first_packet_time is None:
                    first_packet_time = timestamp

                direction = 'incoming' if socket.inet_ntoa(ip.dst) == target_ip else 'outgoing'
                packet_size = len(buf)
                inter_arrival_time = timestamp - first_packet_time if first_packet_time else 0

                features.append({
                    'timestamp': timestamp,
                    'direction': direction,
                    'packet_size': -packet_size if direction == 'outgoing' else packet_size,
                    'inter_arrival_time': inter_arrival_time
                })

    return features

def visualize_features(features):
    if not features:
        print("No features to visualize.")
        return

    # Scatter plot
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    relative_times = [ts - features[0]['timestamp'] for ts in [feature['timestamp'] for feature in features]]
    colors = ['orange' if size < 0 else 'blue' for size in [feature['packet_size'] for feature in features]]
    plt.scatter(relative_times, [feature['packet_size'] for feature in features], c=colors)
    plt.xlabel('Relative Time')
    plt.ylabel('Packet Size')
    plt.title('Scatter Plot of Relative Time vs Packet Size')

    # Line plot
    plt.subplot(1, 2, 2)
    max_inter_arrival_time = max(feature['inter_arrival_time'] for feature in features)
    x = list(range(1, len(features) + 1))
    y = [feature['inter_arrival_time'] / max_inter_arrival_time for feature in features]
    plt.plot(x, y, 'o-', color='skyblue', markersize=8, label='Lollipop Plot')
    plt.scatter(x, y, color='skyblue', s=50, zorder=10)
    plt.xlabel("Packet Number")
    plt.ylabel("Normalized Inter-Arrival Time")
    plt.title("Lollipop Plot")
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Step 1: Load pcap file
    with open('YTB.pcap', 'rb') as file:
        pcap = dpkt.pcap.Reader(file)

        # Step 2: Find the IP address used
        target_ip = extract_dns_ip(pcap)

        if target_ip:
            print(f"Target IP for www.youtube.com: {target_ip}")

            # Step 3: Filter packets and extract features
            pcap = dpkt.pcap.Reader(open('YTB.pcap', 'rb'))
            features = extract_features(pcap, target_ip)

            # Step 4: Visualize the features
            visualize_features(features)
        else:
            print("Could not extract the target IP from DNS packets.")

