import utils
from templates.plugin_template import PluginBase
import privileges as pv
import time


class Plugin(PluginBase):
    start_time = None

    help_data = "<br><b><font color='red'>#####</font> Bot_Commands Plugin Help <font color='red'>#####</font></b><br> \
            All commands can be run by typing it in the channel or privately messaging DuckBot.<br>\
            <b>!echo 'message/image'</b>: Echoes a message/image in the chat.<br>\
            <b>!make 'channel_name'</b>: Creates a channel with the given name.<br>\
            <b>!move 'channel_name'</b>: Moves to an existing channel with the given name.<br>\
            <b>!joinme</b>: Moves to the users channel.<br>\
            <b>!msg 'username' 'message'</b>: Anonymously private messages a user from the bot.<br>\
            <b>!leave</b>: Moves the bot to the default channel.<br>\
            <b>!exit/!quit</b>: Initializes the bot exit procedure.<br>\
            <b>!version</b>: Displays the bot version.<br>\
            <b>!status</b>: Displays the bots current status.<br>\
            <b>!refresh</b>: Refreshes all plugins.<br>\
            <b>!about</b>: Displays the bots about screen."

    def __init__(self):
        print("Bot_Commands Plugin Initialized.")
        super().__init__()
        self.start_time = time.time()

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        all_messages = message[1:].split()
        command = message_parse[0]

        if command == "echo":
            if utils.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                return
            parameter = message_parse[1]
            utils.echo(utils.get_my_channel(mumble), parameter)
            return

        elif command == "msg":
            if utils.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                return
            utils.msg(mumble, all_messages[1], message[1:].split(' ', 2)[2])
            return

        elif command == "move":
            if utils.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                return
            parameter = message_parse[1]
            channel_name = parameter
            if channel_name == "default" or channel_name == "Default":
                channel_name = utils.get_default_channel()
            channel_search = utils.get_channel(mumble, channel_name)
            if channel_search is None:
                return
            else:
                channel_search.move_in()
                utils.echo(channel_search, "DuckBot was moved by %s" % mumble.users[text.actor]['name'])
            return

        elif command == "make":
            if utils.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                return
            parameter = message_parse[1]
            channel_name = parameter
            utils.make_channel(mumble, mumble.channels[mumble.users.myself['channel_id']], channel_name)
            return

        elif command == "leave":
            utils.leave(mumble)
            return

        elif command == "joinme":
            if utils.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                return
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "Joining user: %s" % mumble.users[text.actor]['name'])
            mumble.channels[mumble.users[text.actor]['channel_id']].move_in()
            return

        elif command == "version":
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "DuckBot is on version %s" % utils.get_version())
            return

        elif command == "about":
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "%s" % utils.get_about())
            return

        elif command == "blacklist":
            if utils.privileges_check(mumble.users[text.actor]) != pv.Privileges.ADMIN:
                return
            try:
                parameter = message_parse[1]
                result = utils.add_to_blacklist(parameter)
                if result is True:
                    utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               "User: %s added to the blacklist." % parameter)
                else:
                    utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               "User: %s could not be added to the blacklist." % parameter)
            except IndexError:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           utils.get_blacklist())
            return

        elif command == "whitelist":
            if utils.privileges_check(mumble.users[text.actor]) != pv.Privileges.ADMIN:
                return
            parameter = message_parse[1]
            result = utils.remove_from_blacklist(parameter)
            if result is True:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "User: %s removed from the blacklist." % parameter)
            else:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "User: %s could not be removed from the blacklist." % parameter)

    @staticmethod
    def plugin_test():
        print("Bot_Commands Plugin self-test callback.")

    def quit(self):
        print("Exiting Bot_Commands Plugin...")

    def help(self):
        return self.help_data