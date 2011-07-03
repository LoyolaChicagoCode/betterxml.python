from distutils.core import setup

setup(name='BetterXML',
      version='1.0',
      description='BetterXML Python Distribution',
      url='http://www.betterxml.org/',
      package_dir = {'':'src'},
      packages = ['betterxml', 'betterxml.util',
                  'betterxml.nxml', 'betterxml.xelement1',
                  'betterxml.xelement2', 'betterxml.xir' ],
      scripts = [ 'src/betterxml/xir/xirgen', 'src/betterxml/xir/xirecho'  ]
     )

