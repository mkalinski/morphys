# coding: utf-8

from setuptools import setup
import os


def _readme_text():
    here = os.path.dirname(__file__)

    with open(os.path.join(here, 'README.rst')) as f:
        return f.read()


if __name__ == '__main__':
    setup(
        name='morphys',
        version='1.0',
        license='MIT',

        description='Smart conversions between unicode and bytes types for '
        'common cases',
        long_description=_readme_text(),

        author='Michał Kaliński',
        url='https://github.com/mkalinski/morphys',

        keywords='string unicode bytes conversion',
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Utilities',
        ],

        py_modules=['morphys'],
        test_suite='tests',
    )
