from configparser import ConfigParser

config = ConfigParser()
config = config.read("config.ini")
print(config)
