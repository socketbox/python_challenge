#!/usr/bin/env python

import cherrypy
import xfipchk


class XforceForm(object):

    def __init__(self, address='127.0.0.1', port=8000):
        # parms override anything in config
        cherrypy.config.update({'server.socket_port': port,
                                'server.socket_host': address})

    @cherrypy.expose
    def index(self):
        return "/"

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def process_form(self, api_key, api_password, ip_addresses):
        if xfipchk.validate_api_creds(api_key.strip()) and xfipchk.validate_api_creds(api_password.strip()):
            form_ips = []
            if isinstance(ip_addresses, str):
                form_ips.append(ip_addresses)
            elif isinstance(ip_addresses, list):
                form_ips.extend(ip_addresses)
            good_ips = []
            for i in form_ips:
                if xfipchk.validate_ip(i):
                    good_ips.append(i)
            return xfipchk.call_xforce_api(good_ips, api_key, api_password)
        else:
            return cherrypy.HTTPError("400: Bad Request", 400)

    @cherrypy.expose()
    def stop_demo(self, stop_demo):
        cherrypy.engine.stop()

if __name__ == '__main__':
    xfipchk.start_server()
