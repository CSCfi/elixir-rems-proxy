from setuptools import setup

setup(
    name='elixir_rems_proxy',
    version='0.2.dev',
    description='ELIXIR Permissions API proxy for REMS API',
    long_description_content_type='text/markdown',
    project_urls={
        'Source': 'https://github.com/CSCfi/elixir-rems-proxy',
    },
    author='CSC - IT Center for Science',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: Proxy Servers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
    packages=['elixir_rems_proxy', 'elixir_rems_proxy/utils'],
    install_requires=['aiohttp'],
    entry_points={
        'console_scripts': [
            'elixir_api=elixir_rems_proxy.app:main',
        ],
    },
)
