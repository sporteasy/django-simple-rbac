from distutils.core import setup

setup(
    name='django-simple-rbac',
    version='0.1.1',
    author='SportEasy',
    author_email='contact@sporteasy.fr',
    packages=['django_simple_rbac'],
    url='https://github.com/sporteasy/django-simple-rbac',
    license='LICENSE.txt',
    description='Simple RBAC for Django 1.4.x.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.4.0",
        "simple-rbac >= 0.1.1",
    ],
)
