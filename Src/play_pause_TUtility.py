import datetime
import threading

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


class PlayPauseUtility:

    def __init__(self, app):
        self.App = app
        self.playOnStart = True
        self.reloadAmount = 50

        print("Initialized Todo Play Events")

    def playpauseTodo(self, button, comp, index):
        index = self.App.TodoList.index(comp)
        data = None

        if comp.isCompleted:
            self.App.DBStore.updateLocalAnalyticalData((index + 1), "extra_time", comp.extraATime)

        if comp.state == "Completed":

            comp.absoluteProgress = (comp.absoluteProgress - (comp.absoluteProgress * (self.reloadAmount / 100)))
            comp.relativeProgress = (comp.absoluteProgress - (comp.absoluteProgress * (self.reloadAmount / 100)))
            self.App.ProgressTUtility.setTodoProgress(comp, comp.absoluteProgress)

            data = self.changeComponentIconsAndState("playpause", comp, index, None)
        else:
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

        if comp.isCompleted:
            self.updateAnalytics_ExtraTime(comp, index)

        fileData = data or self.App.Store.getDatabase()

        if which == "playpause":

            if comp.state != "Playing":
                self.changeComponentIcons("play", comp)
                comp.state = "Playing"
                self.App.ActiveTodoIndex = index
                fileData[index]["state"] = "Playing"
                fileData[index]["progress"] = comp.absoluteProgress
                self.App.canProgress = True
                self.App.ProgressTUtility.advanceProgress(fileData[index]["progress"], fileData[index]["data"]["time"],
                                                          comp,
                                                          datetime.datetime.now(), index, fileData)
            else:
                self.changeComponentIcons("pause", comp)
                comp.state = "Paused"

                self.checkForCompletedAndPausedTodo(index)

                fileData[index]["state"] = "Paused"
                fileData[index]["progress"] = comp.absoluteProgress
                if comp.progressThread is not None:
                    GLib.source_remove(comp.progressThread)
                    comp.progressThread = None
                    comp.absoluteProgress = (comp.todoProgress.get_fraction() * 100)
                    fileData[index]["progress"] = comp.absoluteProgress

        if which == "pause":

            if comp.state == "Playing":

                self.changeComponentIcons("pause", comp)
                comp.state = "Paused"

                self.checkForCompletedAndPausedTodo(index)

                fileData[index]["state"] = "Paused"
                fileData[index]["progress"] = comp.absoluteProgress

                if comp.progressThread is not None:
                    GLib.source_remove(comp.progressThread)
                    comp.progressThread = None
                    comp.absoluteProgress = (comp.todoProgress.get_fraction() * 100)

        if which == "play":
            self.changeComponentIcons("play", comp)
            comp.state = "Playing"
            self.App.ActiveTodoIndex = index
            fileData[index]["state"] = "Playing"
            fileData[index]["progress"] = comp.absoluteProgress
            self.App.Store.modifyTodoStoreProperty(index, "progress", comp.absoluteProgress)
            self.App.ProgressTUtility.advanceProgress(fileData[index]["progress"], fileData[index]["data"]["time"],
                                                      comp,
                                                      datetime.datetime.now(), index, fileData)

        if which == "complete":
            self.changeComponentIcons("complete", comp)
            comp.state = "Completed"
            self.checkForCompletedAndPausedTodo(index)

            fileData[index]["state"] = "Completed"
            fileData[index]["progress"] = comp.absoluteProgress

            if comp.progressThread is not None:
                comp.absoluteProgress = 100
                GLib.source_remove(comp.progressThread)
                comp.progressThread = None

        return fileData

    def changeComponentIcons(self, which, comp):
        icon = comp.controlButton.get_children()[0]
        if which == "pause":
            icon.set_from_icon_name("media-playback-start", Gtk.IconSize.BUTTON)
            comp.controlButton.set_tooltip_text("Play")

        if which == "play":
            icon.set_from_icon_name("media-playback-pause", Gtk.IconSize.BUTTON)
            comp.controlButton.set_tooltip_text("Pause")

        if which == "complete":
            icon.set_from_icon_name("media-seek-backward", Gtk.IconSize.BUTTON)
            comp.controlButton.set_tooltip_text("Rewind")

    def updateAnalytics_ExtraTime(self, comp, index):

        def update(c, i):
            self.App.DBStore.updateLocalAnalyticalData((i + 1), "extra_time", c.extraATime)

        threading.Thread(target=update,
                         args=(comp, index),
                         daemon=True).start()

    def checkForCompletedAndPausedTodo(self, index):
        if self.App.ActiveTodoIndex == index:
            self.App.ActiveTodoIndex = None
