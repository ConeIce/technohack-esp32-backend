import network
import math
import time
import urequests


fingerprinted_data = {
     -40: 'Cone table',
     -42: 'Cone table',
     -44: 'Cone table',
     -46: 'Cone table',
     -48: 'Cone table',
     -50: 'Cone table',
     -20: 'Random table',
     -22: 'Random table',
     -24: 'Random table',
     -26: 'Random table',
     -28: 'Random table',
     -30: 'Random table',
}
rssis = [rssi for rssi in fingerprinted_data.keys()]
active = {}


class WiFi:

    def __init__(self):
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        if not self.sta_if.isconnected():
            print('connecting to network...')
            self.sta_if.connect('MECAP-WPA2', '8b140b20e7')
            while not self.sta_if.isconnected():
                pass
        # print('network config: ', self.sta_if.ifconfig())

    def scan_wifi_devices(self):
        ap_list = self.sta_if.scan()
        for ap in ap_list:
            self.parse_wifi_details(ap)
            if 'SE' in self.ssid:
                self.final_location()

    def parse_wifi_details(self, ap):
        self.ssid = ap[0].decode('utf-8')
        self.bssid_str = ":".join("{:02x}".format(b) for b in ap[1])
        self.rssi = ap[3]
        if self.bssid_str in active:
            self.calc(active[self.bssid_str])
        else:
            active[self.bssid_str] = self.rssi

    def calc(self, rssi):
        threshold = 5
        min_diff = float('inf')
        closest_val = None

        for val in rssis:
            diff = abs(val - self.rssi)
            if diff < min_diff and diff < threshold:
                min_diff = diff
                closest_val = val

        try:
            location = fingerprinted_data[closest_val]
            active[self.bssid_str] = self.rssi
            print(location)
        except:
            pass

    def display_wifi_details(self):
        print('SSID: ', self.ssid)
        print('Mac address: ', self.bssid_str)
        print('Signal strength: ', self.rssi)

    def final_location(self):
        self.display_wifi_details()
        threshold = 5
        min_diff = float('inf')
        closest_val = None

        for val in rssis:
            diff = abs(val - self.rssi)
            if diff < min_diff and diff < threshold:
                min_diff = diff
                closest_val = val

        try:
            location = fingerprinted_data[closest_val]
            active[self.bssid_str] = self.rssi
            print(location)
        except:
            print('location unknown')


while True:
    try:
        wifi = WiFi()
        wifi.scan_wifi_devices()
        response = urequests.get("http://jsonplaceholder.typicode.com/albums/1")
        print(response.text)
        time.sleep(5)
    except Exception as e:
        print(str(e))
