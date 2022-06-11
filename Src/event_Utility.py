class EventUtility:

    def __init__(self, app):
        self.App = app
        self.setTUtilityEvents()

        print("Initialized Todo Control Events")

    def setTUtilityEvents(self):
        self.App.AddRemoveTUtility.newTodoButton.connect("clicked", self.App.AddRemoveTUtility.wantsToCreateTodo)

    def addDefaultTodoHandlers(self, todoComp, index):
        todoComp.removeButton.connect("clicked", self.App.AddRemoveTUtility.removeTodoExcited, todoComp)
        todoComp.controlButton.connect("clicked", self.App.PlayPauseTUtility.playpauseTodo, todoComp, index)
