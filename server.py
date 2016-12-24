import tornado.ioloop
import tornado.web

from nlp.luNlp import analyze_sentence
from nlp.trackable import Builder

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        result = analyze_sentence("3 by five snatches 135 pounds")
        b = Builder.build(result)
        self.set_header('Content-Type', 'application/json')
        self.write(b.todict())

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()