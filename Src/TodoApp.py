import datetime
import gi
import TodoTComp
import json

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

# the rewind button is not set the progress is not in store ie not storing
# bug found : start first todo wait till end
# now stop the program and reopen it , you will see 1st and 3rd todo not completed

builder = Gtk.Builder()
builder.add_from_file("../Todo_Glade.glade")

screen = Gdk.Screen.get_default()
cprovider = Gtk.CssProvider()
cprovider.load_from_path("../assets/css/main.css")
Gtk.StyleContext.add_provider_for_screen(screen, cprovider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


def getActiveRadio(radio):
    active = None
    for rad in radio.get_group():
        if rad.get_active():
            active = rad
    return active


class App:

    def __init__(self):
        self.Window = builder.get_object("MainWindow")
        self.TodoContainer = builder.get_object("TodoContainer")
        self.newTodoButton = builder.get_object("createNewTodo")
        self.discardTodoButton = builder.get_object("discardNewTodo")
        #################################
        self.Builder = builder
        #################################
        self.TodoList = []
        self.DataStorage = "../assets/data/database.json"

        self.newTodoButton.connect("clicked", self.wantsToCreateTodo)
        self.canProgress = False;

        self.initialSetup()

        self.Window.connect("destroy", Gtk.main_quit)
        self.Window.show_all()

    def getTodoContainerChild(self):
        return Gtk.Box.get_children(self.TodoContainer)

    def addTodoComp(self, title):
        todoComponent = TodoTComp.Todo({"title": title, "counter": str(len(self.getTodoContainerChild()) + 1)})
        Gtk.Box.add(self.TodoContainer, todoComponent.todo)
        return todoComponent

    def getInputForTodo(self):
        title = str(builder.get_object("inputTitle").get_text())
        time = builder.get_object("inputTime").get_value()
        timeUnit = getActiveRadio(builder.get_object("TodoHour")).get_label()
        alarm = getActiveRadio(builder.get_object("TodoAlarmYes")).get_label()

        if title.strip() == "":
            title = "new Todo"

        if timeUnit == "Hours":
            time = time * 60

        if alarm == "ON":
            alarm = True
        else:
            alarm = False

        return {"title": title, "time": time, "alarm": alarm}

    def wantsToCreateTodo(self, widget, data=None):
        data = self.getInputForTodo()
        todo = self.addTodoComp(data.get("title"))
        self.TodoList.append(todo)
        created = {"data": data, "time": str(datetime.datetime.now()),"state":todo.state,"progress":0}
        self.saveToStore(created)
        self.addDefaultTodoHandlers(todo, (len(self.TodoList)-1))

    def saveToStore(self, data):
        file = open(self.DataStorage, 'r')
        loaded = json.load(file)
        file.close()
        loaded.append(data)
        self.localWrite(loaded)

    def removeFromStoreByIndex(self, index):
        file = open(self.DataStorage, 'r')
        loaded = json.load(file)
        file.close()

        if index is not None and index < len(loaded):
            del loaded[index]

        self.localWrite(loaded)

    def removeFromStoreByValue(self, value):
        file = open(self.DataStorage, 'r')
        loaded = json.load(file)
        file.close()

        if value and value in loaded:
            loaded.remove(value)

        self.localWrite(loaded)

    def localWrite(self, data):
        file2 = open(self.DataStorage, 'w')
        file2.write(json.dumps(data))
        file2.close()

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
            todo.state=loaded[i]["state"];
            self.setTodoProgress(todo,(loaded[i]["progress"]))


            if(loaded[i]["state"]=="Playing"):
                self.changeComponentIcons("play",todo)
                self.canProgress=True
                self.advanceProgress(loaded[i]["progress"], loaded[i]["data"]["time"], todo,datetime.datetime.now(),i,loaded)
            elif(loaded[i]["state"]=="Paused"):
                self.changeComponentIcons("pause", todo)


    def removeTodo(self, index):
        if(self.TodoList[index].state=="Playing"):
            del self.TodoList[index]
            self.removeFromStoreByIndex(index)
            if(len(self.TodoList) > 0):
                self.playpauseTodo(0,self.TodoList[0],0)
        else:
            del self.TodoList[index]
            self.removeFromStoreByIndex(index)

    def addDefaultTodoHandlers(self, todoComp, index):
        todoComp.removeButton.connect("clicked", self.removeTodoExcited, todoComp)
        todoComp.controlButton.connect("clicked", self.playpauseTodo, todoComp,index)

    def removeTodoExcited(self, button, comp):
        index = self.TodoList.index(comp)
        self.TodoContainer.remove(comp.todo)
        self.removeTodo(index)
        self.correctLabelCounter(index)

    def correctLabelCounter(self, index):
        length = len(self.TodoList)
        for i in range(index, length):
            todoComp = self.TodoList[i]
            todoComp.todoCounter.set_text(str(i+1))

    def playpauseTodo(self,button,comp,index):
        index = self.TodoList.index(comp)
        data = self.changeComponentIconsAndState("playpause",comp,index,None)
        self.pauseOtherTodo(index,data)


    def changeComponentIconsAndState(self,which,comp,index,data):

        fileData = data or self.getDatabase()

        if(which == "playpause"):
            icon = comp.controlButton.get_children()[0];

            if (comp.state != "Playing"):
                icon.set_from_icon_name("media-playback-pause", Gtk.IconSize.BUTTON)
                comp.state = "Playing"
                fileData[index]["state"] = "Playing"
                self.canProgress=True;
                self.advanceProgress(fileData[index]["progress"],fileData[index]["data"]["time"],comp,datetime.datetime.now(),index,fileData)
            else:
                icon.set_from_icon_name("media-playback-start", Gtk.IconSize.BUTTON);
                comp.state = "Paused"
                fileData[index]["state"] =  "Paused"
                if(comp.progressThread!=None):
                    GLib.source_remove(comp.progressThread)
                    comp.progressThread = None
                    comp.absoluteProgress = (comp.todoProgress.get_fraction()*100)

        if (which == "pause"):
            if (comp.state == "Playing"):
                icon = comp.controlButton.get_children()[0];
                icon.set_from_icon_name("media-playback-start", Gtk.IconSize.BUTTON);
                comp.state = "Paused"
                fileData[index]["state"] =  "Paused"
                if (comp.progressThread != None):
                    GLib.source_remove(comp.progressThread)
                    comp.progressThread = None
                    comp.absoluteProgress = (comp.todoProgress.get_fraction() * 100)

        if (which == "play"):
            icon = comp.controlButton.get_children()[0];
            icon.set_from_icon_name("media-playback-pause", Gtk.IconSize.BUTTON);
            comp.state = "Playing"
            fileData[index]["state"] = "Playing"
            self.advanceProgress(fileData[index]["progress"], fileData[index]["data"]["time"], comp,datetime.datetime.now(),index,fileData)

        if (which == "complete"):
            icon = comp.controlButton.get_children()[0];
            icon.set_from_icon_name("media-seek-backward", Gtk.IconSize.BUTTON);
            comp.state = "Completed"
            fileData[index]["state"] =  "Completed"
            if (comp.progressThread != None):
                comp.absoluteProgress = 100
                GLib.source_remove(comp.progressThread)
                comp.progressThread = None

        return fileData;

    def changeComponentIcons(self, which, comp):
        if (which == "pause"):
            icon = comp.controlButton.get_children()[0];
            icon.set_from_icon_name("media-playback-start", Gtk.IconSize.BUTTON);

        if (which == "play"):
            icon = comp.controlButton.get_children()[0];
            icon.set_from_icon_name("media-playback-pause", Gtk.IconSize.BUTTON);

    def pauseOtherTodo(self,index,data):
        length = len(self.TodoList)
        for i in range(length):
            if(i!=index and self.TodoList[i].state=="Playing"):
                todoComp = self.TodoList[i]
                data = self.changeComponentIconsAndState("pause",todoComp,i,data)
        self.localWrite(data)

    def modifyTodoStoreProperty(self,index,option,value):
        file = open(self.DataStorage, 'r')
        loaded = json.load(file)
        file.close()
        loaded[index][option] = value;
        self.localWrite(loaded)

    def getDatabase(self):
        file = open(self.DataStorage, 'r')
        loaded = json.load(file)
        file.close()
        return loaded

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


    # def pu(self):
    #     print(datetime.datetime.now())
    #     GLib.timeout_add_seconds(1, self.pu)


App()
Gtk.main()
