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

        data1 = self.App.PlayPauseTUtility.changeComponentIconsAndState("complete", comp, i, data);
        data2 = self.App.PlayPauseTUtility.changeComponentIconsAndState("complete", comp, i, data);

        nearestPositive = 1
        nearestNegative = len(self.App.TodoList)
        negsign = False
        if len(self.App.TodoList) > 1:
            length = len(self.App.TodoList)
            for l in range(length):
                if self.App.TodoList[l].state == "Paused":
                    if (i - l) > 0:
                        nearestPositive = (i - l)
                        negsign = True
                        # print("upper", nearestPositive)
                    elif (i - l) < 0:
                        nearestNegative = (l - i)
                        # print("lower",nearestNegative)
                        negsign = False
                        break

        if negsign:
            if self.App.TodoList[i - nearestPositive].state != "Completed":
                data2 = self.App.PlayPauseTUtility.changeComponentIconsAndState("play",
                                                                                self.App.TodoList[i - nearestPositive],
                                                                                (i - nearestPositive), data1)
                self.App.Store.localWrite(data2)
        else:
            if (i + nearestNegative) < (len(self.App.TodoList)):
                if self.App.TodoList[i + nearestNegative].state != "Completed":
                    data2 = self.App.PlayPauseTUtility.changeComponentIconsAndState("play", self.App.TodoList[
                        i + nearestPositive], (i + nearestPositive), data1)
                    self.App.Store.localWrite(data2)

        self.App.Store.localWrite(data2)