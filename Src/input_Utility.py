def getActiveRadio(radio):
    active = None
    for rad in radio.get_group():
        if rad.get_active():
            active = rad
    return active


class InputUtility:

    def __init__(self, app):
        self.App = app
        self.inputPermission = True

        print("Initialized Todo Form Events")

    def getInputForTodo(self):
        title = str(self.App.Builder.get_object("inputTitle").get_text())
        time = self.App.Builder.get_object("inputTime").get_value()
        timeUnit = getActiveRadio(self.App.Builder.get_object("TodoHour")).get_label()
        alarm = getActiveRadio(self.App.Builder.get_object("TodoAlarmYes")).get_label()

        if title.strip() == "":
            title = "new Todo"

        if timeUnit == "Hours":
            time = time * 60

        if alarm == "ON":
            alarm = True
        else:
            alarm = False

        return {"title": title, "time": time, "alarm": alarm}
