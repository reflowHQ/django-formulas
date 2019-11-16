from setuptools import setup, find_packages

setup(
    name='django-formulas',
    version='0.1.0',
    url='https://github.com/reflowHQ/django-formulas',
    license='MIT',
    description='A minimal lib to write custom formulas on Django',
    long_description=open('README.md', 'r').read(),
    author='Nicolas Melo',
    author_email='nicolasmelo12@gmail.com',
    install_requires=[
        'django'
    ],
    python_requires='>=3.6,<3.8',
    extras_require={},
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)