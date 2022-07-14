import threading

import gi
import datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


class AddRemoveUtility:

    def __init__(self, app):
        self.App = app
        print("Initialized Todo Creation Functionality")

    def getTodoContainerChild(self):
        return Gtk.Box.get_children(self.App.TodoContainer)

    def addTodoComp(self, title):
        todoComponent = self.App.TodoTCompClass.Todo(
            {"title": title, "counter": str(len(self.getTodoContainerChild()) + 1)})
        Gtk.Box.add(self.App.TodoContainer, todoComponent.todo)
        return todoComponent

    def wantsToCreateTodo(self, widget, data=None):

        data = self.App.Input.getInputForTodo()

        dictData = {
            "placeholder": data.get("title"),
            "time": 0,
            "extra_time": 0,
            "programs": [],
            "p_time": {}
        }

        localAnalytics = self.App.DBStore.saveLocalAnalyticalData(dictData)

        if localAnalytics.get('saved') is True:
            todo = self.addTodoComp(data.get("title"))

            todo.aId = localAnalytics.get('id')

            self.App.TodoList.append(todo)
            created = {"data": data, "time": str(datetime.datetime.now()), "state": todo.state, "progress": 0, "a_id": localAnalytics.get('id'), "is_completed": False}
            self.App.Store.saveToStore(created)
            self.App.Events.addDefaultTodoHandlers(todo, (len(self.App.TodoList) - 1))

    def removeTodo(self, index):
        if self.App.TodoList[index].state == "Playing":
            if len(self.App.TodoList) > 0 and self.App.TodoList[0]:
                nearestTodo = self.App.Operation.findNearestPausedTodo(index)
                if nearestTodo != 0:
                    self.App.PlayPauseTUtility.playpauseTodo(0, self.App.TodoList[nearestTodo], nearestTodo)
            self.removeAnalyticalData(index)
            del self.App.TodoList[index]
            self.App.Store.removeFromStoreByIndex(index)
        else:
            self.removeAnalyticalData(index)
            del self.App.TodoList[index]
            self.App.Store.removeFromStoreByIndex(index)

    def removeTodoExcited(self, button, comp):
        index = self.App.TodoList.index(comp)
        self.App.TodoContainer.remove(comp.todo)
        self.removeTodo(index)
        self.correctLabelCounter(index)

    def correctLabelCounter(self, index):
        length = len(self.App.TodoList)
        for i in range(index, length):
            todoComp = self.App.TodoList[i]
            todoComp.todoCounter.set_text(str(i + 1))

    def removeAnalyticalData(self, index):
        def remove(i):
            self.App.DBStore.removeSingleRowLocalAnalyticalData(self.App.TodoList[i].aId)

        threading.Thread(target=remove,
                         args=(index,),
                         daemon=True).start()
