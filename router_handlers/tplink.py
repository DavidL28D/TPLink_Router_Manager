import base64
import time
import random
import requests

from getpass import getpass
from datetime import datetime

from .router_handler import RouterHandler

class TPLink(RouterHandler):

    PROTOCOL = 'http'

    # Status
    STATUS = 'userRpm/StatusRpm.htm'

    # IP
    RELEASE_IP = 'userRpm/StatusRpm.htm?ReleaseIp=Release&wan=1'
    RENEW_IP = 'userRpm/StatusRpm.htm?RenewIp=Renew&wan=1'
 
    # MAC
    CHANGE_MAC = 'userRpm/MacCloneCfgRpm.htm?mac1={mac}&wan=1&Save=Save'
    RESTART_MAC = 'userRpm/MacCloneCfgRpm.htm'

    # Firewall
    FIREWALL = 'userRpm/FireWallRpm.htm'
    FIREWALL_UP = 'userRpm/FireWallRpm.htm?FireWall=2&IpFilt=2&IpRule=0&MacRule=0&Save=Save'
    FIREWALL_DOWN = 'userRpm/FireWallRpm.htm?IpFilt=2&IpRule=0&MacRule=0&Save=Save'


    def __init__(self, username=None, password=None, ip=None):
        super().__init__(username, ip)

        if not username or password is None:
            self.ask_credentials()
        
        else:
            self.username = username
            self.authorization_code = self.generate_authorization_code(password)
            self.request_headers = self.generate_request_headers()

    def ask_credentials(self):

        while True:
            
            self.ip = input("Ip: ")
            self.username = input("Username: ")
            password = getpass("Password: ")

            self.authorization_code = self.generate_authorization_code(password)
            self.request_headers = self.generate_request_headers()

            if self.get_public_ip():
                break

            print("Wrong credentials. Please verify and try again!")


    def generate_request_headers(self):

        return {
            'Authorization': 'Basic {}'.format(self.authorization_code),
            'Referer': self.generate_url(self.STATUS)
        }


    def generate_authorization_code(self, password):

        return base64.b64encode(
            '{username}:{password}'.format(
                username=self.username,
                password=password).encode('ascii')).decode('ascii')


    def get_status(self):

        response = requests.get(
            self.generate_url(self.STATUS),
            headers=self.request_headers)

        if response.status_code == 401:
            return None

        return response.text.splitlines()


    def get_firewall_status(self):

        response = requests.get(
            self.generate_url(self.FIREWALL),
            headers=self.request_headers)

        if response.status_code == 401:
            return None

        return response.text.splitlines()


    def get_public_ip(self):

        response = requests.get(
            self.generate_url(self.STATUS),
            headers=self.request_headers)

        if response.status_code == 401:
            return None

        return response.text.splitlines()


    def get_mac_address(self):

        response = requests.get(
            self.generate_url(self.STATUS),
            headers=self.request_headers)

        if response.status_code == 401:
            return None

        return response.text.splitlines()


    def send_ip_release_request(self):

        requests.get(
            self.generate_url(self.RELEASE_IP),
            headers=self.request_headers)


    def send_ip_renew_request(self):

        requests.get(
            self.generate_url(self.RENEW_IP),
            headers=self.request_headers)


    def send_mac_change_request(self, mac_address):
        
        requests.get(
            self.generate_url(self.CHANGE_MAC.format(mac=mac_address)),
            headers=self.request_headers)


    def send_firewall_up_request(self):

        requests.get(
            self.generate_url(self.FIREWALL_UP),
            headers=self.request_headers)

        print("Firewall ON.")


    def send_firewall_down_request(self):

        requests.get(
            self.generate_url(self.FIREWALL_DOWN),
            headers=self.request_headers)

        print("Firewall OFF.")

    
    def renew_public_ip(self):

        lap = lap2 = 0
        old_ip = new_ip = self.get_public_ip()

        print("Renewing IP Address...")

        while old_ip == new_ip:

            lap2 = 0
            self.send_ip_release_request()
            print("Released at: {}".format(datetime.now()))
            time.sleep(2)

            self.send_ip_renew_request()
            print("Renew request at: {}".format(datetime.now()))
            time.sleep(5)

            new_ip = self.get_public_ip()

            while new_ip == '0.0.0.0':

                if lap2 < 9:
                    lap2+=1
                else:
                    print(f"OLD IP -> NEW IP\n{old_ip} -> {new_ip}")
                    print("Has exceeded the number of attempts, Check your internet connection.\n")
                    return

                time.sleep(5)
                new_ip = self.get_public_ip()

            if lap < 4:
                lap +=1
            else:
                print(f"OLD IP -> NEW IP\n{old_ip} -> {new_ip}")
                print("Has exceeded the number of attempts.\n")
                return

            print(f"OLD IP -> NEW IP\n{old_ip} -> {new_ip}\n")
            

    def renew_mac_address(self):

        old_mac = new_mac = self.get_mac_address()

        octets = old_mac.split("-")
        new_last_octet = hex(random.randrange(256)).split("x")[-1]
        new_mac = "-".join(octets[:-1]+[new_last_octet])

        print(f"Changing MAC Address (Rebooting Router)...")
        self.send_mac_change_request(new_mac)
        time.sleep(10)

        new_mac = self.get_mac_address()

        print(f"OLD MAC -> NEW MAC\n{old_mac} -> {new_mac}\n")


    def renew_public_ip_and_mac(self):

        old_ip = new_ip = self.get_public_ip()

        print("Waiting for changes...\n")

        self.renew_mac_address()
        new_ip = self.get_public_ip()

        if old_ip == new_ip:

            self.renew_public_ip()
            new_ip = self.get_public_ip()

        else:

            print(f"Renewing IP Address...\nOLD IP -> NEW IP\n{old_ip} -> {new_ip}")


    def restart_mac_address(self):

        response = requests.get(
            self.generate_url(self.RESTART_MAC),
            headers=self.request_headers)

        if response.status_code == 401:
            return None

        texto = response.text.splitlines()
        mac = texto[2].split(",")

        active_mac = mac[0].replace('"', '').replace(' ','')
        fabric_mac = mac[1].replace('"', '').replace(' ','')

        print("Restoring Mac address...")
        self.send_mac_change_request(fabric_mac)
        time.sleep(10)

        if fabric_mac == self.get_mac_address():
            print(f"Mac restaured: {active_mac} -> {fabric_mac}")
        else:
            print("Problem restarting Mac address.")