from __future__ import print_function

from cloudmesh_client.common import Printer
# from cloudmesh_client.db.SSHKeyDBManager import SSHKeyDBManager
import cloudmesh_client
from cloudmesh_client.common.ConfigDict import ConfigDict

# from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client2 import CloudmeshDatabase
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.dotdict import dotdict

class readable_classproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)

# noinspection PyBroadException
class Default(object):
    """
    Cloudmesh contains the concept of defaults. Defaults can have
    categories (we will rename cloud to categories). A category can be a
    cloud name or the name 'general'. The category general is a 'global'
    name space and contains defaults of global value (in future we will
    rename the value to global).

    """

    __kind__ = "default"
    __provider__ = "general"

    cm = CloudmeshDatabase()


    @classmethod
    def list(cls,
             category=None,
             order=None,
             header=None,
             output='table'):
        """
        lists the default values in the specified format.
        TODO: This method has a bug as it uses format and output,
        only one should be used.

        :param category: the category of the default value. If general is used
                      it is a special category that is used for global values.
        :param format: json, table, yaml, dict, csv
        :param order: The order in which the attributes are returned
        :param output: The output format.
        :return:
        """
        if order is None:
            order, header = None, None
            order = ['user',
                     'category',
                     'name',
                     'value',
                     'updated_at']
            # order, header = Attributes(cls.__kind__, provider=cls.__provider__)
        try:
            if category is None:
                result = cls.cm.all(cls.__kind__)
            else:
                result = cls.cm.all(category=category, kind=cls.__kind__)

            return (Printer.write(result,
                                  order=order,
                                  output=output))
        except:
            Console.error("Error creating list")
            return None



    #
    # GENERAL SETTER AND GETTER METHOD
    #

    @classmethod
    def set(cls, key, value, category='general', user=None, type='str'):
        """
        sets the default value for a given category
        :param key: the dictionary key of the value to store it at.
        :param value: the value
        :param user: the username to store this default value at.
        :return:
        """
        try:
            o = cls.get(name=key)
            if o is not None:
                cls.cm.update(kind=cls.__kind__,
                              provider=cls.__provider__,
                              filter={'name': key},
                              update={'value': value,
                                      'type': type,
                                      'user': user,
                                      'category': category})

            else:
                t = cls.cm.table(provider=cls.__provider__, kind=cls.__kind__)
                o = t(name=key, value=value, type=type, user=user, category=category)
                cls.cm.add(o)
            cls.cm.save()
        except Exception as e:
            Console.error("problem setting key value {}={}".format(key, value))


    @classmethod
    def get(cls, name=None, category='default'):
        o = cls.cm.find(provider="general",
                        kind="default",
                        scope="first",
                        name=name)
        if o is None:
            return None

        return (o.value)

    @classmethod
    def delete(cls, name):
        cls.cm.delete(name=name, provider=cls.__provider__, kind=cls.__kind__)

    @classmethod
    def clear(cls):
        """
        deletes all default values in the database.
        :return:
        """
        cls.cm.delete(provider=cls.__provider__, kind=cls.__kind__)

    @readable_classproperty
    def cloud(cls):
        return cls.get(name="cloud")

    @readable_classproperty
    def image(cls):
        return cls.get(name="image", category=cls.Default.cloud)

    @readable_classproperty
    def flavor(cls):
        return cls.get(name="flavor", category=cls.Default.cloud)

    @readable_classproperty
    def lastvm(cls):
        return cls.get(name="vm")

    @readable_classproperty
    def group(cls):
        return cls.get(name="group")

    @readable_classproperty
    def key(cls):
        return cls.get(name="key")

    @readable_classproperty
    def debug(cls):
        return bool(cls.get(name="debug"))

    @readable_classproperty
    def refresh(cls):
        return bool(cls.get(name="refresh"))

    @readable_classproperty
    def debug(cls):
        return bool(cls.get(name="debug"))

    @readable_classproperty
    def cluster(cls):
        return cls.get(name="cluster")

    @readable_classproperty
    def loglevel(cls):
        return cls.get(name="loglevel")

    @classmethod
    def set_loglevel(cls, level):
        level = level or 'debug'
        level = level.lower()
        if level in ['debug',
                     'info',
                     'warnin',
                     'error',
                     'critical']:
            cls.set("loglevel", level)
        else:
            Console.error("unkown logging level. Setting to debug.")
            cls.set("loglevel", 'debug')

    @classmethod
    def set_cloud(cls, value):
        """
        sets the cloud in the category general
        :param value: the cloud as defined in cloudmesh.yaml
        :return:
        """
        cls.set("cloud", value)

    @classmethod
    def set_vm(cls, value):
        """
        sets the cloud in the category general
        :param value: the cloud as defined in cloudmesh.yaml
        :return:
        """
        cls.set("vm", value)

    @classmethod
    def set_image(cls, value, category):
        """
        sets the default image for a specific category.
        :param value: the image uuid or name
        :param category: the category
        :return:
        """
        cls.set("image", value, category=category)

    @classmethod
    def get_image(cls, category=None):
        """
        returns the image for a particular category
        :param category: the category
        :return:
        """
        if category is None:
            category = cls.cloud
        return cls.get("image", category=category)

    @classmethod
    def set_flavor(cls, value, category):
        """
        sets the default flavor for a particular category
        :param value: teh flavor name or uuid
        :param category: the category
        :return:
        """
        cls.set("flavor", value, category=category)

    @classmethod
    def get_flavor(cls, category=None):
        """
        gets ths flavor default for a category
        :param category: the category
        :return:
        """
        if category is None:
            category = cls.cloud
        return cls.get(name="flavor", category=category)

    @classmethod
    def set_group(cls, value):
        """
        sets the default group
        :param value: the group name
        :return:
        """
        cls.set("group", value)


    @classmethod
    def set_key(cls, name):
        """
        :param name: the key name
        :return:
        """
        cls.set("key", name)

    @classmethod
    def set_cluster(cls, value):
        """
        sets the default cluster
        :param value: the cluster name as defined in the cloudmesh yaml file.
        :return:
        """
        cls.set("cluster", value)

    @classmethod
    def set_debug(cls, value):
        """
        enables debugging
        :param value: True/False
        :return:
        """
        cls.set("debug", value)

    @classmethod
    def set_refresh(cls, value):
        """
        sets the default for all clouds to refresh
        :param value:
        :return:
        """
        cls.set("refresh", value)

    @classmethod
    def set_timer(cls, value):
        """
        sets the default for all clouds to timer
        :param value:
        :return:
        """
        cls.set("timer", value)


    '''
    @classmethod
    def load(cls, filename):

        config = ConfigDict(filename=filename)["cloudmesh"]
        clouds = config["clouds"]

        # FINDING DEFAULTS FOR CLOUDS

        for cloud in clouds:

            db = {
                "image": cls.get("image", cloud),
                "flavor": cls.get("flavor", cloud),
            }
            defaults = clouds[cloud]["default"]
            for attribute in ["image", "flavor"]:
                value = db[attribute]
                if attribute in defaults:
                    value = db[attribute] or defaults[attribute]
                Default.set(attribute, value, category=cloud)

        # FINDING DEFAUlTS FOR KEYS
        # keys:
        #     default: id_rsa
        #     keylist:
        #       id_rsa: ~/.ssh/id_rsa.pub

        # key_db = SSHKeyDBManager()

        name_key = cls.get("key")

        keys = config["keys"]
        name = keys["default"]
        if name in keys["keylist"]:
            value = name_key or keys["keylist"][name]
            # key_db.add(value, keyname=name)

        # Check if the key is already set
        exist_key = cls.get_key()

        # Set the key only if there is no existing value in the DB.
        if exist_key is None:
            Default.set_key(name)
    '''