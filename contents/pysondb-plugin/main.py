import argparse


class Plugin:

    def __init__(self) -> None:
        pass

    def plugin_parser(self, subparser: argparse.ArgumentParser) -> None:
        """
        The subparser is passed in as the only argument, and you can add the arguments for you command
        here
        """
        pass

    def action(self, args: argparse.Namespace) -> None:
        """
            The action methods is called when the command is executed by the user and the entire
             args namespace is passed in.
        """
        pass
