from distutils.core import setup

setup(name='BetterXML',
      version='1.0',
      description='BetterXML Python Distribution',
      url='http://www.betterxml.org/',
      package_dir = {'':'src'},
      packages = ['org', 'org.betterxml', 'org.betterxml.util',
                  'org.betterxml.nxml', 'org.betterxml.xelement1',
                  'org.betterxml.xelement2',],
     )

