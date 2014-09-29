import tornado.ioloop
import tornado.web
import tornado_xstatic

class MyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("eg_template.html",
                    xstatic=self.application.settings['xstatic_url'])

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MyHandler),
        (r"/xstatic/(.*)", tornado_xstatic.XStaticFileHandler,
            {"allowed_modules": ["jquery"]}),
    ], xstatic_url=tornado_xstatic.url_maker("/xstatic/")
    )
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
