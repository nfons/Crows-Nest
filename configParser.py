import pycurl
from io import BytesIO
import yaml

class ConfigParser:
    def __init__(self, gitRepo):
        self.config = None
        self.gitRepo = gitRepo
        self.getGitFile()
        self.parseYaml()


    def getGitFile(self):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.gitRepo)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        body = buffer.getvalue()
        # Body is a byte string.
        # We have to know the encoding in order to print it to a text file
        # such as standard output.
        self.configstring = body.decode('iso-8859-1')

    def parseYaml(self):
        self.config = yaml.load(self.configstring)


    def getConfig(self):
        return self.config

