# Note that since qtile configs are just python scripts, you can check for
# syntax and runtime errors by just running this file as is from the command
# line, e.g.:
#
#    python config.py

import logging
import logging.handlers
import os

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

# The screens variable contains information about what bars are drawn where on
# each screen. If you have multiple screens, you'll need to construct multiple
# Screen objects, each with whatever widgets you want.
#
# Below is a screen with a top bar that contains several basic qtile widgets.

config_dir = os.path.expanduser('~/.config/qtile')
battery_custom_icons = {
        "battery-full-charged": "icons/battery-full.png",
        "battery-full-charging": "icons/battery-full-charging.png",
        "battery-full": "icons/battery-full.png",
        "battery-good-charging": "icons/battery-good-charging.png",
        "battery-good": "icons/battery-good.png",
        "battery-caution-charging": "icons/battery-caution-charging.png",
        "battery-caution": "icons/battery-caution.png",
        "battery-low-charging": "icons/battery-low-charging.png",
        "battery-low": "icons/battery-low.png",
        "battery-empty": "icons/battery-empty.png",
        }
battery_custom_icons = {k: os.path.join(config_dir, v) for k, v in battery_custom_icons.items()}


default_screen_widgets = [
        widget.GroupBox(urgent_alert_method='text', fontsize=10, borderwidth=1),
        widget.Prompt(),
        widget.WindowName(foreground="a0a0a0"),
        widget.Notify(),
        widget.Volume(foreground="70ff70"),
        widget.Clock(
            foreground="a0a0a0",
            format='<small>%a</small> <b>%I:%M %p</b> <small>%Y.%m.%d</small>',
            markup=True,
            ),
        ]

primary_screen_widgets = [
        widget.GroupBox(urgent_alert_method='text', fontsize=10, borderwidth=1),
        widget.Prompt(),
        widget.WindowName(foreground="a0a0a0"),
        widget.Notify(),
        widget.Volume(foreground="70ff70"),
        widget.Clock(
            foreground="a0a0a0",
            format='<small>%a</small> <b>%I:%M %p</b> <small>%Y.%m.%d</small>',
            markup=True,
            ),
        ]

if os.path.exists('/proc/acpi/battery'):
    primary_screen_widgets.insert(1, widget.BatteryIcon(custom_icons=battery_custom_icons))

screens = [
        Screen(top=bar.Bar(primary_screen_widgets, size=22)),
        Screen(top=bar.Bar(default_screen_widgets, size=22)),
        ]

@hook.subscribe.client_new
def dialogs(window):
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True

@hook.subscribe.client_new
def idle_dialogues(window):
    if((window.window.get_name() == 'Search Dialog') or
	   (window.window.get_name() == 'Module') or
	   (window.window.get_name() == 'Goto') or
	   (window.window.get_name() == 'IDLE Preferences')):
        window.floating = True

@hook.subscribe.client_new
def libreoffice_dialogues(window):
    if((window.window.get_wm_class() == ('VCLSalFrame', 'libreoffice-calc')) or
            (window.window.get_wm_class() == ('VCLSalFrame', 'LibreOffice 3.4'))):
        window.floating = True

@hook.subscribe.client_new
def inkscape_dialogues(window):
    if(window.window.get_name() in ('Sozi', 'Create new database')):
        window.floating = True

@hook.subscribe.client_new
def pinetry_dialogue(window):
    if(window.window.get_name() == 'pinentry'):
        window.floating = True

# Super_L (the Windows key) is typically bound to mod4 by default, so we use
# that here.
mod = "mod4"
alt = "mod1"

# The keys variable contains a list of all of the keybindings that qtile will
# look through each time there is a key pressed.
keys = [
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod, "shift"],  "r", lazy.restart()),
    Key([mod], "c", lazy.window.kill()),
    Key([mod, "shift"], "m", lazy.group.setlayout('max')),
    Key([mod], "s", lazy.group.setlayout('stack')),
    Key([mod], "n", lazy.group.setlayout('xmonad-tall')),
    Key([mod], "x", lazy.group.setlayout('xmonad-tall')),

    Key([mod], "Tab", lazy.next_screen()),
    Key([mod, "shift"], "Tab",
        lazy.group.prev_window(),
        lazy.window.disable_floating()),

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod, alt], "j", lazy.window.opacity(0.5)),
    Key([mod, alt], "k", lazy.window.opacity(1.0)),
    Key([mod], "h",
        lazy.layout.previous(), # Stack
        lazy.layout.left()),    # xmonad-tall
    Key([mod], "l",
        lazy.layout.next(),     # Stack
        lazy.layout.right()),   # xmonad-tall
    Key([mod], "k",
        lazy.layout.up()),
    Key([mod], "j",
        lazy.layout.down()),

    # These are unique to stack layout
    Key([mod, "shift"], "l",
        lazy.layout.client_to_next(), # Stack
        lazy.layout.swap_right()),    # xmonad-tall
    Key([mod, "shift"], "h",
        lazy.layout.client_to_previous(), # Stack
        lazy.layout.swap_left()),    # xmonad-tall
    Key([mod, "shift"], "Return",
        lazy.layout.toggle_split()),

    # Multiple function keys
    Key([mod, "shift"], "space",
        lazy.layout.rotate(),
        lazy.layout.flip()),              # xmonad-tall
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up()),       # Stack, xmonad-tall
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down()),         # Stack, xmonad-tall
    Key([mod], "m",
        lazy.layout.toggle_maximize()), # Stack
    Key([mod, "control"], "m",
        lazy.layout.maximize()),            # xmonad-tall
    Key([mod, "control"], "n",
        lazy.layout.normalize()),            # xmonad-tall
    Key([mod, "control"], "l",
        lazy.layout.delete(),                # Stack
        lazy.layout.increase_ratio(),     # Tile
        lazy.layout.grow()),            # xmonad-tall
    Key([mod, "control"], "h",
        lazy.layout.add(),             # Stack
        lazy.layout.decrease_ratio(),     # Tile
        lazy.layout.shrink()),         # xmonad-tall
    Key([mod, "control"], "k",
        lazy.layout.grow(),             # xmonad-tall
        lazy.layout.decrease_nmaster()),    # Tile
    Key([mod, "control"], "j",
        lazy.layout.shrink(),               # xmonad-tall
        lazy.layout.increase_nmaster()),   # Tile

    # interact with prompts
    Key([mod], "r",              lazy.spawncmd()),
    Key([mod], "g",              lazy.switchgroup()),

    # start specific apps
    Key([mod], "b",              lazy.spawn("firefox")),
    Key([mod], "e",              lazy.spawn("evince")),
    Key([mod], "Return",         lazy.spawn("urxvt")),
    Key([mod], "F12",            lazy.spawn("xscreensaver-command -lock")),
]

# This allows you to drag windows around with the mouse if you want.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
groups = []
labels = [str(n) for n in range(1, 10)]
for label in labels:
    groups.append(Group(label))
    keys.append(Key([mod], label, lazy.group[label].toscreen()))
    keys.append(Key([mod, "shift"], label, lazy.window.togroup(label)))

layouts = [
    layout.MonadTall(border_width=1),
    layout.Max(),
]

main = None
follow_mouse_focus = True

# start the applications at Qtile startup
@hook.subscribe.startup
def startup():
    logger = logging.getLogger('qtile.config')
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.handlers.RotatingFileHandler(
        filename=os.path.join(os.path.expanduser('~'), '.config/qtile/qtile.log'),
        maxBytes=100000,
        backupCount=10,
        ))


@hook.subscribe.current_screen_change
def current_screen_change():
    logger = logging.getLogger('qtile.config')

    try:
        root = screens[0].qtile
        current_window = root.currentGroup.currentWindow

        for group in root.groups:
            group_window = group.currentWindow
            if group_window is not None and group_window is not current_window:
                group_window.bordercolor = 0x808080
                group_window.window.set_attribute(borderpixel=group_window.bordercolor)


    except Exception as e:
        logger.exception(e)
