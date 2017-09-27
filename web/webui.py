#!/usr/bin/env python

import cherrypy
import os
import io


class XforceForm(object):
    def __init__(self, address='127.0.0.1', port=8000):
        cherrypy.config.update({'tools.staticdir.debug': True})
        # cherrypy.config.update('web/server.cfg')
        # parms override anything in config
        cherrypy.config.update({'server.socket_port': port,
                                'server.socket_host': address})

    # def start_server(self):
    #    cherrypy.quickstart(XforceForm(), '/', './web/server.cfg')

    @cherrypy.expose
    def index(self):
        return "/"


if __name__ == '__main__':
    cherrypy.quickstart(XforceForm())
