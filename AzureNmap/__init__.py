import logging
import azure.functions as func
import nmap

class azure_nmap:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.nm = nmap.PortScanner()
        self.standard_scan()

    def standard_scan(self):
        self.nm.scan(self.ip_address, arguments="-sV")

    def get_scan(self):
        return self.nm[self.ip_address]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    ip_address = req.params.get('ip_address')
    if not ip_address:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            ip_address = req_body.get('ip_address')

    if ip_address:
        az_mapper = azure_nmap(ip_address=ip_address)
        return func.HttpResponse(f"{az_mapper.get_scan()}")
    else:
        return func.HttpResponse(
             "Please pass a IP Address(ip_address) on the query string or in the request body",
             status_code=400
        )
