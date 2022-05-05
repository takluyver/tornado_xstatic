"""A tiny application using tornado_xstatic

You need the XStatic-jQuery package installed as well.
"""
import tornado.ioloop
import tornado.web
from tornado_xstatic import XStaticFileHandler, xstatic_url


class MyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("eg_template.html")


if __name__ == "__main__":
    application = tornado.web.Application(
        [
            (r"/", MyHandler),
            (r"/xstatic/(.*)", XStaticFileHandler, {"allowed_modules": ["jquery"]}),
        ],
        ui_methods={'xstatic': xstatic_url('/xstatic/')}
    )
    application.listen(8888)
    print("Open http://localhost:8888/ in your browser")
    tornado.ioloop.IOLoop.instance().start()
