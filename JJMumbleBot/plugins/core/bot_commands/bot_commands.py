from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils import runtime_utils as rutils
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.database_management_utils import get_memory_db
from JJMumbleBot.lib.utils.database_utils import GetDB
from fuzzywuzzy import process


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def cmd_echo(self, data):
        split_data = data.message.strip().split(' ', 1)
        if len(split_data) != 2:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}echo 'message'")
            gs.gui_service.quick_gui(
                f"Incorrect format! Format: {rutils.get_command_token()}echo 'message'",
                text_type='header',
                box_align='left', user=gs.mumble_inst.users[data.actor]['name'],
                ignore_whisper=True)
            return
        to_echo = split_data[1]
        gs.gui_service.quick_gui(to_echo, text_type='header', box_align='left', ignore_whisper=True)
        dprint(f"Echo:[{to_echo}]", origin=L_COMMAND)
        log(INFO, f"Echo:[{to_echo}]", origin=L_COMMAND)

    def cmd_msg(self, data):
        split_data = data.message.strip().split(' ', 2)
        if len(split_data) != 3:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}msg 'username' 'message'")
            gs.gui_service.quick_gui(
                f"Incorrect format! Format: {rutils.get_command_token()}msg 'username' 'message'",
                text_type='header',
                box_align='left', user=gs.mumble_inst.users[data.actor]['name'],
                ignore_whisper=True)
            return
        send_to = split_data[1]
        message_to_send = split_data[2]

        gs.gui_service.quick_gui(message_to_send, text_type='header', box_align='left',
                                 user=send_to,
                                 ignore_whisper=True)
        dprint(f"Msg:[{send_to}]->[{message_to_send}]", origin=L_COMMAND)
        log(INFO, f"Msg:[{send_to}]->[{message_to_send}]", origin=L_COMMAND)

    def cmd_log(self, data):
        split_data = data.message.strip().split(' ', 1)
        if len(split_data) != 2:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}log 'message'")
            gs.gui_service.quick_gui(
                f"Incorrect format! Format: {rutils.get_command_token()}log 'message'",
                text_type='header',
                box_align='left', user=gs.mumble_inst.users[data.actor]['name'],
                ignore_whisper=True)
            return
        to_log = split_data[1]
        dprint(f"Manually Logged: [{to_log}]", origin=L_LOGGING)
        log(INFO, f'Manually Logged: [{to_log}]', origin=L_LOGGING)

    def cmd_showplugins(self, data):
        cur_text = f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>All Plugins:</font>"
        for i, plugin in enumerate(gs.bot_plugins.keys()):
            cur_text += f"<br><font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{plugin}]"
        gs.gui_service.quick_gui(
            cur_text,
            text_type='header',
            box_align='left',
            text_align='left',
            ignore_whisper=True,
            user=gs.mumble_inst.users[data.actor]['name']
        )

    def cmd_move(self, data):
        data_actor = gs.mumble_inst.users[data.actor]['name']
        split_data = data.message.strip().split(' ', 1)
        if len(split_data) != 2:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}move 'channel_name'")
            gs.gui_service.quick_gui(
                f"Incorrect format! Format: {rutils.get_command_token()}move 'channel_name'",
                text_type='header',
                box_align='left', user=gs.mumble_inst.users[data.actor]['name'],
                ignore_whisper=True)
            return
        channel_name = split_data[1]
        if channel_name == "default" or channel_name == "Default":
            channel_name = rutils.get_default_channel()
        channel_search = rutils.get_channel(channel_name)
        if channel_search is None:
            return
        channel_search.move_in()
        gs.gui_service.quick_gui(
            f"{rutils.get_bot_name()} was moved by {data_actor}",
            text_type='header', box_align='left', ignore_whisper=True)
        dprint(f"Moved to channel: {channel_name} by {data_actor}", origin=L_COMMAND)
        log(INFO, f"Moved to channel: {channel_name} by {data_actor}", origin=L_COMMAND)

    def cmd_makechannel(self, data):
        data_actor = gs.mumble_inst.users[data.actor]['name']
        split_data = data.message.strip().split(' ', 1)
        if len(split_data) != 2:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}makechannel 'channel_name'")
            gs.gui_service.quick_gui(
                f"Incorrect format! Format: {rutils.get_command_token()}makechannel 'channel_name'",
                text_type='header',
                box_align='left', user=gs.mumble_inst.users[data.actor]['name'],
                ignore_whisper=True)
            return
        channel_name = split_data[1]
        rutils.make_channel(rutils.get_my_channel(), channel_name)
        dprint(f"Made a channel: {channel_name} by {data_actor}", origin=L_COMMAND)
        log(INFO, f"Made a channel: {channel_name} by {data_actor}", origin=L_COMMAND)

    def cmd_leave(self, data):
        rutils.leave_channel()
        dprint(f"Returned to default channel.", origin=L_COMMAND)
        log(INFO, "Returned to default channel.", origin=L_COMMAND)

    def cmd_removechannel(self, data):
        rutils.remove_channel()
        dprint(f"Removed current channel.", origin=L_COMMAND)
        log(INFO, "Removed current channel.", origin=L_COMMAND)

    def cmd_joinme(self, data):
        data_actor = gs.mumble_inst.users[data.actor]
        gs.gui_service.quick_gui(f"Joining user: {data_actor['name']}", text_type='header',
                                 box_align='left', ignore_whisper=True)

        gs.mumble_inst.channels[data_actor['channel_id']].move_in()
        dprint(f"Joined user: {data_actor['name']}", origin=L_COMMAND)
        log(INFO, f"Joined user: {data_actor['name']}", origin=L_COMMAND)

    def cmd_joinuser(self, data):
        split_data = data.message.strip().split(' ', 1)
        if len(split_data) != 2:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}joinuser 'username'")
            gs.gui_service.quick_gui(
                f"Incorrect format! Format: {rutils.get_command_token()}joinuser 'username'",
                text_type='header',
                box_align='left', user=gs.mumble_inst.users[data.actor]['name'],
                ignore_whisper=True)
            return
        to_join = split_data[1]
        all_users = rutils.get_all_users()
        for user_id in rutils.get_all_users():
            if all_users[user_id]['name'] == to_join:
                gs.gui_service.quick_gui(f"Joining user: {all_users[user_id]['name']}", text_type='header',
                                         box_align='left', ignore_whisper=True)
                gs.mumble_inst.channels[all_users[user_id]['channel_id']].move_in()
                dprint(f"Joined user: {all_users[user_id]['name']}", origin=L_COMMAND)
                log(INFO, f"Joined user: {all_users[user_id]['name']}", origin=L_COMMAND)

    def cmd_cmdsearch(self, data):
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}cmdsearch 'command'")
            gs.gui_service.quick_gui(
                f"Incorrect format! Format: {rutils.get_command_token()}cmdsearch 'command'",
                text_type='header',
                box_align='left', user=gs.mumble_inst.users[data.actor]['name'],
                ignore_whisper=True)
            return
        search_query = all_data[1].strip()

        all_cmds = GetDB.get_all_commands(db_cursor=get_memory_db().cursor())
        if not all_cmds:
            gs.gui_service.quick_gui(
                "There was an error retrieving the commands from the database.",
                text_type='header',
                text_align='left',
                box_align='left'
            )
            return
        cmd_list = [f"{cmd_item[0]}" for cmd_item in all_cmds]
        file_ratios = process.extract(search_query, cmd_list)
        match_list = []
        for file_item in file_ratios:
            if file_item[1] > 80 and len(match_list) < 10:
                match_list.append(file_item[0])

        match_str = f"Search Results for <font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>{search_query}</font>: "
        if len(match_list) > 0:
            for i, clip in enumerate(match_list):
                match_str += f"<br><font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>[{i + 1}]</font> - {clip}"
        else:
            match_str += "None"
        gs.gui_service.quick_gui(
            match_str,
            text_type='header',
            text_align='left',
            box_align='left'
        )

    def cmd_showprivileges(self, data):
        gs.gui_service.quick_gui(f"{privileges.get_all_privileges()}", text_type='header', box_align='left',
                                 text_align='left', user=gs.mumble_inst.users[data.actor]['name'],
                                 ignore_whisper=True)
        log(INFO, f"Displayed user privileges to: {gs.mumble_inst.users[data.actor]['name']}", origin=L_COMMAND)

    def cmd_setprivileges(self, data):
        data_actor = gs.mumble_inst.users[data.actor]
        try:
            username = data.message.strip().split()[1]
            level = int(data.message.strip().split()[2])
            result = privileges.set_privileges(username, level, data_actor)
            if result:
                gs.gui_service.quick_gui(f"User: {username} privileges have been modified.", text_type='header',
                                         box_align='left', user=data_actor['name'],
                                         ignore_whisper=True)
                log(INFO, f"Modified user privileges for: {username}", origin=L_USER_PRIV)
        except IndexError:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}setprivileges 'username' 'level'")
            gs.gui_service.quick_gui(
                f"Incorrect format! Format: {rutils.get_command_token()}setprivileges 'username' 'level'",
                text_type='header',
                box_align='left', user=data_actor['name'],
                ignore_whisper=True)

    def cmd_addprivileges(self, data):
        data_actor = gs.mumble_inst.users[data.actor]
        try:
            username = data.message.strip().split()[1]
            level = int(data.message.strip().split()[2])
            result = privileges.add_to_privileges(username, level)
            if result:
                gs.gui_service.quick_gui(f"Added a new user: {username} to the user privileges.",
                                         text_type='header',
                                         box_align='left',
                                         user=data_actor['name'],
                                         ignore_whisper=True)
                log(INFO, f"Added a new user: {username} to the user privileges.", origin=L_USER_PRIV)
        except IndexError:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}addprivileges 'username' 'level'")
            gs.gui_service.quick_gui(
                f"Incorrect format! Format: {rutils.get_command_token()}addprivileges 'username' 'level'",
                text_type='header',
                box_align='left',
                user=data_actor['name'],
                ignore_whisper=True)

    def cmd_showblacklist(self, data):
        gs.gui_service.quick_gui(privileges.get_blacklist(), text_type='header',
                                 box_align='left',
                                 text_align='left',
                                 user=gs.mumble_inst.users[data.actor]['name'],
                                 ignore_whisper=True
                                 )

    def cmd_blacklistuser(self, data):
        try:
            all_data = data.message.strip().split(' ', 2)
            reason = "No reason provided."
            if len(all_data) > 2:
                reason = all_data[2]
            result = privileges.add_to_blacklist(all_data[1])
            if result:
                gs.gui_service.quick_gui(f"User: {all_data[1]} added to the blacklist.<br>Reason: {reason}",
                                         text_type='header',
                                         box_align='left',
                                         text_align='left',
                                         user=gs.mumble_inst.users[data.actor]['name'],
                                         ignore_whisper=True
                                         )
                log(INFO, f"Blacklisted user: {all_data[1]} <br>Reason: {reason}", origin=L_USER_PRIV)
        except IndexError:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}blacklistuser 'username'")
            gs.gui_service.quick_gui(f"Incorrect format! Format: {rutils.get_command_token()}blacklistuser 'username'",
                                     text_type='header',
                                     box_align='left',
                                     user=gs.mumble_inst.users[data.actor]['name'],
                                     ignore_whisper=True)

    def cmd_whitelistuser(self, data):
        try:
            all_data = data.message.strip().split(' ', 1)
            result = privileges.remove_from_blacklist(all_data[1])
            if result:
                gs.gui_service.quick_gui(f"User: {all_data[1]} removed from the blacklist.",
                                         text_type='header',
                                         box_align='left',
                                         user=gs.mumble_inst.users[data.actor]['name'],
                                         ignore_whisper=True
                                         )
                log(INFO, f"User: {all_data[1]} removed from the blacklist.", origin=L_USER_PRIV)
        except IndexError:
            gs.gui_service.quick_gui(f"Incorrect format! Format: {rutils.get_command_token()}whitelistuser 'username'",
                                     text_type='header',
                                     box_align='left',
                                     user=gs.mumble_inst.users[data.actor]['name'],
                                     ignore_whisper=True
                                     )
