import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


class OperationUtility:
    def __init__(self, app):
        self.App = app

    def findNearestPausedTodo(self, i):
        nearestTodo = 1
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
                nearestTodo = (i - nearestPositive)
            else:
                nearestTodo = None
        else:
            if (i + nearestNegative) < (len(self.App.TodoList)):
                if self.App.TodoList[i + nearestNegative].state != "Completed":
                    nearestTodo = (i + nearestPositive)
                else:
                    nearestTodo = None
            else:
                nearestTodo = None

        return nearestTodo

