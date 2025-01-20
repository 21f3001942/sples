from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from collections import OrderedDict


class handler(BaseHTTPRequestHandler):

    def _set_headers(self,status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def _send_json_response(self, data, status_code=200):
        self._set_headers(status_code)
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def do_GET(self):
        
        parsed_path = urlparse(self.path)

        query_params = OrderedDict(sorted(parse_qs(parsed_path.query).items()))

        
        if query_params:
            param_names = query_params.get('name',[])
            
            with open('q-vercel-python.json') as f:
                data = json.load(f)

                
            result = []

            for x in data:
                if x['name'] in param_names:
                    result.append(x['marks'])

            r = {"marks":[]}

            for i in range(len(result)):
                r['marks'].append(result[i])


            self._send_json_response(r)
        else:
            self._send_json_response('Hello World!')
        return
    

