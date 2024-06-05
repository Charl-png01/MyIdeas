import dpkt
import socket
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def extract_dns_requests(filename):
    f = open(filename, 'rb')
    pcap = dpkt.pcap.Reader(f)

    dns_responses = []  # List to store extracted IP addresses

    for ts, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
        except:
            continue

        if eth.type != 2048:
            continue

        try:
            ip = eth.data
        except:
            continue

        if ip.p != 17:
            continue

        try:
            udp = ip.data
        except:
            continue

        if udp.sport != 53 and udp.dport != 53:
            continue

        try:
            dns = dpkt.dns.DNS(udp.data)
        except:
            continue

        if dns.qr != dpkt.dns.DNS_R:
            continue
        else:
            for qname in dns.qd:
                print(qname.name)

        if dns.opcode != dpkt.dns.DNS_QUERY:
            continue

        if dns.rcode != dpkt.dns.DNS_RCODE_NOERR:
            continue

        if len(dns.an) < 1:
            continue

        # Extract and store IP addresses from the answer section
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

    features = {'timestamps': [], 'directions': [], 'sizes': [], 'interarrival_times': [], 'prev_timestamp': None,
                'prev_ip': None}

    for ts, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
        except:
            continue

        if eth.type != 2048:
            continue

        try:
            ip = eth.data
        except:
            continue

        # if ip.p != 17:
        #     continue

        # try:
        #     udp = ip.data
        # except:
        #     continue

        # Check if source or destination IP is the target IP
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


def print_packet_features(features, target_ip):
    print("PP_target_ip = ", target_ip)
    if not features:
        print("No packet features to print.")
        return

    print("Packet Features:")
    for i in range(len(features['timestamps'])):
        print("Timestamp:", features['timestamps'][i])
        print("Source:", features['prev_ip'])
        print("Destination:", target_ip)
        print("Direction:", features['directions'][i])
        print("Size:", features['sizes'][i])
        print("Interarrival Time:", features['interarrival_times'][i])
        print()


def visualize_features(features):
    if not features:
        print("No features to visualize.")
        return

    # Scatter plot
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    relative_times = [ts - features['timestamps'][0] for ts in features['timestamps']]
    colors = ['orange' if size < 0 else 'blue' for size in features['sizes']]
    plt.scatter(relative_times, features['sizes'], c=colors)
    plt.xlabel('Relative Time')
    plt.ylabel('Packet Size')
    plt.title('Scatter Plot of Relative Time vs Packet Size')

    # Line plot
    plt.subplot(1, 2, 2)
    normalized_interarrival_times = [t / max(features['interarrival_times']) for t in features['interarrival_times']]
    plt.plot(range(len(normalized_interarrival_times)), normalized_interarrival_times, marker='o', color='blue')
    plt.xlabel('Packet Number')
    plt.ylabel('Normalized Interarrival Time')
    plt.title('Line Plot of Normalized Interarrival Time vs Packet Number')

    plt.tight_layout()
    plt.show()


def main():
    filename = "1.pcap"
    dns_responses = extract_dns_requests(filename)
    target_ip = find_target_ip(dns_responses)

    if target_ip:
        pcap = dpkt.pcap.Reader(open(filename, 'rb'))
        packet_features = extract_packet_features(pcap, target_ip)
        # print("Packet Features = ",packet_features)
        # print_packet_features(packet_features, target_ip)

        # Visualize features using the extracted IP addresses
        visualize_features(packet_features)


if __name__ == "__main__":
    main()
