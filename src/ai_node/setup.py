from setuptools import find_packages, setup

package_name = 'ai_node'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='you',
    maintainer_email='you@example.com',
    description='AI perception node',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ai_node = ai_node.ai_node:main',
        ],
    },
)
