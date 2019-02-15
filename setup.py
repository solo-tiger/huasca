from setuptools import setup,find_packages
from os import path

with open('README.md') as f:
    long_description = f.read()

name = 'huasca'
version = '0.2.1'

from shutil import copyfile
_workdir = path.abspath(path.dirname(__file__))
copyfile(_workdir+'/README.md',_workdir+'/{0}/__doc__'.format(name))

setup(name=name
    , version=version
    , description='out-of-the-box computer vision'
    , long_description=long_description
    , long_description_content_type='text/markdown'
    , author = 'Michael Stewart'
    , author_email = 'statueofmike@gmail.com'
    , url='https://github.com/statueofmike/{}'.format(name)
    , download_url="https://github.com/statueofmike/{0}/archive/{1}.tar.gz".format(name,version)
    , license='MIT'
    , packages=find_packages()
    , include_package_data=True     # includes files from e.g. MANIFEST.in
    , classifiers=[
        #'Development Status :: 5 - Production/Stable',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Information Analysis'
      ]
    , keywords='computer-vision'
    , install_requires=['keras','tensorflow','numpy','pillow','requests']
    , python_requires='>=3.5'
    , zip_safe=True
     )


