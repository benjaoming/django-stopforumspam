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

packages = find_packages()

def build_media_pattern(base_folder, file_extension):
    return ["%s/%s*.%s" % (base_folder, "*/"*x, file_extension) if base_folder else "%s*.%s" % ("*/"*x, file_extension) for x in range(10)]

media_patterns = ( build_media_pattern("templates", "html") +
     	           build_media_pattern("static", "js") +
                   build_media_pattern("static", "css") +
                   build_media_pattern("static", "png") +
                   build_media_pattern("static", "jpeg") +
                   build_media_pattern("static", "gif") +
                   build_media_pattern("", "md")
)

package_data = dict(
    (package_name, media_patterns)
    for package_name in packages
)

setup(name='stopforumspam',
      description='Django middleware for blocking IPs listed in stopforumspam.com',
      author="Benjamin Bach",
      author_email="benjamin@overtag.dk",
      version='1.5',
      packages=packages,
      license='BSD License',
      install_requires=[
        'Django>=1.7',
      ],
      url='https://overtag.dk/',
      classifiers=CLASSIFIERS,
      include_package_data=True,
      package_data=package_data,
)
