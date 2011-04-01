import socket
import json
import random

class JsonRPCProxy(object):
    BUFFER = 2048
    def __init__(self, server, timeout=1.0):
        self.server = server
        self.timeout = timeout
        self.s = socket.create_connection(server, timeout)
        self._function_name = ""

    def __call__(self, *args, **kwargs):
        return self._call_method(self._function_name, *args, **kwargs)

    def _call_method(self, name, *args, **kwargs):
        if not (len(args) == 0 or len(kwargs) == 0):
            raise ValueError(
                "JSON spec allows positional arguments OR " + \
                "keyword arguments, not both."
            )
 
        req = {}
        req["id"] = random.random()
        req["jsonrpc"] = "2.0"
        req["method"] = name
        req["params"] = args or kwargs
        req_str = json.dumps(req)
        self.s.send(req_str)
        responselist = []
        while True:
            try:
                data = self.s.recv(self.BUFFER)
            except socket.timeout:
                    break
            if not data: 
                break
            responselist.append(data)
            if len(data) < self.BUFFER:
                break
        resp = ''.join(responselist)
        return json.loads(resp)

    def __getattr__(self, key):
        if key.startswith('_'):
            raise AttributeError
        else:
            self._function_name = key
        return self
 
if __name__ == "__main__":
    j = JsonRPCProxy(("localhost", 1234))
    j.echo("hallo welt")
    j.echo(text="hallo welt")
    print "done"

