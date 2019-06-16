class RouterHandler():

    MANUFACTURER = ""
    MODEL = ""
    PROTOCOL = ""

    def __init__(self, username, ip):
        self.username = username
        self.ip = ip

    def generate_url(self, relative_url):
        return "{protocol}://{domain}/{relative_url}".format(
            protocol=self.PROTOCOL, domain=self.ip, relative_url=relative_url)
