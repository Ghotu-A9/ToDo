import datetime
import TodoTComp
from Todo import App
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


class AddRemoveUtility(App):
    def __init__(self):
        self.newTodoButton = self.Builder.get_object("createNewTodo")
        self.discardTodoButton = self.Builder.get_object("discardNewTodo")

    def initialSetup(self):
        file = open(self.DataStorage, 'r')
        loaded = json.load(file)
        file.close()

        for i, data in enumerate(loaded):
            saved = data.get("data")
            todo = self.addTodoComp(saved.get("title"))
            todo.todoCounter.set_text(str(i + 1))
            self.TodoList.append(todo)
            self.addDefaultTodoHandlers(todo, i)
            todo.state = loaded[i]["state"];
            self.setTodoProgress(todo, (loaded[i]["progress"]))

            if (loaded[i]["state"] == "Playing"):
                self.changeComponentIcons("play", todo)
                self.canProgress = True
                self.advanceProgress(loaded[i]["progress"], loaded[i]["data"]["time"], todo,
                                     datetime.datetime.now(), i, loaded)
            elif (loaded[i]["state"] == "Paused"):
                self.changeComponentIcons("pause", todo)

    def getTodoContainerChild(self):
        return Gtk.Box.get_children(self.TodoContainer)

    def addTodoComp(self, title):
        todoComponent = TodoTComp.Todo({"title": title, "counter": str(len(self.getTodoContainerChild()) + 1)})
        Gtk.Box.add(self.TodoContainer, todoComponent.todo)
        return todoComponent

    def wantsToCreateTodo(self, widget, data=None):
        data = self.getInputForTodo()
        todo = self.addTodoComp(data.get("title"))
        self.TodoList.append(todo)
        created = {"data": data, "time": str(datetime.datetime.now()), "state": todo.state, "progress": 0}
        self.saveToStore(created)
        self.addDefaultTodoHandlers(todo, (len(self.TodoList) - 1))

    def removeTodo(self, index):
        if (self.TodoList[index].state == "Playing"):
            del self.TodoList[index]
            self.removeFromStoreByIndex(index)
            if (len(self.TodoList) > 0):
                self.playpauseTodo(0, self.TodoList[0], 0)
        else:
            del self.TodoList[index]
            self.removeFromStoreByIndex(index)

    def removeTodoExcited(self, button, comp):
        index = self.TodoList.index(comp)
        self.TodoContainer.remove(comp.todo)
        self.removeTodo(index)
        self.correctLabelCounter(index)

    def correctLabelCounter(self, index):
        length = len(self.TodoList)
        for i in range(index, length):
            todoComp = self.TodoList[i]
            todoComp.todoCounter.set_text(str(i + 1))
