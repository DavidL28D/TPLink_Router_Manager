class RouterHandler():

    PROTOCOL = ""

    def __init__(self, username, ip):
        self.username = username
        self.ip = ip

    def generate_url(self, relative_url):
        return f"{self.PROTOCOL}://{self.ip}/{relative_url}"