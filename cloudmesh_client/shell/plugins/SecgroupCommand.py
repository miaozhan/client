from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.secgroup import SecGroup
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint
from cloudmesh_client.common.Printer import Printer

class SecgroupCommand(PluginCommand, CloudPluginCommand):
    topics = {"secgroup": "security"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command secgroup")

    def _delete(self, arg):
        if arg.cloud is None:
            Console.ok("Delete secgroup {GROUP}".format(**arg))
            SecGroup.delete(group=arg.GROUP)
        else:
            Console.ok("Delete secgroup {cloud}:{GROUP}".format(**arg))
            result = SecGroup.delete_secgroup(name=arg.GROUP, cloud=arg.cloud)
            if result is not None:
                Console.ok("Security Group={GROUP} in cloud={cloud} deleted successfully."
                           .format(**arg))
            else:
                Console.error("Failed to delete Security Group={GROUP} in cloud={cloud}"
                              .format(**arg))


    # noinspection PyUnusedLocal
    @command
    def do_secgroup(self, args, arguments):
        """
        ::

            Usage:
                secgroup list [--format=FORMAT]
                secgroup list --cloud=CLOUD [--format=FORMAT]
                secgroup list GROUP [--format=FORMAT]
                secgroup add GROUP RULE FROMPORT TOPORT PROTOCOL CIDR
                secgroup delete GROUP [--cloud=CLOUD]
                secgroup delete GROUP RULE
                secgroup upload [GROUP] [--cloud=CLOUD]

            Options:
                --format=FORMAT Specify output format, in one of the following:
                                table, csv, json, yaml, dict. The default value
                                is 'table'.
                --cloud=CLOUD   Name of the IaaS cloud e.g. kilo,chameleoon.
                                The clouds are defined in the yaml file.
                                If the name "all" is used for the cloud all
                                clouds will be selected.

            Arguments:
                RULE          The security group rule name
                GROUP         The label/name of the security group
                FROMPORT      Staring port of the rule, e.g. 22
                TOPORT        Ending port of the rule, e.g. 22
                PROTOCOL      Protocol applied, e.g. TCP,UDP,ICMP
                CIDR          IP address range in CIDR format, e.g.,
                              129.79.0.0/16

            Description:
                security_group command provides list/add/delete
                security_groups for a tenant of a cloud, as well as
                list/add/delete of rules for a security group from a
                specified cloud and tenant.


            Examples:
                secgroup list
                secgroup list --cloud=kilo
                secgroup add my_new_group webapp 8080 8080 tcp 0.0.0.0/0
                seggroup delete my_group my_rule
                secgroup delete my_unused_group --cloud=kilo
                secgroup upload --cloud=kilo

            Description:

                Security groups are first assembled in a local database.
                Once they are defined they can be added to the clouds.

                secgroup list [--format=FORMAT]
                    lists all security groups and rules in the database

                secgroup list GROUP [--format=FORMAT]
                    lists a given security group and its rules defined
                    locally in the database

                secgroup list --cloud=CLOUD [--format=FORMAT]
                    lists the security groups and rules on the specified clouds.

                secgroup add GROUP RULE FROMPORT TOPORT PROTOCOL CIDR
                    adds a security rule with the given group and the details
                    of the security ruls

                secgroup delete GROUP [--cloud=CLOUD]
                    Deletes a security group from the local database. To make
                    the change on the remote cloud, using the 'upload' command
                    afterwards.
                    If the --cloud parameter is specified, the change would be
                    made directly on the specified cloud

                secgroup delete GROUP RULE
                    deletes the given rule from the group. To make this change
                    on the remote cloud, using 'upload' command.

                secgroup upload [GROUP] [--cloud=CLOUD...]
                    uploads a given group to the given cloud. If the cloud is
                    not specified the default cloud is used.
                    If the parameter for cloud is "all" the rules and groups
                    will be uploaded to all active clouds.
                    This will synchronize the changes (add/delete on security
                    groups, rules) made locally to the remote cloud(s).

        """

        arg = dotdict(arguments)
        if arguments["--cloud"] is not None:
            is_cloud = True
            arg.cloud = arguments["--cloud"] or Default.cloud
        else:
            is_cloud = False

        arg.FORMAT = arguments["--format"] or 'table'

        # list all security-groups in cloud

        if arguments["list"]:

            if not is_cloud:

                if arg.RULE is None:
                    print(SecGroup.list(group=arg.GROUP, name=arg.RULE, output=arg.FORMAT))
                else:
                    print(SecGroup.list(group=arg.GROUP, output=arg.FORMAT))

            else:

                print(SecGroup.list(category=arg.cloud, output=arg.FORMAT))

        elif arguments["add"]:

            try:
                SecGroup.add_rule_to_db(
                    name=arg.RULE,
                    group=arg.GROUP,
                    from_port=arg.FROMPORT,
                    to_port=arg.TOPORT,
                    protocol=arg.PROTOCOL,
                    cidr=arg.CIDR)
            except:
                Console.error("Problem adding security group to db")


        # Delete a security-group
        elif arguments["delete"]:
            if arg["RULE"] is not None:
                SecGroup.delete_rule_from_db(group=arg["GROUP"],
                                             name=arg["RULE"])
            else:
                self._delete(arg)

        elif arguments["upload"]:

            # rewrite the _delete
            #
            # upload does not implicitly deleting a secgroup anymore
            # instead, it will check and update the rules only
            # self._delete(arg)
            SecGroup.upload(cloud=arg.cloud, group=arg.GROUP)

        return ""


'''
    # Create a security-group
    elif arguments["create"]:

        # If default not set, terminate
        if arg.cloud is not None:
            Console.error("Default cloud not set.")
            return

        # Create returns uuid of created sec-group
        uuid = SecGroup.create(arg.label, arg.cloud)

        if uuid:
            Console.ok("Created a new security group={label} with UUID={uuid}"
                       .format(**arg))
        else:
            Console.error("Exiting!")
        return ""
'''