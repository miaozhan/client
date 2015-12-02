from __future__ import print_function
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command, PluginCommand, \
    CloudCommand, CometCommand
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.cloud.launcher import Launcher


class LauncherCommand(PluginCommand, CloudCommand, CometCommand):
    topics = {"launcher": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command launcher")

    @command
    def do_launcher(self, args, arguments):
        """
        ::

          Usage:
              launcher list [--cloud=CLOUD] [--format=FORMAT] [--all]
              launcher kill KEY [--cloud=CLOUD]
              launcher run
              launcher resume
              launcher suspend
              launcher details
              launcher clear
              launcher refresh

          Arguments:

            KEY    the name of the launcher

          Options:

             --cloud=CLOUD    the name of the cloud
             --format=FORMAT  the output format [launcher: table]
             --all            lists all the launcher values

        Description:

        Launcher is a command line tool to test the portal launch functionalities through command

        The current launcher values can by listed with --all option:(
        if you have a launcher cloud specified. You can also add a
        cloud parameter to apply the command to a specific cloud)

               launcher list

            A launcher can be deleted with

                launcher kill KEY


        Examples:
            launcher list --all
            launcher list --cloud=general
            launcher kill <KEY>
        """
        # pprint(arguments)

        cloud = arguments["--cloud"] or Default.get_cloud()
        launcher = Launcher()

        if cloud is None:
            Console.error("Default cloud not set")
            return

        if arguments["list"]:
            result = launcher.list()
            print (result)

        elif arguments["kill"]:
            result = launcher.kill()
            print (result)

        elif arguments["run"]:
            result = launcher.run()
            print (result)

        elif arguments["resume"]:
            result = launcher.resume()
            print (result)

        elif arguments["suspend"]:
            result = launcher.suspend()
            print (result)

        elif arguments["details"]:
            result = launcher.details()
            print (result)

        elif arguments["clear"]:
            result = launcher.clear()
            print (result)

        elif arguments["refresh"]:
            result = launcher.refresh()
            print (result)


if __name__ == '__main__':
    command = Launcher
    command.do_launcher("list")
    command.do_launcher("run")
    command.do_launcher("suspend")