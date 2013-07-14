from setuptools import setup
import os

setup(name='chorescore',
    version='0.1pre',
    description='Gamify your chores.',
    author='Adam Brenecki',
    author_email='adam@brenecki.id.au',
    url='https://github.com/adambrenecki/chorescore',
    packages=['.'.join(i[0].split(os.sep))
        for i in os.walk('.')
        if '__init__.py' in i[2]],
    install_requires=[
        'django',
    ],
)
