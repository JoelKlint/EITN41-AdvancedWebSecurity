from pcapfile import savefile

testcap = open('cia.log.1337.pcap', 'rb')
capfile = savefile.load_savefile(testcap, layers=2, verbose=True)
i = 0
# print the packets
print ('timestamp\teth src\t\t\teth dst\t\t\tIP src\t\tIP dst')
for pkt in capfile.packets:
    timestamp = pkt.timestamp
    # all data is ASCII encoded (byte arrays). If we want to compare with strings
    # we need to decode the byte arrays into UTF8 coded strings
    eth_src = pkt.packet.src.decode('UTF8')
    eth_dst = pkt.packet.dst.decode('UTF8')
    ip_src = pkt.packet.payload.src.decode('UTF8')
    ip_dst = pkt.packet.payload.dst.decode('UTF8')
    print ('{}:{}\t\t{}\t{}\t{}\t{}'.format(i, timestamp, eth_src, eth_dst, ip_src, ip_dst))
    i += 1