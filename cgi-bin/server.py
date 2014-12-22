#!/usr/bin/env python
import cgi, os
import cgitb; cgitb.enable()

try: # Windows need stdio for set binary
    import msvcrt
    msvcrt.setmode ( 0, os.O_BINARY ) # stdin  = 0
    msvcrt.setmode ( 1, os.O_BINARY ) # stdout = 1
except ImportError:
    pass

# Set vars
form = cgi.FieldStorage()
count_chunks = 0
fileitem = form['filename']


# Iterater for bufffering chunks
def fbuffer( f, chunk_size=1000 ):
    global count_chunks
    while True:
       chunk = f.read( chunk_size )
       if not chunk: break
       count_chunks += 1
       return chunk

# Print header
def prt_header():
    return '''Content-Type: text/html\n
    <html><body>
    '''

# Print footer
def prt_footer():
    return'''</body></html>'''

# Print status
def print_status(input_str):
    return '''<script>
                        function clear() {
                          document.getElementById("echo").innerHTML = "%s";
                        }
                        setTimeout(clear, 1000);
                    </script>
              '''%(input_str,)

# get links for files
def get_links(upd=False):
    print '''<ol id="links" name="links">'''
    dirs = os.listdir( os.path.abspath('')  +'/files/' )
    for file in dirs:
        # WARNING: this is absolute link, check your site address
        print '''<li><a href="%s" target="_blank">%s</a></li>'''%('http://localhost/upload/cgi-bin/files/' +file, file )
    print '''</ol>'''


# main cycle
def prt_body(fileitem):
    print '''<p id="echo">prepare to transfer...</p>'''

    if fileitem.filename:
        fn = os.path.basename(fileitem.filename)
        f = open( os.path.abspath('')  +'/files/' + fn, 'wb',1000000 )

        # get size
        size = len( fbuffer( fileitem.file ) )
        iter=0

        # read all chunks in buffer
        for chunk in fbuffer( fileitem.file ):
            f.write( chunk )
            percent = iter * 100 / size

            print print_status( str( percent )+'%' )

            iter += 1
        f.close()

        print print_status( 'complete' )

    else:
        print print_status('')
        print '''<p id="error" name="error" style="color:red">fail</p>'''

    get_links()

#print
print prt_header()
if form['param'].value == 'rdy':
    prt_body(fileitem)
elif form['param'].value == 'load':
    get_links()
print prt_footer()