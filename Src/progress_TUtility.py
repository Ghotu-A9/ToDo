from Todo import App
import datetime
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


class ProgressUtility (App):
    def __init__(self):
        self.canProgress = False;

    def setTodoProgress(self,todo,value):
        todo.todoProgress.set_fraction( value / 100);
        todo.progressLabel.set_text(str(round(value,2)) + "%");

    def advanceProgress(self,initial,given,comp,lastTime,i,data):
        if(self.canProgress):
            timeEllipsed=((datetime.datetime.now() - lastTime).total_seconds())/60
            comp.relativeProgress = (timeEllipsed / given) * 100
            progress = comp.absoluteProgress + (timeEllipsed / given) * 100

            comp.progressThread=GLib.timeout_add(1, self.advanceProgress,initial+timeEllipsed,given,comp,lastTime,i,data)
            self.setTodoProgress(comp,progress)
            if(progress>=100):
                GLib.source_remove(comp.progressThread)
                comp.progressThread = None
                self.setTodoProgress(comp, 100)
                self.todoProgressCompleted(comp,i,data)

    def todoProgressCompleted(self,comp,i,data):
        self.changeComponentIconsAndState("complete",comp,i,data)
        nearestPositive = 1
        nearestNegative = len(self.TodoList)
        negsign = False
        if (len(self.TodoList)>1):
            length = len(self.TodoList)
            for l in range(length):
                if (self.TodoList[l].state == "Paused"):
                    if((i-l) > 0):
                        nearestPositive = (i - l)
                        negsign = True
                        #print("upper", nearestPositive)
                    elif((i-l) < 0):
                        nearestNegative =  (l - i)
                        #print("lower",nearestNegative)
                        negsign = False
                        break


        if(negsign):
            if(self.TodoList[i - nearestPositive].state != "Completed"):
                self.playpauseTodo(None, self.TodoList[i - nearestPositive], (i - nearestPositive))
        else:
            if ((i + nearestNegative)<(len(self.TodoList))):
                if(self.TodoList[i + nearestNegative].state != "Completed"):
                    self.playpauseTodo(None, self.TodoList[i + nearestNegative], (i + nearestNegative))

        self.localWrite(data)