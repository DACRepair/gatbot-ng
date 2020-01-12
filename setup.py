#!/usr/bin/env python3
from setuptools import setup

setup(name='discordbot-base',
      version='1.0.2',
      description='Bot Framework for Discord',
      author='DACRepair',
      author_email='DACRepair@gmail.com',
      url='https://github.com/CerberusGaming/discordbot-base',
      install_requires=[
          'discord.py',
          'sqlalchemy'
      ],
      packages=['discordbot-base',
                'discordbot-base.Common',
                'discordbot-base.Modules',
                'discordbot-base.Modules.Settings',
                'discordbot-base.Modules.Storage'])