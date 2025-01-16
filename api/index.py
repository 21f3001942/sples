from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs


class handler(BaseHTTPRequestHandler):

    def _set_headers(self,status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type',content_type)
        self.end_headers()

    def _send_json_response(self, data, status_code=200):
        self._set_headers(status_code)
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def do_GET(self):

        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        try:
            if path=="/api":

                param_names = query_params.get('name',[])
            
                with open('q-vercel-python.json') as f:
                    data = json.load(f)

            
                result = list(filter(lambda x:x['name']==param_names[0] or x['name']==param_names[1],data))
                r = {"marks":[]}

                r['marks'].append(result[0]['marks'])
                r['marks'].append(result[1]['marks'])

                self._send_json_response(r)
                

            else:
                self.send_response(200)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write('Hello, world!'.encode('utf-8'))
        except:

            return
