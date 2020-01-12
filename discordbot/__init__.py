import importlib
import os
from glob import glob

from discord.ext.commands import CogMeta, Cog
from discord.ext.commands.bot import Bot

from discordbot.Common.config import Config
from discordbot.Modules.Settings import Settings
from discordbot.Modules.Storage import Storage


class DiscordBot(Bot):
    def __init__(self, debug=False):
        self.debug = debug

        self.config = Config()
        self.config.init_module('bot', defaults={'prefix': '', 'token': '!'})

        super().__init__(command_prefix=self.config.get_setting('bot', 'prefix', 'BOT_PREFIX', '!'))

        self.add_cog(Storage(self))
        self.add_cog(Settings(self))

    def load_modules(self, path: str = "./Modules"):
        modules = [os.path.normpath(x) for x in glob("{}/*/__init__.py".format(path))]

        loader = {}
        for module in modules:
            module = module.replace("\\", "/").replace("//", "/").replace("/__init__.py", '').split('/')
            package = ".".join(module[0:-1])
            module = str(module[-1])
            if not module.startswith("_"):
                impt = importlib.import_module(".{}".format(module), package=package)
                for item in [x for x in dir(impt) if not x.startswith("_")]:
                    cog = getattr(impt, item)
                    if isinstance(cog, Cog) or isinstance(cog, CogMeta):
                        if item in loader.keys():
                            # Module Collision
                            del loader[item]
                        elif hasattr(cog, 'deps'):
                            loader[item.lower()] = {'deps': [x.lower() for x in getattr(cog, 'deps')], 'cog': cog}
                        else:
                            loader[item.lower()] = {'deps': None, 'cog': cog}
        loaded = []
        while True:
            if len(loader.keys()) == 0:
                break
            loop = loader.copy()
            for name, value in loop.items():
                name = name.lower()
                if value['deps'] is None:
                    cog = value['cog']
                    self.add_cog(cog(self))
                    loaded.append(name)
                    del loader[name]
                else:
                    deps = value['deps']
                    deps.sort()
                    loaded.sort()
                    if deps == loaded:
                        cog = value['cog']
                        self.add_cog(cog(self))
                        loaded.append(name)
                        del loader[name]
        del loader
        return loaded

    def run(self, *args, **kwargs):
        self.load_modules()
        if self.debug:
            print("Loaded: {}".format(", ".join(self.cogs)))
        super().run(self.config.get_setting('bot', 'token', 'BOT_TOKEN', ''), *args, **kwargs)
