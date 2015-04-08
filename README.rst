Utilities for using XStatic in Tornado applications
---------------------------------------------------

`XStatic <http://xstatic.readthedocs.org/en/latest/index.html>`_ is a means of
packaging static files, especially JS libraries, for Python applications.
`Tornado <http://www.tornadoweb.org/en/latest/>`_ is a Python web framework.

This integration provides:

- ``XStaticFileHandler`` to serve static files from XStatic packages.
- ``xstatic_url`` ui method to build URLs for XStatic files, including
  the ``?v=...`` tag  that Tornado uses for cache invalidation.

To use these:

.. code:: python

    import tornado.ioloop
    import tornado.web
    from tornado_xstatic import XStaticFileHandler, xstatic_url

    class MyHandler(tornado.web.RequestHandler):
        def get(self):
            self.render("mytemplate.html")


    if __name__ == "__main__":
        application = tornado.web.Application(
            [
                (r"/", MyHandler),
                (r"/xstatic/(.*)", XStaticFileHandler,
                    {"allowed_modules": ["jquery", "bootstrap"]}),
            ],
            ui_methods={'xstatic_url': xstatic_url('/xstatic/')}
        )
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

Passing ``allowed_modules`` is optional: if it is not provided, files from any
XStatic module may be served.

In your template, you can then do this::

    <script src="{{ xstatic_url('jquery', 'jquery.min.js') }}"></script>
    <script src="{{ xstatic_url('bootstrap', 'js/bootstrap.min.js') }}"></script>

    <link href="{{ xstatic_url('bootstrap', 'css/bootstrap.min.css') }}" rel="stylesheet">
