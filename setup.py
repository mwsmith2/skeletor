from setuptools import setup

setup(
    name='skeletor',
    version='0.0.0',
    description='A flexible templating library',
    packages=['skeletor'],
    py_modules=['sk'],
    entry_points = {
        'console_scripts': ['sk=sk:main'],
    }
)