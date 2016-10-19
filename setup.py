from setuptools import find_packages, setup


from stopforumspam import __version__


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

packages = find_packages()

setup(
    name='stopforumspam',
    description='Django middleware for blocking IPs listed in stopforumspam.com',
    author="Benjamin Bach",
    author_email="benjamin@overtag.dk",
    version=__version__,
    packages=packages,
    license='BSD License',
    install_requires=[
        'Django>=1.7',
    ],
    url='https://overtag.dk/',
    classifiers=CLASSIFIERS,
    include_package_data=True,
)
