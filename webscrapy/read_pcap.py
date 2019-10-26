from utils.basic.parser import default_arp_poison_reader_args
from utils.basic.pcap_reader import PCAP

parser = default_arp_poison_reader_args()
filename = parser.filename

pcap = PCAP(filename)
pcap.init_pcap(filename)
