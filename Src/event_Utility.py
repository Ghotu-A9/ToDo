import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gio


class EventUtility:

    def __init__(self, app):
        self.App = app
        self.setTUtilityEvents()

        print("Initialized Todo Control Events")

    def setTUtilityEvents(self):
        self.App.newTodoButton.connect("clicked", self.App.AddRemoveTUtility.wantsToCreateTodo)

    def addDefaultTodoHandlers(self, todoComp, index):
        todoComp.removeButton.connect("clicked", self.App.AddRemoveTUtility.removeTodoExcited, todoComp)
        todoComp.controlButton.connect("clicked", self.App.PlayPauseTUtility.playpauseTodo, todoComp, index)


