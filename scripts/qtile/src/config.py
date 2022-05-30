### MGD QTile Config v1 ###
# by Michael Davis

import os
import subprocess
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.widget import backlight

import metadata
from metadata import *

logger.warning('loading MGD Config...')

my = metadata.Struct()
# MY CONSTANTS
my.fonts = {
        'normal': MY.fonts['normal'],
        'bold': MY.fonts['bold'],
        'monospace': MY.fonts['monospace']
}
my.colors = MY.colors['distro']['data']
my.emojis = MY.emojis

# alt = mod1
mod = "mod4"


# CLASSES

@lazy.function
def activity_config (qtile):
    #qtile.cmd_simulate_keypress([mod], "4")
    logger.warning("%s -a %s/lxconfig/scripts/qtile/" % (MY.apps.editor, HOME_PATH))
    qtile.cmd_spawn([MY.apps.editor,'-n', "%s/lxconfig/scripts/qtile/" % HOME_PATH])
    qtile.cmd_spawn([MY.apps.terminal, "-e", 'tail -f %s/.local/share/qtile/qtile.log' % HOME_PATH])


# KEYS
kc = [mod]
modKeys = [
    Key(kc, "h", lazy.layout.left(), desc="Move focus to left"),
    Key(kc, "j", lazy.layout.down(), desc="Move focus down"),
    Key(kc, "l", lazy.layout.right(), desc="Move focus to right"),
    Key(kc, "k", lazy.layout.up(), desc="Move focus up"),

    Key(kc, "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key(kc, "Tab", lazy.layout.next(),
        desc="Move window focus to other window"),
    Key(kc, "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(kc, "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key(kc, "x", lazy.window.kill(), desc="Kill focused window"),    
    #KeyChord(kc, "w", [
    #    Key([], "c", activity_config())
    #        #lazy.group["4"].toscreen(), lazy.spawn("code"), lazy.spawn("firefox"))
    #],
    #mode="Activity"
    #),

    Key(kc, "Return", lazy.spawn(MY.apps.terminal),
        desc="Launch terminal [%s]" % MY.apps.terminal),
    Key(kc, "quoteright", lazy.spawn(MY.apps.browser),
        desc="Launch browser [%s]" % MY.apps.browser),
    Key(kc, "backslash", lazy.spawn(MY.apps.fileManager),
        desc="Launch file manager [%s]" % MY.apps.fileManager),
]

kc = [mod, "shift"]
modshiftKeys = [
    Key(kc, "h", lazy.layout.shuffle_left(), desc="Move window left"),
    Key(kc, "l", lazy.layout.shuffle_right(), desc="Move window right"),
    Key(kc, "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key(kc, "k", lazy.layout.shuffle_up(), desc="Move window up"),
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
    #Key([], "XF86MonBrightnessUp",
    #        lazy.widget['backlight'].change_backlight(backlight.ChangeDirection.UP)),
    #Key([], "XF86MonBrightnessDown", 
    #    lazy.widget['backlight'].change_backlight(backlight.ChangeDirection.DOWN))    
    Key([], "XF86MonBrightnessUp", lazy.spawn(f"brightnessctl -s set +{ BRIGHTNESS_STEP }")),
    Key([], "XF86MonBrightnessDown", lazy.spawn(f"brightnessctl -s set { BRIGHTNESS_STEP }-"))
]

# A list of available commands that can be bound to keys can be found
# at https://docs.qtile.org/en/latest/manual/config/lazy.html
keys = []
keys.extend(modKeys)
keys.extend(modshiftKeys)
keys.extend(modcontrolKeys)
keys.extend(blankKeys)

# Load the group control keys in
groups = [Group(i) for i in "qweiop"]
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
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=3, margin=3),
    layout.Max(margin=3),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    #layout.Matrix(),
    #layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]


### SCREENS & WIDGETS
widget_defaults = dict(
    font=MY.fonts['normal'],
    fontsize = 14,
    padding = 2,
    background=TASKBAR_BGCOLOR
)
extension_defaults = widget_defaults.copy()


# The left side of the taskbar
taskbarInfo = [
    SimpleSeperator(10),
    widget.Image(
        filename=ICONS_FOLDER + "/python-white.png",
        scale="False",
        #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm)}
    ),
    SimpleSeperator(10),
    widget.GroupBox(
        font="Ubuntu Bold",
        fmt=MY.emojis['bullet'],
        fontsize=15,
        margin_y=2,
        margin_x=0,
        padding_y=4,
        padding_x=4,
        borderwidth=3,
        active=MY.colors['lights'][1],
        inactive=MY.colors['purple'],
        rounded=False,
        highlight_color=MY.colors['darks'][3],
        highlight_method="line",
        this_current_screen_border=MY.colors['blue'],
        this_screen_border=MY.colors['yellow'],
        other_current_screen_border=MY.colors['blue'],
        other_screen_border=MY.colors['yellow'],
        #foreground=MY.colors['darks'][3],
        background=TASKBAR_BGCOLOR
    ),
    widget.TextBox(
        text='|',
        font=MY.fonts['monospace'],
        background=TASKBAR_BGCOLOR,
        foreground='474747',
        padding=2,
        fontsize=14
    ),
    widget.CurrentLayoutIcon(
        custom_icon_paths=[ICONS_FOLDER],
        foreground=MY.colors['lights'][1],
        background=TASKBAR_BGCOLOR,
        padding=0,
        scale=0.7
    ),
    widget.CurrentLayout(
        foreground=MY.colors['lights'][1],
        background=TASKBAR_BGCOLOR,
        padding=5
    ),
    widget.TextBox(
        text='|',
        font=MY.fonts['monospace'],
        background=TASKBAR_BGCOLOR,
        foreground='474747',
        padding=2,
        fontsize=14
    ),
    widget.Prompt(),
    widget.Chord(
        chords_colors={
                "launch": ("#ff0000", "#ffffff"),
                },
        name_transform=lambda name: name.upper(),
    ),
    widget.WindowName(
        foreground=MY.colors['blue'],
        background=TASKBAR_BGCOLOR,
        padding=0
    ),
    widget.Systray(
        background=TASKBAR_BGCOLOR,
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

colorSwitcher = switcher(TASKBAR_BGCOLOR, MY.colors['darks'][3])

# The right side of the taskbar
taskbarRight = [
    widget.Net(
        interface="wlan0",
        format='Net: {down} ↓↑ {up}',
        foreground=MY.colors['lights'][1],
        backgroun2d=next(colorSwitcher),
        padding=5
    ),
    widget.ThermalSensor(
        foreground=MY.colors['lights'][1],
        background=next(colorSwitcher),
        threshold=90,
        fmt='Temp: {}',
        padding=5
    ),
    #widget.Volume(update_interval=0.2, emoji=True),
    widget.CheckUpdates(
        update_interval=1800,
        font = MY.fonts['bold'],
        fontsize = 16,
        distro="Arch_checkupdates",
        display_format="%s {updates} " % MY.emojis['update'],
        foreground=MY.colors['lights'][1],
        colour_have_updates=MY.colors['lights'][1],
        colour_no_updates=MY.colors['lights'][1],
        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(MY.apps.terminal + " -e sudo pacman -Syu")},
        padding=5,
        background=next(colorSwitcher),
    ),
    widget.Memory(
        foreground=MY.colors['lights'][1],
        background=next(colorSwitcher),
        #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
        fmt='Mem: {}',
        padding=5,
        measure_mem = 'G',
    ),
    widget.Battery(
        format="{percent:2.0%}",
        background=next(colorSwitcher),        
    ),
    widget.Volume(
        font="Noto Sans Symbols",
        foreground=MY.colors['lights'][1],
        background=next(colorSwitcher),
        #fmt='{} %s' % my.emojis['volume-on'],
        emoji = True,
        padding=5
    ),
    #widget.KeyboardLayout(
    #    foreground=MY.colors['lights'][1],
    #    background=next(colorSwitcher),
    #    fmt='Keyboard: {}',
    #    padding=5
    #),
    widget.Clock(
        font=MY.fonts['bold'],
        foreground=MY.colors['lights'][1],
        background=next(colorSwitcher),
        format="%A, %B %d - %H:%M "
    )
]
taskbarRight = metadata.TaskbarStack (taskbarRight, my.emojis['triangle-left'], TASKBAR_BGCOLOR)

distroBar = bar.Bar(
    taskbarInfo + taskbarRight.stack(),
    opacity=0.7,
    size=22
)


screens = [
    Screen(
        top=distroBar,
        wallpaper=MY.wallpaper,
        wallpaper_mode='stretch',
    ),
    Screen(
        top=distroBar,
        wallpaper=MY.wallpaper,
        wallpaper_mode='stretch',
    ),
]


mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Click([mod, "shift"], "Button1", lazy.window.toggle_floating(), desc='Toggle floating'),

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


@hook.subscribe.startup_once
def autostart_once():
    pass

# MISCELLANEOUS SETTINGS
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
auto_minimize = True  # should apps be able to auto-minimize on blur?
wl_input_rules = None  # For Wayland - can be used to configure input devices


################################################################################


# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

