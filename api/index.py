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
        raw_query = parsed_path.query

        param_names = []
        current_pos = 0

        while True:
            name_pos = raw_query.find('name=', current_pos)
            if name_pos == -1:  
                break
                
            start_pos = name_pos + 5
            end_pos = raw_query.find('&', start_pos)
            if end_pos == -1:
                end_pos = len(raw_query)
                
            name = raw_query[start_pos:end_pos]
            param_names.append(name)
            current_pos = end_pos
        
        if param_names:
            with open('q-vercel-python.json') as f:
                data = json.load(f)
                
            marks_dict = {x['name']: x['marks'] for x in data}
            result = [marks_dict[name] for name in param_names if name in marks_dict]
            r = {"marks": result}
            self._send_json_response(r)
        else:
            self._send_json_response('Hello World!')
        return
    

