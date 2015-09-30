from __future__ import print_function
import os

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.ConfigDict import Config


class Nova(object):
    @classmethod
    def set_os_environ(cls, cloudname):
        """Set os environment variables on a given cloudname"""
        try:
            d = ConfigDict("cloudmesh.yaml")
            credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
            for key, value in credentials.iteritems():
                if key == "OS_CACERT":
                    os.environ[key] = Config.path_expand(value)
                else:
                    os.environ[key] = value
        except Exception, e:
            print(e)

    # noinspection PyPep8Naming
    @classmethod
    def remove_subjectAltName_warning(cls, content):
        result = []
        for line in content.split("\n"):
            if "Certificate has no `subjectAltName`" in line:
                pass
            elif "SecurityWarning" in line:
                pass
            else:
                result.append(line)
        return "\n".join(result)