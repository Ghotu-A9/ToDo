import datetime
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


class ProgressUtility:
    def __init__(self, app):
        self.App = app
        self.canProgress = True

        print("Initialized Todo Progress Events")

    def setTodoProgress(self, todo, value):
        todo.todoProgress.set_fraction(value / 100)
        todo.progressLabel.set_text(str(round(value, 2)) + "%")

    def advanceProgress(self, initial, given, comp, lastTime, i, data):
        if self.canProgress:
            timeElapse = ((datetime.datetime.now() - lastTime).total_seconds()) / 60
            comp.relativeProgress = (timeElapse / given) * 100
            progress = comp.absoluteProgress + (timeElapse / given) * 100

            comp.progressThread = GLib.timeout_add(1, self.advanceProgress, initial + timeElapse, given, comp,
                                                   lastTime, i, data)
            self.setTodoProgress(comp, progress)
            if progress >= 100:
                GLib.source_remove(comp.progressThread)
                comp.progressThread = None
                self.setTodoProgress(comp, 100)
                self.todoProgressCompleted(comp, i, data)

    def todoProgressCompleted(self, comp, i, data):

        data1 = self.App.PlayPauseTUtility.changeComponentIconsAndState("complete", comp, i, data)
        nearestTodo = self.App.Operation.findNearestPausedTodo(i)

        if nearestTodo is not None:
            data2 = self.App.PlayPauseTUtility.changeComponentIconsAndState("play", self.App.TodoList[nearestTodo], nearestTodo, data1)
            self.App.Store.localWrite(data2)
        else:
            self.App.Store.localWrite(data1)

