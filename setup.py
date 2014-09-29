from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(name="tornado_xstatic",
      version='0.1',
      description="Utilities for using XStatic in Tornado applications",
      long_description=readme,
      author='Thomas Kluyver',
      author_email="thomas@kluyver.me.uk",
      url="https://github.com/takluyver/tornado_xstatic",
      py_modules=['tornado_xstatic'],
      classifiers=[
          "Environment :: Web Environment",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 3",
          "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
         ],)