from setuptools import setup

setup(
    name='pahom',
    version='0.4.5',
    packages=['pahom'],
    install_requires=[
        'python-telegram-bot',
        'apiai',
        'markovify',
        'flask',
        'flask_limiter'
    ],
    include_package_data=True,
    zip_safe=False
    # python3 setup.py sdist
    # to setup: pip3 install pahom-0.1.tar.gzc
    # to update: pip3 install pahom-0.1.tar.gzc --upgrade
    # to run this shit use:
    # python3 -m pahom
    # to run in backgroud use bash nohup
)
