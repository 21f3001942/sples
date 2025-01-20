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
        
        # parsed_path = urlparse(self.path)

        # query_params = OrderedDict(sorted(parse_qs(parsed_path.query).items()))

        
        # if query_params:
        #     param_names = query_params.get('name',[])
            
        #     with open('q-vercel-python.json') as f:
        #         data = json.load(f)

                
        #     result = []

        #     for x in data:
        #         if x['name'] in param_names:
        #             result.append(x['marks'])

        #     r = {"marks":[]}

        #     for i in range(len(result)):
        #         r['marks'].append(result[i])


        #     self._send_json_response(r)

        parsed_path = urlparse(self.path)
        raw_query = parsed_path.query

        # This will store names in the exact order they appear in URL
        param_names = []
        current_pos = 0

        while True:
            name_pos = raw_query.find('name=', current_pos)
            if name_pos == -1:  # No more 'name=' parameters found
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
    

