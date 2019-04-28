import configparser
import time
import datetime


class GlobalMods:
    # JJMumbleBot Version
    version = "v2.0.1"
    # Mumble instance
    mumble = None
    # Config Access
    cfg = configparser.ConfigParser()
    # PGUI System Access
    gui = None
    # Logger Access
    logger = None
    # Global Mute Access
    muted = True
    # System Arguments Access
    debug_mode = False
    safe_mode = False
    verbose_mode = False
    quiet_mode = False
    # Up-time Tracker
    start_seconds = None
    seconds = 0
    minutes = 0
    hours = 0
    days = 0


def debug_print(msg):
    if GlobalMods.verbose_mode and not GlobalMods.quiet_mode:
        print(msg)


def reg_print(msg):
    if not GlobalMods.quiet_mode:
        print(msg)


def check_time():
    GlobalMods.seconds = time.time() - GlobalMods.start_seconds
    return f"Up-time: {str(datetime.timedelta(seconds=GlobalMods.seconds)).split('.')[0]}"
