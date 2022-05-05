"""Utilities for using XStatic in Tornado applications"""
import os.path
import tornado.web

__version__ = '0.3'

class XStaticFileHandler(tornado.web.StaticFileHandler):
    _cached_xstatic_data_dirs = {}

    def initialize(self, allowed_modules=None, **kwargs):
        if allowed_modules:
            self.allowed_modules = set(allowed_modules)
        else:
            self.allowed_modules = None

        assert 'root' not in kwargs
        # NOTE: Passing path=/ will not work on some conditions on windows
        # like the pip packages are install in C:/ and the code you are
        # running is in another partition.
        # see also https://github.com/tornadoweb/tornado/blob/v6.1.0/tornado/web.py#L2768
        # So change this to the root drive location of 'xstatic' package
        # for windows platform.
        from pathlib import Path
        from sys import platform
        path = '/' if platform != 'win32' else Path(__import__('xstatic').__path__[0]).drive
        super(XStaticFileHandler, self).initialize(path=path)

    def parse_url_path(self, url_path):
        if '/' not in url_path:
            raise tornado.web.HTTPError(403, "XStatic module, not a file")
        if self.allowed_modules is not None:
            module_name = url_path.split('/', 1)[0]
            if module_name not in self.allowed_modules:
                raise tornado.web.HTTPError(
                    403, 'Access to XStatic module %s denied', module_name)

        return super(XStaticFileHandler, self).parse_url_path(url_path)

    @classmethod
    def _get_xstatic_data_dir(cls, mod_name):
        try:
            return cls._cached_xstatic_data_dirs[mod_name]
        except KeyError:
            xsmod = getattr(__import__('xstatic.pkg', fromlist=[mod_name]), mod_name)
            data_dir = os.path.abspath(xsmod.BASE_DIR)
            if not data_dir.endswith(os.path.sep):
                # So joining ../datafoo will not be valid
                data_dir += os.path.sep
            cls._cached_xstatic_data_dirs[mod_name] = data_dir
            return data_dir

    @classmethod
    def get_absolute_path(cls, root, path):
        mod_name, path = path.split(os.path.sep, 1)
        root = cls._get_xstatic_data_dir(mod_name)
        abs_path = os.path.join(root, path)
        if not abs_path.startswith(root):
            raise tornado.web.HTTPError(
                403, "Request for file outside XStatic package %s: %s", mod_name, path)

        return abs_path


def url_maker(prefix, include_version=True):
    def make_url(package, path):
        if include_version:
            fs_style_path = package + os.path.sep + path.replace("/", os.path.sep)
            version_bit = "?v=" + XStaticFileHandler.get_version({'static_path': ''}, fs_style_path)
        else:
            version_bit = ""
        return prefix + package + "/" + path + version_bit
    return make_url


def xstatic_url(path, include_version=True):
    """ Returns helper function to make URL to xstatic resources.

    Note: Returned function is ui_method compatible.

    :arg path: Part of URI (eg. /xstatic/) should be
        the same as one used in handler URI match
    :arg include_version: Determines whether the generated URL should
        include the query string containing the version hash of the
        file corresponding to the give
    """
    helper_make_url = url_maker(path, include_version)

    def inner(handler, package, path):
        return helper_make_url(package, path)

    return inner
