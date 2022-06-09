from Todo import App

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class PlayPauseUtility(App):

    def __init__(self):
        self.inputPermission = True

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