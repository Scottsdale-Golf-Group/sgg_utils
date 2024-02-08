from setuptools import setup

setup(
    name='sgg_utils',
    version='1.0',
    description='Tools for interacting with the ForeUp API.',
    author='Michael Futch',
    author_email='michael.d.futch@gmail.com',
    url='https://github.com/michaeldfutch/sgg_utils',
    packages=['sgg_utils'],
    install_requires=[
        # Add any dependencies your module requires
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)