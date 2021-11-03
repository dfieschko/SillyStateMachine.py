from distutils.core import setup

setup(
  name = 'SillyStateMachine',
  packages = ['SillyStateMachine'],
  version = '0.1.0',
  license='MIT',
  description = 'A simple, threaded finite state machine that looks up function pointers in a dict.',
  long_description = open('README.md').read(),
  long_description_content_type = 'text/markdown',
  author = 'Darius Fieschko',
  author_email = 'dfieschko@gmail.com',
  url = 'https://github.com/dfieschko/RP1210',
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
  ]
)
