import tornado.ioloop
import tornado.web
from tornado_xstatic import XStaticFileHandler, xstatic_ui_method


class MyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("eg_template.html")


if __name__ == "__main__":
    application = tornado.web.Application(
        [
            (r"/", MyHandler),
            (r"/xstatic/(.*)", XStaticFileHandler, {"allowed_modules": ["jquery"]}),
        ],
        ui_methods={'xstatic': xstatic_ui_method('/xstatic/')}
    )
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
