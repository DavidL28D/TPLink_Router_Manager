import time
import requests

from .tplink import TPLink

class TPLinkWR340G (TPLink):

    def __init__(self, username=None, password=None, ip=None):
        super().__init__(username, password, ip)


    def get_status(self):

        splited_response = super().get_status()

        # INFO

        firmware = splited_response[7].replace('"', '').replace(',', '')
        model = splited_response[8].replace('"', '').replace(',', '')

        # LAN

        second_splited_response = splited_response[13].replace('"', '').replace(',', '')
        third_splited_response = second_splited_response.split(' ')

        lan_mac = third_splited_response[0]
        lan_ip = third_splited_response[1]
        lan_mask = third_splited_response[2]

        # WIRELESS

        wireless_name = splited_response[19].replace('"', '').replace(',', '')
        wireless_mac = splited_response[22].replace('"', '').replace(',', '')
        wireless_ip = splited_response[23].replace('"', '').replace(',', '')

        # WAN

        second_splited_response = splited_response[36].replace('"', '').replace(',', '')
        third_splited_response = second_splited_response.split(" ")

        wan_mac = third_splited_response[1]
        wan_ip = third_splited_response[2]
        wan_subnet_mask = third_splited_response[4]
        wan_dafault_wateway = third_splited_response[7]
        wan_dns_a = third_splited_response[11]
        wan_dns_b = third_splited_response[13]

        print(f"** Status **\nHardware Version: {model}\nFirmware Version: {firmware}\n\n** LAN **\nMAC Address: {lan_mac}\nIP Address: {lan_ip}\nSubnet Mask: {lan_mask}\n\n** Wireless **\nSSID: {wireless_name}\nMAC Address: {wireless_mac}\nIP Address: {wireless_ip}\n\n** WAN **\nMAC Address: {wan_mac}\nIP Address: {wan_ip}\nSubnet Mask: {wan_subnet_mask}\nDefault Gateway: {wan_dafault_wateway}\nDNS Server: {wan_dns_a} - {wan_dns_b}\n")


    def get_firewall_status(self):
        splited_response = super().get_firewall_status()
        
        num = int(splited_response[2].replace('"', '').replace(',', ''))
        if num == 1:
            general = 'On'
        else:
            general = 'Off'

        num = int(splited_response[3].replace('"', '').replace(',', ''))
        if num == 1:
            ip = 'On'
        else:
            ip = 'Off'

        num = int(splited_response[5].replace('"', '').replace(',', ''))
        if num == 1:
            mac = 'On'
        else:
            mac = 'Off'

        num = int(splited_response[6].replace('"', '').replace(',', ''))
        if num == 1:
            domain = 'On'
        else:
            domain = 'Off'

        print(f"** Firewall **\nGeneral Switch: {general}\nIP Address Filtering: {ip}\nMAC Address Filtering: {mac}\nDomain Address Filtering: {domain}")
        

    def get_public_ip(self):
        
        splited_response = super().get_public_ip()
        second_splited_response = splited_response[36].split(',')
        return second_splited_response[2].replace(' ', '').replace('"', '').replace(',', '')


    def get_mac_address(self):

        splited_response = super().get_public_ip()
        second_splited_response = splited_response[36].split(',')
        return second_splited_response[1].replace(' ', '').replace('"', '').replace(',', '')


