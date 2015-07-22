"""Utilities for using XStatic in Tornado applications"""
import os.path
import tornado.web

__version__ = '0.2'

class XStaticFileHandler(tornado.web.StaticFileHandler):
    _cached_xstatic_data_dirs = {}
    default_filename = None

    def initialize(self, allowed_modules=None, **kwargs):
        if allowed_modules:
            self.allowed_modules = set(allowed_modules)
        else:
            self.allowed_modules = None

        # Not calling parent initialize() here because there's no root to set.
        # If SFH ever gains further attributes set in initialize(), we'll need
        # to copy them here.

    @classmethod
    def get_xstatic_data_dir(cls, mod_name):
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

    def get(self, path, include_body=True):
        if '/' not in path:
            raise tornado.web.HTTPError(403, "XStatic module, not a file")

        mod, path = path.split('/')
        if (self.allowed_modules is not None) and (mod not in self.allowed_modules):
            raise tornado.web.HTTPError(
                403, 'Access to XStatic module %s denied', mod)

        # This stateful setting of root seems awkward, but SFH is already stateful
        # (self.path, self.absolute_path, self.modified), and from examining
        # the code of SFH, this should work.
        self.root = self.get_xstatic_data_dir(mod)
        return super(XStaticFileHandler, self).get(path, include_body=include_body)


def url_maker(prefix, include_version=True):
    def make_url(package, path):
        if include_version:
            fs_style_path = path.replace("/", os.path.sep)
            pkg_dir = XStaticFileHandler.get_xstatic_data_dir(package)
            version_bit = "?v=" + XStaticFileHandler.get_version(
                                        {'static_path': pkg_dir}, fs_style_path)
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
