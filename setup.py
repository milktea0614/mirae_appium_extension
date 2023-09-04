from setuptools import setup

with open('README.md', encoding='utf-8') as _f:
    long_description = _f.read()

setup(
    name='mirae_appium_extension',
    version='0.0.1',
    packages=['mirae_appium_extension'],
    url='https://github.com/milktea0614/mirae_appium_extension',
    license='',
    author='Jang, Mirae',
    author_email='milktea0614@naver.com',
    description='Appium extension for me.',
    keywords=['pypi deploy', 'miraelogger'],
    python_requires='>=3',  # Requires python version
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    long_description=long_description,  # for pypi description
    long_description_content_type='text/markdown',
    install_requires=[
        'Appium-Python-Client~=2.11.1',
        'miraelogger~=0.0.2'
    ]
)
