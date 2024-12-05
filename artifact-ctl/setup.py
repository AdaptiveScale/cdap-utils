from setuptools import setup

setup(
    name="artifact-ctl",
    version='0.1',
    py_modules=['artifact_ctl.py'],
    install_requires=[
        'Click',
        'Requests'
    ],
    entry_points='''
        [console_scripts]
        artifact-ctl=artifact_ctl:main
    ''',
)
