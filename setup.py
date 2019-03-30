import setuptools
import os

this_dir = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(this_dir, 'README.md'), encoding='utf-8').read()

setuptools.setup(
    name='susy-tester',
    version='0.0.1.post1',
    license='MIT',
    description='Testador de soluções para o SuSy da UNICAMP',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Lucas Valente',
    author_email='lucasvvop@hotmail.com',
    url='https://www.github.com/serramatutu/susy-tester',
    packages=['susytester'],
    install_requires=['termcolor', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)