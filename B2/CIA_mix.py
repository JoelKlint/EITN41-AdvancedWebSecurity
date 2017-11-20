from pcapfile import savefile

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

    new_set = []
    all_sets = []
    row_is_interesting = False
    for i in range(len(rows)):
        ip_src = rows[i]["ip_src"]
        ip_dst = rows[i]["ip_dst"]

        if row_is_interesting and ip_src == mix_ip:                
            new_set.append(ip_dst)
            # We have reached the end of the new set
            try:
                if rows[i+1]["ip_src"] != mix_ip:

                    # Do intersections

                    new_intersections = []
                    for old_set in all_sets:
                        new_intersection = intersection(old_set, new_set)
                        new_intersections.append(new_intersection)
                    
                    all_sets.append(new_set)
                    all_sets += new_intersections

                    
                    new_set = []
                    row_is_interesting = False
            except IndexError:
                continue

        if ip_src == abu_ip and ip_dst == mix_ip:
            row_is_interesting = True
    



find_receivers('159.237.13.37', '94.147.150.188', 2, 'cia.log.1337.pcap')

