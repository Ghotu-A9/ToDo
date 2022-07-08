import gi

gi.require_version('Wnck', '3.0')
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gio, Wnck


class EventUtility:

    def __init__(self, app):
        self.App = app
        self.setTUtilityEvents()
        self.screen = Wnck.Screen.get_default()
        print("Initialized Todo Control Events")

    def setTUtilityEvents(self):
        self.App.newTodoButton.connect("clicked", self.App.AddRemoveTUtility.wantsToCreateTodo)

    def addDefaultTodoHandlers(self, todoComp, index):
        todoComp.removeButton.connect("clicked", self.App.AddRemoveTUtility.removeTodoExcited, todoComp)
        todoComp.controlButton.connect("clicked", self.App.PlayPauseTUtility.playpauseTodo, todoComp, index)

    def registerActiveWindowChangeEvent(self):
        def saveWindowStatus(screen,window):
            if screen.get_active_window():
                #print(screen.get_active_window().get_icon().savev("lol1","png"))
                program = (screen.get_active_window().get_name()).split()
                name = screen.get_active_window().get_name()
                icon = screen.get_active_window().get_icon()
                self.App.ActiveWindow={"program":program[len(program)-1],"name":name,"icon":icon}

        self.screen.connect("active-window-changed",saveWindowStatus)


