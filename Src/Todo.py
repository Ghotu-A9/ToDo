import datetime
import pprint

import gi
import TodoTComp

from input_Utility import InputUtility
from store_TUtility import StoreTUtility
from store_Utility import StoreUtility
from Initial_setup_TUtility import InitialSetupUtility
from add_remove_TUtility import AddRemoveUtility
from event_Utility import EventUtility
from play_pause_TUtility import PlayPauseUtility
from progress_TUtility import ProgressUtility
from operation_TUtility import OperationUtility
from voice_Utility import VoiceUtility

gi.require_version('Wnck', '3.0')
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, Wnck, Gio

builder = Gtk.Builder()
builder.add_from_file("../assets/glade/Todo_Glade.glade")

screen = Gdk.Screen.get_default()
cprovider = Gtk.CssProvider()
cprovider1 = Gtk.CssProvider()

settings = Gtk.Settings.get_default()

if settings.get_property("gtk-application-prefer-dark-theme"):

    cprovider.load_from_path("../assets/themes/chromeos_theme/ChromeOS-dark/gtk-3.0/gtk.css")
    cprovider1.load_from_path("../assets/css/main_dark.css")

else:
    cprovider.load_from_path("../assets/themes/chromeos_theme/ChromeOS-light/gtk-3.0/gtk.css")
    cprovider1.load_from_path("../assets/css/main_light.css")

Gtk.StyleContext.add_provider_for_screen(screen, cprovider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

Gtk.StyleContext.add_provider_for_screen(screen, cprovider1, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class App:

    def __init__(self):
        self.Builder = builder
        self.TodoTCompClass = TodoTComp
        self.Window = self.Builder.get_object("MainWindow")
        self.Stack = self.Builder.get_object("AppStackMain")
        self.TodoContainer = self.Builder.get_object("TodoContainer")
        self.newTodoButton = self.Builder.get_object("createNewTodo")
        self.discardTodoButton = self.Builder.get_object("discardNewTodo")

        self.TodoList = []
        self.ActiveWindow = {}
        self.LastActiveWindow = None
        self.ActiveTodoIndex = None
        self.LastActiveWindowOn = datetime.datetime.now()

        self.DBStore = StoreUtility()
        self.Store = StoreTUtility()
        self.Input = InputUtility(self)
        self.Voice = VoiceUtility(self)

        self.AddRemoveTUtility = AddRemoveUtility(self)
        self.PlayPauseTUtility = PlayPauseUtility(self)
        self.ProgressTUtility = ProgressUtility(self)
        self.Operation = OperationUtility(self)

        self.Events = EventUtility(self)

        self.InitialSetup = InitialSetupUtility(self)

        self.Window.connect("destroy", Gtk.main_quit)
        self.Window.show_all()

        self.Events.registerActiveWindowChangeEventDefault()


        # print(self.DBStore.saveLocalAnalyticalData(dictData))
        # print(self.DBStore.getAllLocalAnalyticalData())
        # print(self.DBStore.getSingleLocalAnalyticalData(2, "p_time"))
        # self.DBStore.updateLocalAnalyticalData(1, "programs", ["lollop1", "polloi000", "hkeys11"])
        # self.DBStore.removeSingleRowLocalAnalyticalData(2)



App()
Gtk.main()
