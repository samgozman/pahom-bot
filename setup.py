from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='pahom',
    version='0.1.7',
    packages=['pahom'],
    install_requires=[
        'python-telegram-bot',
        'apiai',
        'markovify',
        'emoji',
        'tqdm'
    ],
    # data_files=[('pahom', ['pahom/shiza.txt', 'pahom/markov.txt'])],
    include_package_data=True,
    zip_safe=False
    # long_description=open(join(dirname(__file__), 'README.txt')).read(),
    # python3 setup.py sdist
    # to setup: pip3 install pahom-0.1.tar.gzc
    # to update: pip3 install pahom-0.1.tar.gzc --upgrade
    # to run this shit use:
    # python3 -m pahom.__init__
    # to run in backgroud use bash nohup
)