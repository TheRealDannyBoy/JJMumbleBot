from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils.runtime_utils import get_command_token
from JJMumbleBot.lib.resources.strings import *
import os
import random


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from json import loads
        self.plugin_name = os.path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def cmd_coinflip(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = "Heads" if random.randint(1, 2) == 1 else "Tails"
        GS.gui_service.quick_gui(
            f"<font color='cyan'>Coin Flip Result:</font> <font color='yellow'>{result}</font>",
            text_type='header', box_align='left')

    def cmd_d4roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 4)
        GS.gui_service.quick_gui(f"<font color='cyan'>D4 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d6roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 6)
        GS.gui_service.quick_gui(f"<font color='cyan'>D6 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d8roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 8)
        GS.gui_service.quick_gui(f"<font color='cyan'>D8 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d10roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 10)
        GS.gui_service.quick_gui(f"<font color='cyan'>D10 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d12roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 12)
        GS.gui_service.quick_gui(f"<font color='cyan'>D12 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d16roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 16)
        GS.gui_service.quick_gui(f"<font color='cyan'>D16 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d20roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 20)
        GS.gui_service.quick_gui(f"<font color='cyan'>D20 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_customroll(self, data):
        all_data = data.message.strip().split()
        try:
            number_of_dice = int(all_data[1])
            number_of_faces = int(all_data[2])
            if number_of_dice > 20:
                GS.gui_service.quick_gui("Too many dice! Dice Limit: 20",
                                         text_type='header', box_align='left')
                return
            ret_text = "<br><font color='red'>Custom Dice Roll:</font>"
            for i in range(number_of_dice):
                random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
                result = random.randint(1, number_of_faces)
                ret_text += f"<br><font color='cyan'>[Dice {i}]-</font> <font color='yellow'>Rolled {result}</font>"
            GS.gui_service.quick_gui(ret_text, text_type='header', box_align='left')
            return
        except IndexError:
            GS.gui_service.quick_gui(f"Incorrect parameters! Format: {get_command_token()}customroll 'number_of_dice' 'dice_faces'",
                                     text_type='header', box_align='left')
            return
