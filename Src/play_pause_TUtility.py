import datetime
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


class PlayPauseUtility:

    def __init__(self, app):
        self.App = app
        self.playOnStart = True

        print("Initialized Todo Play Events")

    def playpauseTodo(self, button, comp, index):
        index = self.App.TodoList.index(comp)
        data = self.changeComponentIconsAndState("playpause", comp, index, None)
        self.pauseOtherTodo(index, data)



    def pauseOtherTodo(self, index, data):

        length = len(self.App.TodoList)
        for i in range(length):
            if i != index and self.App.TodoList[i].state == "Playing":
                todoComp = self.App.TodoList[i]
                data = self.changeComponentIconsAndState("pause", todoComp, i, data)

        self.App.Store.localWrite(data)

    def changeComponentIconsAndState(self, which, comp, index, data):

        fileData = data or self.App.Store.getDatabase()

        if which == "playpause":
            icon = comp.controlButton.get_children()[0];
            if comp.state != "Playing":
                icon.set_from_icon_name("media-playback-pause", Gtk.IconSize.BUTTON)
                comp.state = "Playing"
                fileData[index]["state"] = "Playing"
                self.App.canProgress = True;
                self.App.ProgressTUtility.advanceProgress(fileData[index]["progress"], fileData[index]["data"]["time"],
                                                          comp,
                                                          datetime.datetime.now(), index, fileData)
            else:
                icon.set_from_icon_name("media-playback-start", Gtk.IconSize.BUTTON);
                comp.state = "Paused"
                fileData[index]["state"] = "Paused"
                if comp.progressThread is not None:
                    GLib.source_remove(comp.progressThread)
                    comp.progressThread = None
                    comp.absoluteProgress = (comp.todoProgress.get_fraction() * 100)

        if which == "pause":

            if comp.state == "Playing":
                icon = comp.controlButton.get_children()[0];
                icon.set_from_icon_name("media-playback-start", Gtk.IconSize.BUTTON);
                comp.state = "Paused"
                fileData[index]["state"] = "Paused"
                if comp.progressThread is not None:
                    GLib.source_remove(comp.progressThread)
                    comp.progressThread = None
                    comp.absoluteProgress = (comp.todoProgress.get_fraction() * 100)

        if which == "play":
            icon = comp.controlButton.get_children()[0];
            icon.set_from_icon_name("media-playback-pause", Gtk.IconSize.BUTTON);
            comp.state = "Playing"
            fileData[index]["state"] = "Playing"
            self.App.ProgressTUtility.advanceProgress(fileData[index]["progress"], fileData[index]["data"]["time"],
                                                      comp,
                                                      datetime.datetime.now(), index, fileData)

        if which == "complete":
            icon = comp.controlButton.get_children()[0];
            icon.set_from_icon_name("media-seek-backward", Gtk.IconSize.BUTTON);
            comp.state = "Completed"
            fileData[index]["state"] = "Completed"
            if comp.progressThread is not None:
                comp.absoluteProgress = 100
                GLib.source_remove(comp.progressThread)
                comp.progressThread = None

        return fileData;

    def changeComponentIcons(self, which, comp):
        if which == "pause":
            icon = comp.controlButton.get_children()[0];
            icon.set_from_icon_name("media-playback-start", Gtk.IconSize.BUTTON);

        if which == "play":
            icon = comp.controlButton.get_children()[0];
            icon.set_from_icon_name("media-playback-pause", Gtk.IconSize.BUTTON);
