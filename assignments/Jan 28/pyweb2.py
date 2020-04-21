from http.server import HTTPServer, SimpleHTTPRequestHandler
import pgmeta
import dbexec

page ="""
<script src="./view/node_modules/dagre/dist/dagre.js"></script>
<script src="./view/node_modules/nomnoml/dist/nomnoml.js"></script>

    <script id="noml" type="text/plain">
#zoom: 1    
{str1}
    </script>


<canvas id="target-canvas"></canvas>
<script>
    var canvas = document.getElementById('target-canvas');
    var noml = document.getElementById('noml').innerHTML;
    nomnoml.draw(canvas, noml);
</script>
"""

page1="""
<!DOCTYPE html>
<html>
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<head>
<style>
body {
  background-color: linen;
  margin: 10px; 
}
hr {
    display: block;
    width: 400px;
    margin-before: 0.5em;
    margin-after: 0.5em;
    margin-start: auto;
    margin-end: auto;
    overflow: hidden;
    border-style: inset;
    border-width: 1px;
}

.row {
}

.left {
   display: inline-block;
   text-align: right;
   width: 100px;
   padding: 10px;
}

.right {
   display: inline-block;
   padding: 10px;
}

.error {{
    color: red;
}}

</style>
</head>
<body>

<form action="/add" method="post">
  <div>Tables:</div>
  <select name="table_select">
    <option value="student">student</option>
    <option value="university">university</option>
    <option value="teaches">teaches</option>
  </select>
  <input type="submit" value="Select table" >
</form>
<hr>
<form action="/add" method="post">
  <div>Student:</div>
  <input type="hidden" name="table_name" value="student">
  <div class="row">
    <div class="left">id</div>
    <div class="right">
      <input type="text" name="id" value="2342">
    </div>
  </div>

  <div class="row">
    <div class="left">name</div>
    <div class="right">
      <input type="text" name="name">
    </div>
  </div>
    
  <div class="row">
    <div class="left">dept_name</div>
    <div class="right">
      <input type="text" name="dept_name">
    </div>
  </div>
    
  <div class="row">
    <div class="left">total_credit</div>
    <div class="right">
      <input type="text" name="total_credit">
    </div>
  </div>
 </div>
    
 <div class = "row">
   <div class="left"></div>
 <div class="right">
   <input type="submit" value="Add" >
 </div>
</form>
<div class="error"></div>
</body>

</html>
"""

class PGMetaHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/meta":
            conn = dbexec.connect()
            meta = pgmeta.get_meta_data(conn) # returns dbmeta 'Meta'
            graph=pgmeta.to_graph(meta)
            html = page.format(str1=graph)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode('utf-8')   )
            conn.close()
        elif self.path == "/add":
            conn = dbexec.connect()
            meta = pgmeta.get_meta_data(conn) # returns dbmeta 'Meta'
            html = pagef1
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            # print("point1")
            self.end_headers()
            # print("point2")
            self.wfile.write(html.encode('utf-8'))
            # print("point3")
            conn.close()
            # print("point4")
        else:
            SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        SimpleHTTPRequestHandler.do_GET(self)
        # print("point5")
        # self.rfile.read()
        # self.send_response(200)
        # self.end_headers()


httpd = HTTPServer( ('', 8000), PGMetaHandler)
httpd.serve_forever()