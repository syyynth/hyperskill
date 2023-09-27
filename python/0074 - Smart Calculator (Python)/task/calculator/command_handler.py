from constants import MSG_UNKNOWN_COMMAND, MSG_HELP, MSG_EXIT


class CommandHandler:
    def __init__(self):
        self.commands = {
            '/help': MSG_HELP,
            '/exit': MSG_EXIT,
        }

    def parse_command(self, command):
        return self.commands.get(command, MSG_UNKNOWN_COMMAND)
