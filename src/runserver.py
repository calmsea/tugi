#!/usr/bin/env python

import app

from wsgiref import simple_server
application = app.TugiApp()

if __name__ == '__main__':
    server = simple_server.make_server('', 8081, application)
    server.serve_forever()

#
# EOF
#
