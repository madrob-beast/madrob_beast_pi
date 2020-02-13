import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='madrob_beast_pi',
    version='0.1.0',
    author='João Pereira',
    author_email='95joaopereira@gmail.com',
    description='Performance indicators for the MADROB and BEAST benchmarks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/joaomacp/madrob_beast_pi',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.7.12',
    install_requires=[
        'pyyaml',
        'numpy>=1.16.6',
        'pandas',
        'scipy'
    ]
)