from setuptools import setup, find_packages

setup(
    name='mindcanvas',
    version='0.1.0',
    description='A Flask-based journaling app',
    long_description=open('README.md').read(),
    author='Indrajit Ghosh',
    author_email='rs_math1902@isibang.ac.in',
    url='https://github.com/indrajit912/MindCanvas',
    packages=find_packages(),
    install_requires=[
        "Flask",
        "gunicorn",
        "python-dotenv",
        "pytz",
        "cryptography"
    ],
    entry_points={
        'console_scripts': [
            'mindcanvas=run:app',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
