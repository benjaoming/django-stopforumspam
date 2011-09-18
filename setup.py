from setuptools import setup, find_packages
import os

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


setup(name='stopforumspam',
      description='Django middleware for blocking IPs from stopforumspam.com',
      long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
      author="Benjamin Bach",
      author_email="benjamin@overtag.dk",
      version='1.0',
      packages=find_packages(),
      license='BSD License',
      install_requires=[
        'Django>=1.2.0',
      ],
      url='https://overtag.dk/',
      classifiers=CLASSIFIERS,
      include_package_data=True,
      )
