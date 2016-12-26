import os

import tornado.ioloop
import tornado.web

from nlp.luNlp import analyze_wod
from nlp.trackable import Builder

class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type')

    def get(self):
        self.write({'status': 'ok'})

    def post(self):
        wod = self.request.body
        if not wod:
          raise tornado.web.HTTPError(400)
        result = analyze_wod(wod)
        b = Builder.build(result)
        self.set_header('Content-Type', 'application/json')
        self.write({
          'input': wod,
          'output': b.todict(),
        })

    def options(self):
        self.set_status(204)
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    application = make_app()
    application.listen(os.environ.get('PORT', 8888))
    tornado.ioloop.IOLoop.current().start()