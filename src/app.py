#
#
#

from cStringIO import StringIO

class TugiApp(object):
    def __init__(self):
        ''' Initialize '''
        pass

    def __call__(self, environ, start_response):
        ''' WSGI application '''

        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        if path == '/':
            start_response('200 OK', [('Content-type', 'text/html')])
            sout = StringIO()
            sout.write("<html><body>")
            sout.write("<p><a href='/environ'>environ</a></p>")
            sout.write("<p><a href='/tugi'>tugi</a></p>")
            sout.write("</body></html>")
            return sout.getvalue()
        elif path == '/tugi':
            start_response('200 OK', [('Content-type', 'text/html')])
            sout = StringIO()
            sout.write('<html><head>')
            sout.write('<link rel=stylesheet type="text/css" href="tugi.css">')
            sout.write('''
<script
	src="http://www.google.com/jsapi"
	type="text/javascript"
	charset="utf-8"
></script>
<script language="javascript" type="text/javascript">
google.load("prototype", "1.6");
</script>''')
            sout.write('<script type="text/javascript" src="tugi.js"></script>')
            sout.write('</head><body>')
            sout.write("<div id='tugi'>")
            sout.write("<p>Tugi</p>")

            #
            # Compose
            #
            sout.write("<div id='tugi_compose'>")
            sout.write("<p>Tugi Compose</p>")
            sout.write("<form id='tugi_compose_form'>")
            sout.write('<select id="member0" onchange="json_update(\'/tugi.xml?member=\' + $F(member0))">')
            for m in ["feed", "url"]:
                sout.write("<option value=\"%s\">%s</option>" % (m,m))
            sout.write("</select>")

            sout.write("</form>")
            sout.write("</div>")

            #
            # View
            #
            sout.write('<div id="tugi_view">')
            sout.write("<p>Tugi View</p>")
            sout.write("</div>")
            sout.write("</div>")
            sout.write("</body></html>")
            return sout.getvalue()
        elif path.startswith('/tugi.xml'):
            params = {}
            for pair in environ['QUERY_STRING'].split('&'):
                key, val = pair.split('=')
                params[key] = val
            member = params.get('member')
            if member in ('url', 'feed'):
                start_response('200 OK', [('Content-type', 'application/xml'),
                                          ('X-JSON', '({"app" : "tugi", "type" : "member", "name" : "%s", "input_list" : [ {"label" : "URL", "type" : "string", "width" : 60}]})' % (member,))
                                          ])
                return '''<div class="tugi_obj" id="tugi_obj"><form>
<table>
<tr><td colspan="2">Member:%s</td></tr>
<tr><td>URL</td><td><input type="text" length="60"/></td></tr>
</table>
</form></div>''' % (member,)
            else:
                start_response('404 Not Found', [('Content-type', 'text/plain')])
        elif path.startswith('/environ'):
            start_response('200 OK', [('Content-type', 'text/html')])
            sout = StringIO()
            sout.write("<html><body><table>")
            for key, val in sorted(environ.items(), lambda x,y: cmp(x[0], y[0])):
                sout.write("<tr><td>%s</td><td>%s</td></tr>" % (key,val))
            sout.write("</table></body></html>")
            return sout.getvalue()
        elif path == '/tugi.js':
            start_response('200 OK', [('Content-type', 'text/javascript')])
            return open("tugi.js", "r").readlines()
        elif path == '/tugi.css':
            start_response('200 OK', [('Content-type', 'text/javascript')])
            return open("tugi.css", "r").readlines()
        else:
            start_response('404 Not Found', [('Content-type', 'text/plain')])
            return "Not Found"

#
# EOF
#
