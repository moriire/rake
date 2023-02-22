from setuptools import setup

setup(
    name='rake',
    author = "Ibraheem Mobolaji Abdulsalam",
    author_email = "ibmabdulsalam@gmail.com",
    version='0.1.0',
    py_modules=['rake'],
    install_requires=[
        'click',
        'pysimplegui',
        'bs4',
        #'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'start-rake = rake:index',
            'rake = rake:cli'
        ],
    },
)