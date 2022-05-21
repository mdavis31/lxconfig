### MGD QTile Config v1 ###
# by Michael Davis

from cgi import test
from email.policy import default
import os
from re import L
import subprocess
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger
#from libqtile.utils import guess_terminal

logger.warning('loading MGD Config...')

class Struct (object):
    def __init__(self):
        pass


# MY CONSTANTS
my = Struct()
my.terminal = "alacritty"
my.fmanager = "thunar"
my.browser = "google-chrome-stable"
my.colors = [["#282c34", "#282c34"],
             ["#1c1f24", "#1c1f24"],
             ["#dfdfdf", "#dfdfdf"],
             ["#ff6c6b", "#ff6c6b"],
             ["#98be65", "#98be65"],
             ["#da8548", "#da8548"],
             ["#51afef", "#51afef"],
             ["#c678dd", "#c678dd"],
             ["#46d9ff", "#46d9ff"],
             ["#a9a1e1", "#a9a1e1"]]

mod = "mod1"


# CLASSES
# The stack of widgets to the right of the taskbar (i.e. the colorful blocks)
class TaskbarStack (object):
    emoji = '\u25E2'

    def __init__ (self, widgList):
        self.widgList = widgList

    def _createSeperator (self, index):
        background = self.widgList[index-1].background if index > 0 else my.colors[0]
        foreground = self.widgList[index].background
        return widget.TextBox (
                text = self.emoji,
                font = "Ubuntu Mono",
                background = background,
                foreground = foreground,
                padding = -1,
                fontsize = 42
        )

    def stack (self):
        result = []
        for index, w in enumerate (self.widgList):
            result.append (self._createSeperator(index))
            result.append (w)
        return result

class SimpleSeperator (widget.Sep):
    def __init__ (self, padding, background=my.colors[1]):
        super().__init__(
            linewidth=0,
            padding=padding,
            foreground=my.colors[2],
            background=background
        )

# KEYS
kc = [mod]
modKeys = [
    Key(kc, "h", lazy.layout.left(), desc="Move focus to left"),
    Key(kc, "j", lazy.layout.down(), desc="Move focus down"),
    Key(kc, "l", lazy.layout.right(), desc="Move focus to right"),
    Key(kc, "k", lazy.layout.up(), desc="Move focus up"),

    Key(kc, "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key(kc, "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    Key(kc, "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(kc, "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    Key(kc, "Return", lazy.spawn(my.terminal),
        desc="Launch terminal [%s]" % my.terminal),
    Key(kc, "quoteright", lazy.spawn(my.browser),
        desc="Launch browser [%s]" % my.browser),
    Key(kc, "backslash", lazy.spawn(my.fmanager),
        desc="Launch file manager [%s]" % my.fmanager),
]

kc = [mod, "shift"]
modshiftKeys = [
    Key(kc, "h", lazy.layout.shuffle_left(), desc="Move window left"),
    Key(kc, "l", lazy.layout.shuffle_right(), desc="Move window right"),
    Key(kc, "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key(kc, "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key(kc, "q", lazy.window.kill(), desc="Kill focused window"),
]

kc = [mod, "control"]
modcontrolKeys = [
    Key(kc, "h", lazy.layout.grow_left(), desc="Grow window left"),
    Key(kc, "l", lazy.layout.grow_right(), desc="Grow window right"),
    Key(kc, "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key(kc, "k", lazy.layout.grow_up(), desc="Grow window up"),

    Key(kc, "r", lazy.reload_config(), desc="Reload the config"),
    Key(kc, "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

mixer_cmd = "amixer -c 0 -q set"
blankKeys = [
    Key([], "XF86AudioRaiseVolume", lazy.spawn(mixer_cmd + " Master 2dB+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(mixer_cmd + " Master 2dB-")),
    Key([], "XF86AudioMute", lazy.spawn(mixer_cmd + " Master toggle")),
]

# A list of available commands that can be bound to keys can be found
# at https://docs.qtile.org/en/latest/manual/config/lazy.html
keys = []
keys.extend(modKeys)
keys.extend(modshiftKeys)
keys.extend(modcontrolKeys)
keys.extend(blankKeys)

# Load the group control keys in
groups = [Group(i) for i in "1234uiop"]
for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #        desc="Move focused window to group {}".format(i.name)),
    ])

# LAYOUTS
layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

# COLORS

### SCREENS & WIDGETS
myWidgetDefaults = dict(
    font="sans",
    fontsize=14,
    padding=3,
)
distroWidgetDefaults = dict(
    font="Noto Sans",
    fontsize=10,
    padding=2,
    background=my.colors[2]
)
extension_defaults = distroWidgetDefaults.copy()

myBar = bar.Bar([
    widget.CurrentLayout(),
    widget.GroupBox(),
    widget.Prompt(),
    widget.WindowName(),
    widget.Chord(
        chords_colors={
                "launch": ("#ff0000", "#ffffff"),
                },
        name_transform=lambda name: name.upper(),
    ),
    widget.TextBox("mike\'s config", name="default"),
    widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
    widget.Systray(),
    widget.Net(interface="wlan0"),
    widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
    widget.QuickExit(),
    ],
    28,
    border_width=[0, 0, 2, 0],  # Draw top and bottom borders
    border_color=["ff00ff", "000000", "000000",
                  "000000"]  # Borders are magenta
)


# The left side of the taskbar
taskbarInfo = [
    SimpleSeperator(10),
    widget.Image(
        filename="~/.config/qtile/icons/python-white.png",
        scale="False",
        #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm)}
    ),
    SimpleSeperator(10),
    widget.GroupBox(
        font="Ubuntu Bold",
        fontsize=15,
        margin_y=2,
        margin_x=0,
        padding_y=4,
        padding_x=4,
        borderwidth=3,
        active=my.colors[2],
        inactive=my.colors[7],
        rounded=False,
        highlight_color=my.colors[1],
        highlight_method="line",
        this_current_screen_border=my.colors[6],
        this_screen_border=my.colors[4],
        other_current_screen_border=my.colors[6],
        other_screen_border=my.colors[4],
        foreground=my.colors[2],
        background=my.colors[0]
    ),
    widget.TextBox(
        text='|',
        font="Ubuntu Mono",
        background=my.colors[0],
        foreground='474747',
        padding=2,
        fontsize=14
    ),
    widget.CurrentLayoutIcon(
        custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
        foreground=my.colors[2],
        background=my.colors[0],
        padding=0,
        scale=0.7
    ),
    widget.CurrentLayout(
        foreground=my.colors[2],
        background=my.colors[0],
        padding=5
    ),
    widget.TextBox(
        text='|',
        font="Ubuntu Mono",
        background=my.colors[0],
        foreground='474747',
        padding=2,
        fontsize=14
    ),
    widget.Prompt(),
    widget.WindowName(
        foreground=my.colors[6],
        background=my.colors[0],
        padding=0
    ),
    widget.Systray(
        background=my.colors[0],
        padding=5
    ),
    SimpleSeperator(6),
]

def switcher (arg1, arg2):
    switch = False
    while True:
        if switch:
            yield arg1 
        else:
            yield arg2 
        switch = not switch

colorSwitcher = switcher(my.colors[6], my.colors[9])

# The right side of the taskbar
taskbarStack = TaskbarStack ([
    widget.Net(
        interface="wlan0",
        format='Net: {down} ↓↑ {up}',
        foreground=my.colors[1],
        background=next(colorSwitcher),
        padding=5
    ),
    widget.ThermalSensor(
        foreground=my.colors[1],
        background=next(colorSwitcher),
        threshold=90,
        fmt='Temp: {}',
        padding=5
    ),
    widget.CheckUpdates(
        update_interval=1800,
        distro="Arch_checkupdates",
        display_format="Updates: {updates} ",
        foreground=my.colors[1],
        colour_have_updates=my.colors[1],
        colour_no_updates=my.colors[1],
        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(my.terminal + " -e sudo pacman -Syu")},
        padding=5,
        background=my.colors[6]
    ),
    widget.Memory(
        foreground=my.colors[1],
        background=my.colors[9],
        #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
        fmt='Mem: {}',
        padding=5
    ),
    widget.Volume(
        foreground=my.colors[1],
        background=my.colors[6],
        fmt='Vol: {}',
        padding=5
    ),
    #widget.KeyboardLayout(
    #    foreground=my.colors[1],
    #    background=my.colors[6],
    #    fmt='Keyboard: {}',
    #    padding=5
    #),
    widget.Clock(
        foreground=my.colors[1],
        background=my.colors[9],
        format="%A, %B %d - %H:%M "
    )
])

distroBar = bar.Bar(
    taskbarInfo + taskbarStack.stack(),
    opacity=1.0,
    size=22
)


screens = [
    Screen(
        top=distroBar,
        wallpaper='~/lxconfig/wallpapers/ReflectBlack-Arch.png',
        wallpaper_mode='stretch'
    ),
]


mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)


@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])


# MISCELLANEOUS SETTINGS
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True  # should apps be able to auto-minimize on blur?
wl_input_rules = None  # For Wayland - can be used to configure input devices


################################################################################


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
