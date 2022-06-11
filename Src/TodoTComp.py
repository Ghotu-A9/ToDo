import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

builder = Gtk.Builder()


class Todo:
    def __init__(self, param):
        self.con = param.get("counter") or str(0)
        self.title = param.get("title") or "New ToDo"
        self.state = "Created"
        self.template = param.get("template") or "../assets/glade/todoCard.glade"

        builder.add_from_file(self.template)

        self.todo = builder.get_object("TodoMain")
        self.todoLabel = builder.get_object("TodoLabel")
        self.todoCounter = builder.get_object("TodoCounter")
        self.todoProgress = builder.get_object("TodoProgress")
        self.progressLabel = builder.get_object("ProgressLabel")
        self.removeButton = builder.get_object("RemoveTodo")
        self.editButton = builder.get_object("EditTodo")
        self.controlButton = builder.get_object("ResumeTodo")
        self.completeButton = builder.get_object("ApplyTodo")
        self.progressThread = None
        self.lastInitialisation = None;
        self.relativeProgress = 0
        self.absoluteProgress = 0

        self.initialize()

    def initialize(self):
        self.todoLabel.set_text(self.title)
        self.todoCounter.set_text(self.con)
