import dpkt
import socket
from collections import Counter
import matplotlib.pyplot as plt

def extract_dns_responses(filename):
    f = open(filename, 'rb')
    pcap = dpkt.pcap.Reader(f)

    dns_responses = []

    for ts, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
        except dpkt.dpkt.UnpackError:
            continue

        if eth.type != 2048:
            continue

        try:
            ip = eth.data
        except dpkt.dpkt.UnpackError:
            continue

        if ip.p != 17:
            continue

        try:
            udp = ip.data
        except dpkt.dpkt.UnpackError:
            continue

        if udp.sport != 53 and udp.dport != 53:
            continue

        try:
            dns = dpkt.dns.DNS(udp.data)
        except dpkt.dpkt.UnpackError:
            continue

        if dns.qr == dpkt.dns.DNS_R and dns.opcode == dpkt.dns.DNS_QUERY and dns.rcode == dpkt.dns.DNS_RCODE_NOERR:
            for answer in dns.an:
                if answer.type == 1:  # DNS_A
                    ip_address = socket.inet_ntoa(answer.rdata)
                    print('Domain Name:', answer.name, '\tIP Address:', ip_address)
                    dns_responses.append(ip_address)

    return dns_responses

def find_target_ip(dns_responses):
    if not dns_responses:
        print("No DNS responses found.")
        return None

    # Find the most common IP address
    ip_counter = Counter(dns_responses)
    target_ip = ip_counter.most_common(1)[0][0]
    print("Target IP Address:", target_ip)
    return target_ip

def extract_packet_features(pcap, target_ip):
    if target_ip is None:
        print("No target IP address found.")
        return

    features = {'timestamps': [], 'directions': [], 'sizes': [], 'interarrival_times': [], 'prev_timestamp': None, 'prev_ip': None}

    for ts, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
        except dpkt.dpkt.UnpackError:
            continue

        if eth.type != 2048:
            continue

        try:
            ip = eth.data
        except dpkt.dpkt.UnpackError:
            continue

        if socket.inet_ntoa(ip.src) == target_ip or socket.inet_ntoa(ip.dst) == target_ip:
            if features['prev_timestamp'] is None:
                features['prev_timestamp'] = ts
                features['prev_ip'] = target_ip

            features['timestamps'].append(ts)
            features['directions'].append('incoming' if socket.inet_ntoa(ip.dst) == target_ip else 'outgoing')
            features['sizes'].append(-len(buf) if socket.inet_ntoa(ip.dst) == target_ip else len(buf))

            if 'prev_timestamp' in features:
                features['interarrival_times'].append(ts - features['prev_timestamp'])
            else:
                features['interarrival_times'].append(0)

            features['prev_timestamp'] = ts

    return features

def visualize_features(features):
    if not features:
        print("No features to visualize.")
        return

    # Scatter plot
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    relative_times = [ts - features['timestamps'][0] for ts in features['timestamps']]
    colors = ['green' if size < 0 else 'red' for size in features['sizes']]
    plt.scatter(relative_times, features['sizes'], c=colors)
    plt.xlabel('Relative Time')
    plt.ylabel('Packet Size')
    plt.title('Scatter Plot')

    # Line plot
    plt.subplot(1, 2, 2)
    normalized_interarrival_times = [t / max(features['interarrival_times']) for t in features['interarrival_times']]
    plt.plot(range(len(normalized_interarrival_times)), normalized_interarrival_times, marker='o', color='blue')
    plt.xlabel('Packet Number')
    plt.ylabel('Normalized Inter-arrival Time')
    plt.title('Inter-arrival Time vs Packet Number')

    plt.tight_layout()
    plt.show()

def main():
    filename = "YTB.pcap"
    dns_responses = extract_dns_responses(filename)
    target_ip = find_target_ip(dns_responses)

    if target_ip:
        pcap = dpkt.pcap.Reader(open(filename, 'rb'))
        packet_features = extract_packet_features(pcap, target_ip)
        visualize_features(packet_features)

if __name__ == "__main__":
    main()
