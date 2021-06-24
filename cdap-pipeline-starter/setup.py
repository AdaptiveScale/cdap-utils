from setuptools import setup

setup(
    name="batch-pipeline-starter",
    version='0.1',
    py_modules=['cdf_batch_pipeline_start'],
    install_requires=[
        'Click',
        'Requests',
        'pydash'
    ],
    entry_points='''
        [console_scripts]
        batch-pipeline-starter=cdf_batch_pipeline_start:main
    ''',
)