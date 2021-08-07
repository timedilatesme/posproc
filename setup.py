from setuptools import find_packages, setup

with open("README.md", "r", encoding="UTF-8") as f:
    long_desc = f.read()

setup(
    name='posproc',
    python_requires='>=3.9.5',
    description='QKD post-processing software based on event based networking.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    version='0.1.0',
    url='https://github.com/nutanstrek/posproc',
    author='Paras Sharma, Tanmay Singh',
    author_email='nutanstrek@gmail.com',
    # license='MIT',
    keywords='qkd post-processing',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'colorama',
        'pyngrok',
        'bitstring',
        'jsonpickle',
        'starkbank-ecdsa',
    ],
    # dependency_links = [
    #     'https://github.com/starkbank/ecdsa-python.git'
    # ],
)
