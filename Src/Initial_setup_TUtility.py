import datetime


class InitialSetupUtility:

    def __init__(self, app):
        self.canProgress = None
        self.App = app
        self.changeStackToDefault(self.App.TodoContainer)
        self.initializeTodo()
        print("Initial Setup Done")

    def initializeTodo(self):

        loaded = self.App.Store.getDatabase()

        for i, data in enumerate(loaded):
            saved = data.get("data")
            progress = data.get("progress")

            todo = self.App.AddRemoveTUtility.addTodoComp(saved.get("title"))
            todo.todoCounter.set_text(str(i + 1))
            todo.state = loaded[i]["state"]
            todo.absoluteProgress = progress

            self.App.TodoList.append(todo)
            self.App.Events.addDefaultTodoHandlers(todo, i)
            self.App.ProgressTUtility.setTodoProgress(todo, progress)

            if loaded[i]["state"] == "Playing":
                self.App.PlayPauseTUtility.changeComponentIcons("play", todo)
                self.canProgress = True
                self.App.ProgressTUtility.advanceProgress(loaded[i]["progress"], loaded[i]["data"]["time"], todo,
                                                          datetime.datetime.now(), i,
                                                          loaded)
            elif loaded[i]["state"] == "Paused":
                self.App.PlayPauseTUtility.changeComponentIcons("pause", todo)

            elif loaded[i]["state"] == "Completed":
                self.App.PlayPauseTUtility.changeComponentIcons("complete", todo)
                todo.absoluteProgress = 100
                todo.relativeProgress = 100
                self.App.ProgressTUtility.setTodoProgress(todo, todo.absoluteProgress)

    def changeStackToDefault(self, default):
        self.App.Stack.set_visible_child(default)


