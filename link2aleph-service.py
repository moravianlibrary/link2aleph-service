from flask import Flask
from flask import request
from flask.ext.autoindex import AutoIndex
import codecs
import time
app = Flask(__name__)
idx = AutoIndex(app, '/data', add_url_rules=False)

#if app.debug is not True:
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    error_file_handler = RotatingFileHandler('error.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    error_file_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)
    
    access_file_handler = RotatingFileHandler('access.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    logger = logging.getLogger('werkzeug')
    logger.addHandler(access_file_handler)
    

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

def createLink():
    pid = request.args.get('pid')
    sysno = request.args.get('sysno')
    base = request.args.get('base')
    
    addLine = True
    date = (time.strftime("%d.%m.%Y"))
    fileName = "/data/" + base + "_" + date + ".txt"
    link = "http://kramerius.mzk.cz/search/handle/uuid:" + pid
    record = sysno + " 85641 L $$u" + link + u"$$yDigitalizovaný dokument"
    
    with codecs.open(fileName,"a+", "utf-8") as f:
        lines = f.readlines()
        for i in xrange(len(lines)):
            if sysno in lines[i]:
                lines[i] = record + "\n"
                addLine = False
        if addLine:
           lines.append(record + "\n")
    
    with codecs.open(fileName, "w", "utf-8") as f:
        f.writelines(lines)
    return link

@app.route('/index')
@app.route('/index/<path:path>')
def autoindex(path='.'):
    return idx.render_autoindex(path)

if __name__ == "__main__":
    #app.debug = True
    app.debug = False
    app.run('0.0.0.0')

