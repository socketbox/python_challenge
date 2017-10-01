#!/usr/bin/env python

import cherrypy
import xfipchk

class XforceForm(object):
    def __init__(self, address='127.0.0.1', port=8000):
        cherrypy.config.update({'tools.staticdir.debug': True})
        # cherrypy.config.update('web/server.cfg')
        # parms override anything in config
        cherrypy.config.update({'server.socket_port': port,
                                'server.socket_host': address})


    @cherrypy.expose
    def index(self):
        return "/"

    @cherrypy.expose()
    def process_form(self, api_key, api_password, ip_addresses):
        if isinstance(ip_addresses, list):
            xfipchk.r
        xfipchk.call_xforce_api(ip_addresses, api_key, api_password)


if __name__ == '__main__':
    cherrypy.quickstart(XforceForm())
