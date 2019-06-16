import base64
import time
import random
from getpass import getpass
from datetime import datetime

import requests
from .router_handler import RouterHandler

class TPLinkWR720n(RouterHandler):

    MANUFACTURER = 'TP-Link'
    MODEL = 'WR720n'
    RELEASE_URL = 'userRpm/StatusRpm.htm?ReleaseIp=Release&wan=1'
    RENEW_URL = 'userRpm/StatusRpm.htm?RenewIp=Renew&wan=1'
    REFERER_URL = 'userRpm/StatusRpm.htm'
    PROTOCOL = 'http'
    CHANGE_MAC_URL = 'userRpm/MacCloneCfgRpm.htm?mac1={mac}&wan=1&Save=Save'

    def __init__(self, username=None, password=None, ip="192.168.0.1"):
        super().__init__(username, ip)
        if not username or password is None:
            self.ask_credentials()
        else:
            self.username = username
            self.authorization_code = self.generate_authorization_code(
                password)
            self.request_headers = self.generate_request_headers()

    def ask_credentials(self):
        while True:
            self.username = input("Username: ")
            password = getpass("Password: ")
            self.authorization_code = self.generate_authorization_code(
                password)
            self.request_headers = self.generate_request_headers()
            if self.get_public_ip():
                break
            print("Wrong credentials. Please verify and try again!")

    def generate_request_headers(self):
        return {
            'Authorization': 'Basic {}'.format(self.authorization_code),
            'Referer': self.generate_url(self.REFERER_URL)
        }

    def generate_authorization_code(self, password):
        return base64.b64encode(
            '{username}:{password}'.format(
                username=self.username,
                password=password).encode('ascii')).decode('ascii')

    def get_public_ip(self):
        response = requests.get(
            self.generate_url(self.REFERER_URL),
            headers=self.request_headers)
        if response.status_code == 401:
            return None
        splited_response = response.text.splitlines()
        return splited_response[50].replace('"', '').replace(',', '')

    def get_mac_address(self):
        response = requests.get(
            self.generate_url(self.REFERER_URL),
            headers=self.request_headers)
        if response.status_code == 401:
            return None
        splited_response = response.text.splitlines()
        return splited_response[49].replace('"', '').replace(',', '')

    def renew_public_ip(self):
        old_ip = new_ip = self.get_public_ip()
        while old_ip == new_ip:
            self.send_release_request()
            print("Released at: {}".format(datetime.now()))
            time.sleep(2)
            self.send_renew_request()
            print("Renew request at: {}".format(datetime.now()))
            time.sleep(2)
            new_ip = self.get_public_ip()
            while new_ip == '0.0.0.0':
                new_ip = self.get_public_ip()
                time.sleep(3)
            print("Old ip: {}   New ip: {}".format(old_ip, new_ip))

    def renew_public_ip_and_mac(self):
        old_ip = new_ip = self.get_public_ip()
        while old_ip == new_ip:
            self.renew_mac_address()
            time.sleep(10)
            print("Wating for new public IP")
            new_ip = self.get_public_ip()
            while new_ip == '0.0.0.0':
                new_ip = self.get_public_ip()
                time.sleep(3)
            print("Old ip: {}   New ip: {}".format(old_ip, new_ip))

    def send_release_request(self):
        requests.get(
            self.generate_url(self.RELEASE_URL),
            headers=self.request_headers)

    def send_renew_request(self):
        requests.get(
            self.generate_url(self.RENEW_URL),
            headers=self.request_headers)

    def renew_mac_address(self):
        old_mac_address = self.get_mac_address()
        octets = old_mac_address.split("-")
        new_last_octet = hex(random.randrange(256)).split("x")[-1]
        new_mac_address = "-".join(octets[:-1]+[new_last_octet])
        print("Trying renew MAC address with: {}".format(new_mac_address))
        requests.get(
            self.generate_url(self.CHANGE_MAC_URL.format(mac=new_mac_address)),
            headers=self.request_headers)

