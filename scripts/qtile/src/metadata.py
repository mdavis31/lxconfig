import os, toml
from libqtile import widget
from libqtile.log_utils import logger

logger.warning('loading MGD Config (Metadata)...')
class Struct (object):
    def __init__(self):
        pass


### CONSTANT VALUES (MY is loaded below)
HOME_PATH =  os.path.expanduser('~')
QTILE_PATH = os.path.join (HOME_PATH, ".config/qtile")
ICONS_FOLDER = os.path.join (QTILE_PATH, "icons")
MY_TOML = toml.load(os.path.join (QTILE_PATH, "settings.toml"))

MY = Struct()
MY.wallpaper = MY_TOML.get('wallpaper', '')

MY.apps = Struct()
MY.apps.terminal =      MY_TOML.get('apps', {}).get ('terminal', 'xterm')
MY.apps.editor =        MY_TOML.get('apps', {}).get ('editor', 'vim')
MY.apps.fileManager =   MY_TOML.get('apps', {}).get ('fileManager', 'thunar')
MY.apps.browser =       MY_TOML.get('apps', {}).get ('browser', 'firefox')

MY.fonts = MY_TOML.get('fonts', {})
MY.colors = MY_TOML.get('colors', {})
MY.emojis = MY_TOML.get('emojis', {})

TASKBAR_BGCOLOR = MY.colors['darks'][2]
TASKBAR_EMOJI_FONT = "Ubuntu Mono"
BRIGHTNESS_STEP = 20

### CLASSES
# The stack of widgets to the right of the bar (i.e. the colorful blocks)
# Contains a seperator (emoji), and a bg_color (use same color as taskbar)
class TaskbarStack (object):
    def __init__ (self, widgets, emoji, bg_color):
        self.widgets = widgets
        self.emoji = emoji
        self.bg_color = bg_color

    def _createSeperator (self, index):
        background = self.widgets[index-1].background if index > 0 else self.bg_color
        foreground = self.widgets[index].background
        return widget.TextBox (
                text = self.emoji,
                font = TASKBAR_EMOJI_FONT,
                background = background,
                foreground = foreground,
                padding = -1,
                fontsize = 42
        )

    def stack (self):
        result = []
        for index, w in enumerate (self.widgets):
            result.append (self._createSeperator(index))
            result.append (w)
        return result

class SimpleSeperator (widget.Sep):
    def __init__ (self, padding, background=TASKBAR_BGCOLOR):
        super().__init__(
            linewidth=0,
            padding=padding,
            background=background
        )
