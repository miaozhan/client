from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import dict_printer, attribute_printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider

from cloudmesh_client.cloud.ListResource import ListResource


class Image(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def clear(cls, cloud):
        """
        This method deletes all images of the cloud
        :param cloud: the cloud name
        """
        try:
            image = cls.cm.find('image',
                                output='object',
                                cloud=cloud).all()

            for ima in image:
                cls.cm.delete(ima)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def refresh(cls, cloud):
        """
        This method would refresh the image list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """
        # Newly implemented refresh
        return cls.cm.refresh("image", cloud)

    @classmethod
    def list(cls, cloud, format="table"):
        """
        This method lists all images of the cloud
        :param cloud: the cloud name
        """
        # TODO: make a CloudmeshDatabase without requireing the user=
        cm = CloudmeshDatabase()

        try:
            elements = cm.find("image", cloud=cloud)

            # order = ['id', 'uuid', 'name', 'cloud']
            (order, header) = CloudProvider(cloud).get_attributes("image")

            # order = None

            return dict_printer(elements,
                                order=order,
                                header=header,
                                output=format)

        except Exception as ex:
            Console.error(ex.message, ex)


@classmethod
def details(cls, cloud, id, live=False, format="table"):
    if live:
        cls.refresh(cloud)

    try:
        cm = CloudmeshDatabase()

        elements = None
        for idkey in ["name", "uuid", "id"]:
            s = {idkey: id}
            try:
                elements = cm.find("image", cloud=cloud, **s)
            except:
                pass
            if len(elements) > 0:
                break

        if len(elements) == 0:
            return None

        if format == "table":
            element = elements.values()[0]
            return attribute_printer(element)
        else:
            return dict_printer(elements,
                                output=format)
    except Exception as ex:
        Console.error(ex.message, ex)


if __name__ == "__main__":
    Image.details("india", "58c9552c-8d93-42c0-9dea-5f48d90a3188")
