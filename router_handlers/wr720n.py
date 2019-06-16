from .tplink import TPLink

class TPLinkWR720n (TPLink):

    def __init__(self, username=None, password=None, ip=""):
        super().__init__(username, password, ip)


    def get_public_ip(self):
        
        splited_response = super().get_public_ip()
        return splited_response[49].replace('"', '').replace(',', '')


    def get_mac_address(self):
        
        splited_response = super().get_public_ip()
        return splited_response[49].replace('"', '').replace(',', '')
