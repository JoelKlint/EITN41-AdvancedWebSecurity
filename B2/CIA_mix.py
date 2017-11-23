from pcapfile import savefile

def convert_ip_to_int(ip_address):
    res = ip_address.split(".")
    ints = list(map(lambda s: int(s), res))
    hexes = list(map(lambda i: hex(i)[2:].zfill(2), ints))
    joined_hex = "".join(hexes)
    int_representation = int(joined_hex, 16)
    return int_representation

def parse_file(filename):
    testcap = open(filename, 'rb')
    capfile = savefile.load_savefile(testcap, layers=2, verbose=True)

    entries = []
    for pkt in capfile.packets:
        timestamp = pkt.timestamp
        # all data is ASCII encoded (byte arrays). If we want to compare with strings
        # we need to decode the byte arrays into UTF8 coded strings
        eth_src = pkt.packet.src.decode('UTF8')
        eth_dst = pkt.packet.dst.decode('UTF8')
        ip_src = pkt.packet.payload.src.decode('UTF8')
        ip_dst = pkt.packet.payload.dst.decode('UTF8')

        entries.append({
            "timestamp": timestamp,
            "ip_src": ip_src,
            "ip_dst": ip_dst
        })
    return entries

def find_receivers(abu_ip, mix_ip, m, filename):

    rows = parse_file(filename)

    new_set = set()
    all_sets = []
    row_is_interesting = False
    for i in range(len(rows)):
        ip_src = rows[i]["ip_src"]
        ip_dst = rows[i]["ip_dst"]

        if row_is_interesting and ip_src == mix_ip:
            new_set.add(ip_dst)        
            # We have reached the end of the new set
            try:
                if rows[i+1]["ip_src"] != mix_ip:
                    all_sets.append(new_set)                    
                    new_set = set()
                    row_is_interesting = False
            except IndexError:
                continue

        if ip_src == abu_ip and ip_dst == mix_ip:
            row_is_interesting = True

    # 
    # Learning Phase
    # 

    disjoint_sets = []

    # A new set appears
    for new_set in all_sets:
        new_set_is_disjoint = True

        # Compare with all disjoint sets we have
        for disjoint_set in disjoint_sets:
            if new_set & disjoint_set != set():
                new_set_is_disjoint = False
        
        # Save new disjoint set
        if new_set_is_disjoint:
            disjoint_sets.append(new_set)
            all_sets.remove(new_set)
        
        # Break when we have enough sets
        if len(disjoint_sets) >= m:
            disjoint_sets = disjoint_sets[:m]
            break
        
    # 
    # Excluding phase
    # 
    for new_set in all_sets:
        non_disjoint_sets = []

        for disjoint_set in disjoint_sets:
            if new_set & disjoint_set != set():
                non_disjoint_sets.append(disjoint_set)
        
        if len(non_disjoint_sets) == 1:
            non_disjoint_set = non_disjoint_sets[0]
            # Remove old disjoint set that should be replaced
            disjoint_sets.remove(non_disjoint_set)
            # Calculate intersection
            intersection = non_disjoint_set & new_set
            # Add new disjoint set
            disjoint_sets.append(intersection)

    disjoint_lists = list(map(lambda s: list(s), disjoint_sets))
    disjoint_ips = list(map(lambda s: s[0], disjoint_lists))
    disjoint_ints = list(map(lambda ip: convert_ip_to_int(ip), disjoint_ips))
    integer_sum = sum(disjoint_ints)

    print(integer_sum)
            
        
# find_receivers('159.237.13.37', '94.147.150.188', 2, 'cia.log.1337.pcap')
find_receivers('161.53.13.37', '11.192.206.171', 12, 'cia.log.1339.pcap')


