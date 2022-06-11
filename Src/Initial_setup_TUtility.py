import datetime


class InitialSetupUtility:

    def __init__(self, app):
        self.App = app
        self.initializeTodo()

    def initializeTodo(self):

        loaded = self.App.Store.getDatabase()

        for i, data in enumerate(loaded):
            saved = data.get("data")
            todo = self.App.AddRemoveTUtility.addTodoComp(saved.get("title"))
            todo.todoCounter.set_text(str(i + 1))
            self.App.TodoList.append(todo)
            self.App.Events.addDefaultTodoHandlers(todo, i)
            todo.state = loaded[i]["state"];
            self.App.ProgressTUtility.setTodoProgress(todo, (loaded[i]["progress"]))

            if (loaded[i]["state"] == "Playing"):
                self.App.PlayPauseTUtility.changeComponentIcons("play", todo)
                self.canProgress = True
                self.App.ProgressTUtility.advanceProgress(loaded[i]["progress"], loaded[i]["data"]["time"], todo, datetime.datetime.now(), i,
                                     loaded)
            elif (loaded[i]["state"] == "Paused"):
                self.App.PlayPauseTUtility.changeComponentIcons("pause", todo)

            print("Initial Setup Done")
