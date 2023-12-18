from setuptools import setup, find_packages

with open('requirements.txt',  encoding='utf-8') as f:
    required = f.read().splitlines()

setup(
    name='route-halo',
    version='0.1.1',
    description='Halo the route optimizer tool',
    author='Hoil Jeong',
    author_email='me@haoyi.dev',
    packages=find_packages(exclude=['tests'], where='src'),
    package_dir={'': 'src'},
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lavi02/Halo',
    install_requires=required,
    keywords=['route', 'optimizer', 'tsp', 'traveling', 'salesman'],
    python_requires='>=3.8',
)

