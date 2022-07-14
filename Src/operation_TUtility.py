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
        checkForAllCompleted = True

        if len(self.App.TodoList) > 1:
            length = len(self.App.TodoList)
            for l in range(length):
                if self.App.TodoList[l].state == "Paused" or self.App.TodoList[l].state == "Created":
                    checkForAllCompleted = False
                    if (i - l) > 0:
                        nearestPositive = (i - l)
                        negsign = True
                        # print("upper", nearestPositive)
                    elif (i - l) < 0:
                        nearestNegative = min(nearestNegative, (l - i))
                        # print("lower",nearestNegative)
                        negsign = False
                    else:
                        nearestTodo = None
        else:
            nearestTodo = None

        # print("upper", nearestPositive)
        # print("lower",nearestNegative)
        # print("///////////////")

        if negsign and not checkForAllCompleted:
            nearestTodo = (i - nearestPositive)
        elif not negsign and not checkForAllCompleted:
            nearestTodo = (i + nearestNegative)
        else:
            nearestTodo = None

        # print("nearestTodo",nearestTodo)
        # print("///////////////////////////////////////////////////////")
        return nearestTodo
