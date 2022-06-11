import gi
import TodoTComp

from input_Utility import InputUtility
from store_TUtility import StoreUtility
from Initial_setup_TUtility import InitialSetupUtility
from add_remove_TUtility import AddRemoveUtility
from event_Utility import EventUtility
from play_pause_TUtility import PlayPauseUtility
from progress_TUtility import ProgressUtility

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

# the rewind button is not set the progress is not in store ie not storing


#  ! now solved (because of todoProgressCompleted function in (progress_TUtility.py) -> double writing the database,
#  don`t use the playpauseTodo function for other functionality)

builder = Gtk.Builder()
builder.add_from_file("../assets/glade/Todo_Glade.glade")

screen = Gdk.Screen.get_default()
cprovider = Gtk.CssProvider()
cprovider.load_from_path("../assets/css/main.css")
Gtk.StyleContext.add_provider_for_screen(screen, cprovider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


def getActiveRadio(radio):
    active = None
    for rad in radio.get_group():
        if rad.get_active():
            active = rad
    return active


class App:

    def __init__(self):
        self.Builder = builder
        self.TodoTCompClass = TodoTComp
        self.Window = self.Builder.get_object("MainWindow")

        self.TodoList = []

        self.Store = StoreUtility()
        self.Input = InputUtility(self)

        self.AddRemoveTUtility = AddRemoveUtility(self)
        self.PlayPauseTUtility = PlayPauseUtility(self)
        self.ProgressTUtility = ProgressUtility(self)

        self.Events = EventUtility(self)

        self.InitialSetup = InitialSetupUtility(self)

        self.Window.connect("destroy", Gtk.main_quit)
        self.Window.show_all()


App()
Gtk.main()
