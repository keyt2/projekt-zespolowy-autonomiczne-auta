import datetime


class Request:

    def __init__(self, address_from, address_to, time, passangers):
        self.address_from = address_from
        self.address_to = address_to
        self.time = time
        self.passangers = passangers

    def show(self):
        print(f'Date: {self.time}, address from: {self.address_from}, address to: {self.address_to}, number os passangers: {self.passangers}')
