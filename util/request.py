class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables

        decReq = request.decode()
        decReq.strip()
        header = decReq.split("\r\n")
        print(header)
        self.body = b""
        self.method = ""
        self.path = ""
        self.http_version = "1.1"
        self.headers = {}
        # take care of first header 
        req = header.pop(0).split("/", 1)
        self.headers["Request"] = [req[0].strip(), req[1].split(" ")[0].strip(), req[1].split(" ")[1].strip()]
        
        # then rest of the headers
        for head in header:
            head.strip()
            try:
                spl = head.split(":", 1)
                self.headers[spl[0].strip()] = spl[1].strip()
            except IndexError:
                if self.headers.get("IndexErrors") is not None:
                    self.headers["IndexErrors"].append(head)
                else:
                    self.headers["IndexErrors"] = list()
        #print(self.headers)
