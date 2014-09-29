Utilities for using XStatic in Tornado applications
---------------------------------------------------

`XStatic <http://xstatic.readthedocs.org/en/latest/index.html>`_ is a means of
packaging static files, especially JS libraries, for Python applications.
`Tornado <http://www.tornadoweb.org/en/latest/>`_ is a Python web framework.

This integration provides two pieces:

- ``XStaticFileHandler`` to serve static files from XStatic packages.
- ``url_maker`` to build URLs for XStatic files, including the ``?v=...`` tag
  that Tornado uses for cache invalidation.

To use these:

.. code:: python

    import tornado.ioloop
    import tornado.web
    import tornado_xstatic
    
    class MyHandler(tornado.web.RequestHandler):
        def get(self):
            self.render("mytemplate.html",
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

Passing ``allowed_modules`` is optional: if it is not provided, files from any
XStatic module may be served.

In your template, you can then do this::

    <script src="{{ xstatic('jquery', 'jquery.min.js') }}"></script>
