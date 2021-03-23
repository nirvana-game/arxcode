"""
Base settings that we'll inherit from
"""
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# CHANGES: replace ADDITIONAL ANSI MAPPINGS WITH the following:
from evennia.contrib import color_markups

COLOR_ANSI_EXTRA_MAP = (
    color_markups.CURLY_COLOR_ANSI_EXTRA_MAP + color_markups.MUX_COLOR_ANSI_EXTRA_MAP
)
COLOR_XTERM256_EXTRA_FG = (
    color_markups.CURLY_COLOR_XTERM256_EXTRA_FG
    + color_markups.MUX_COLOR_XTERM256_EXTRA_FG
)
COLOR_XTERM256_EXTRA_BG = (
    color_markups.CURLY_COLOR_XTERM256_EXTRA_BG
    + color_markups.MUX_COLOR_XTERM256_EXTRA_BG
)
COLOR_XTERM256_EXTRA_GFG = (
    color_markups.CURLY_COLOR_XTERM256_EXTRA_GFG
    + color_markups.MUX_COLOR_XTERM256_EXTRA_GFG
)
COLOR_XTERM256_EXTRA_GBG = (
    color_markups.CURLY_COLOR_XTERM256_EXTRA_GBG
    + color_markups.MUX_COLOR_XTERM256_EXTRA_GBG
)
COLOR_ANSI_BRIGHT_BG_EXTRA_MAP = (
    color_markups.CURLY_COLOR_ANSI_XTERM256_BRIGHT_BG_EXTRA_MAP
    + color_markups.MUX_COLOR_ANSI_XTERM256_BRIGHT_BG_EXTRA_MAP
)
PERMISSION_HIERARCHY = [
    "Guest",  # note-only used if GUEST_ENABLED=True
    "Player",
    "Helper",
    "Builders",
    "Builder",
    "Wizards",
    "Wizard",
    "Admin",
    "Immortals",
    "Immortal",
    "Developer",
]
CHANNEL_COMMAND_CLASS = "commands.base_commands.channels.ArxChannelCommand"
BASE_ROOM_TYPECLASS = "typeclasses.rooms.ArxRoom"
BASE_SCRIPT_TYPECLASS = "typeclasses.scripts.scripts.Script"
BASE_GUEST_TYPECLASS = "typeclasses.guest.Guest"
VERBOSE_GAME_NAME = "Nirvana: Happy Place"
MULTISESSION_MODE = 1
COMMAND_DEFAULT_MSG_ALL_SESSIONS = True
ADDITIONAL_ANSI_MAPPINGS = [
    (r"%r", "\r\n"),
]
COMMAND_DEFAULT_ARG_REGEX = r"^[ /]+.*$|$"
LOCKWARNING_LOG_FILE = ""
DEFAULT_CHANNELS = [
    {
        "key": "Public",
        "aliases": "pub",
        "desc": "Public discussion",
        "locks": "control: perm(Wizards);listen:all();send:all()",
    },
    {
        "key": "MUinfo",
        "aliases": "",
        "desc": "Connection log",
        "locks": "control:perm(Immortals);listen:perm(Wizards);send:false()",
    },
    {
        "key": "Guest",
        "aliases": "",
        "desc": "Guest channel",
        "locks": "control:perm(Immortals);listen:all();send:all()",
    },
    {
        "key": "Staff",
        "aliases": "",
        "desc": "Staff channel",
        "locks": "control:perm(Immortals);listen:perm(Builder);send:perm(Builder)",
    },
    {
        "key": "StaffInfo",
        "aliases": "",
        "desc": "Messages for staff",
        "locks": "control:perm(Immortals);listen:perm(Builder);send:perm(Builder)",
    },
    {
        "key": "Helper",
        "aliases": "",
        "desc": "Channel for player volunteers",
        "locks": "control:perm(Immortals);listen:perm(helper);send:perm(helper)",
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "nirvana",
        "USER": "nirvanadb",
        "PASSWORD": "Nirsun123!@#",
        "HOST": "localhost",
        "PORT": "",
    }
}

TEMPLATES[0]["OPTIONS"]["context_processors"] += [
    "web.character.context_processors.consts"
]
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

# Global and Evennia-specific apps. This ties everything together so we can
# refer to app models and perform DB syncs.
INSTALLED_APPS += (
    "world.dominion",
    "world.msgs",
    "world.conditions.apps.ConditionsConfig",
    "world.fashion.apps.FashionConfig",
    "world.petitions.apps.PetitionsConfig",
    "web.character",
    "web.news",
    "web.helpdesk",
    "web.help_topics",
    "cloudinary",
    "django.contrib.humanize",
    "bootstrapform",
    "crispy_forms",
    "world.weather",
    "world.templates.apps.TemplateConfig",
    "world.exploration",
    "web.admintools",
    "world.magic",
    "world.quests.apps.QuestsConfig",
    "world.stat_checks.apps.StatChecksConfig",
    "world.prayer.apps.PrayerConfig",
    "world.traits.apps.TraitsConfig",
    "evennia_extensions.object_extensions.apps.ObjectExtensionsConfig",
    "world.game_constants.apps.GameConstantsConfig",
)

CRISPY_TEMPLATE_PACK = "bootstrap3"
DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000

######################################################################
# Game Time setup
######################################################################

######################################################################
# Magic setup
######################################################################
MAGIC_CONDITION_MODULES = ("world.magic.conditionals",)

######################################################################
# Helpdesk settings
######################################################################
# Queue.id for our Requests. Should normally be 1, but can be changed if you move queues around
REQUEST_QUEUE_SLUG = "Request"
BUG_QUEUE_SLUG = "Bugs"

######################################################################
# Dominion settings
######################################################################
BATTLE_LOG = os.path.join(LOG_DIR, "battle.log")
DOMINION_LOG = os.path.join(LOG_DIR, "dominion.log")
LOG_FORMAT = "%(asctime)s: %(message)s"
DATE_FORMAT = "%m/%d/%Y %I:%M:%S"

import cloudinary

cloudinary.config(
    cloud_name="CLOUDINARY_NAME",
    api_key="CLOUDINARY_API_KEY",
    api_secret="CLOUDINARY_API_SECRET",
)

# Evennia's base settings screw up current account creation
AUTH_PASSWORD_VALIDATORS = []
MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",  # 1.4?
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "web.middleware.auth.SharedLoginMiddleware",
]
