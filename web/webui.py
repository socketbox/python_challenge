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
                form_ips = ip_addresses.splitlines()
            good_ips = []
            for i in form_ips:
                if xfipchk.validate_ip(i):
                    good_ips.append(i)
            return xfipchk.call_xforce_api(good_ips, api_key, api_password)
        else:
            return cherrypy.HTTPError("400: Bad Request", 400)


if __name__ == '__main__':
    webapp = XforceForm('127.0.0.1', 8000)
    cherrypy.tree.mount(webapp, config='./server.cfg')

    if hasattr(cherrypy.engine, 'signal_handler'):
        cherrypy.engine.signal_handler.subscribe()

    # Initialize console control
    if hasattr(cherrypy.engine, "console_control_handler"):
        cherrypy.engine.console_control_handler.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()
