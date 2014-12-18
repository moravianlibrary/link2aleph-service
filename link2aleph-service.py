from flask import Flask
from flask import request
app = Flask(__name__)

# comma separated list of URLs where http get is sent after successful ingest
# you may want to use following variables:
# ${pid}, ${sysno}, ${name}
# NOTE: it is also possible to use substring extraction:
# i.e. ${pid:5} is 'pid' without first 5 characters
#      ${sysno:-8} is last 8 characters of 'sysno'
#      ${name:2:4} is a substring of name starting by 2nd char and ending by 4th character
#      ${pid::5} only first 5 characters
#      ${pid::-5} pid without last 5 characters
#postIngestHooks=http://192.168.0.25:8080/katalog/l.dll?bqkram2clav~clid=${sysno::8}&uuid=${pid:5}
@app.route("/link2aleph")
def hello():
    pid = request.args.get('pid')
    name = request.args.get('name')
    sysno = request.args.get('sysno')
    return sysno

if __name__ == "__main__":
    app.debug = True
    app.run()

