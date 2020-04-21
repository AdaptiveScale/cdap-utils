from setuptools import setup

setup(
    name="upload-plugin",
    version='0.1',
    py_modules=['deploy_artifact_cli'],
    install_requires=[
        'Click',
        'Requests'
    ],
    entry_points='''
        [console_scripts]
        upload-plugin=deploy_artifact_cli:main
    ''',
)