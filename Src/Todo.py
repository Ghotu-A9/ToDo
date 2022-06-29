import gi
import TodoTComp

from input_Utility import InputUtility
from store_TUtility import StoreUtility
from Initial_setup_TUtility import InitialSetupUtility
from add_remove_TUtility import AddRemoveUtility
from event_Utility import EventUtility
from play_pause_TUtility import PlayPauseUtility
from progress_TUtility import ProgressUtility
from operation_TUtility import OperationUtility
from voice_Utility import VoiceUtility

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

builder = Gtk.Builder()
builder.add_from_file("../assets/glade/Todo_Glade.glade")

screen = Gdk.Screen.get_default()
cprovider = Gtk.CssProvider()

settings = Gtk.Settings.get_default()



if settings.get_property("gtk-application-prefer-dark-theme"):
    cprovider.load_from_path("../assets/css/main_dark.css")
else:
    settings.set_property("gtk-theme-name", "light")
    cprovider.load_from_path("../assets/css/main_light.css")

Gtk.StyleContext.add_provider_for_screen(screen, cprovider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

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

        self.Store = StoreUtility()
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


App()
Gtk.main()
