from setuptools import setup

setup(
    name='rake',
    author_name = "Ibraheem Mobolaji Abdulsalam",
    author_email = "ibmabdulsalam@gmail.com",
    version='0.1.0',
    py_modules=['rake'],
    install_requires=[
        'click',
        "requests",
        'pysimplegui',
        'bs4',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'rake = rake:cli'
        ],
    },
)