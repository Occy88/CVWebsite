#!C:\Users\octav\AppData\Local\Programs\Python\Python36-32\python.exe -u
#!/usr/bin/env python
# Required header that tells the browser how to render the text.
import cgi
import cgitb
cgitb.enable()

def htmlTop():
    print("""Content-type:text/html\n\n
    <!DOCTYPE html>
    <html>
        <head lang="en">
            <meta charset="utf-8"/>
            <title>My first server page</title>
        </head>
        <body>""")
def htmlTail():
    print("""</body>
        </html>""")
#main program
if __name__=="__main__":
    try:
        htmlTop()
        print("hello")
        htmlTail()
    except:
        cgi.print_exception()