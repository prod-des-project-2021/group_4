import socket
import threading

class ConnectionListener(threading.Thread):
    def __init__(self, service):
        self.service = service

    def run(self):
        while(service.running):
            pass 
