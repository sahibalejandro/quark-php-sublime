# encoding=utf8
import sublime, sublime_plugin
import os
import functools
import threading

class QuarkPhpNewControllerCommand(sublime_plugin.WindowCommand):
  def run(self, dirs):
    self.window.show_input_panel("New Quark PHP Controller:", "Home", functools.partial(self.on_done, dirs[0]), None, None)

  def on_done(self, dir, name):
    if name == -1:
        return
    else:
        # Crear la ruta donde se guardará el archivo
        file_path  = os.path.join(dir, name + "Controller.php")

        # Crear el nuevo archivo
        new_file = open(file_path, "w")
        new_file.write("<?php\nclass " + name + "Controller ")
        new_file.close()
        
        # Abrir el archivo en la ventana actual
        new_view = self.window.open_file(file_path)

        # Iniciar el thread para esperar a que el view este cargado e insertar
        # el snippet
        thread = QuarkPHPInsertSnippetThread(new_view, "controller")
        thread.start()

class QuarkPhpNewOrmCommand(sublime_plugin.WindowCommand):
  def run(self, dirs):
    self.window.show_input_panel("New Quark ORM:", "MyORM", functools.partial(self.on_done, dirs[0]), None, None)

  def on_done(self, dir, name):
    if name == -1:
        return
    else:
        # Crear la ruta donde se guardará el archivo
        file_path  = os.path.join(dir, name + "ORM.php")

        # Crear el nuevo archivo
        new_file = open(file_path, "w")
        new_file.write("<?php\nclass " + name + "ORM ")
        new_file.close()
        
        # Abrir el archivo en la ventana actual
        new_view = self.window.open_file(file_path)

        # Iniciar el thread para esperar a que el view este cargado e insertar
        # el snippet
        thread = QuarkPHPInsertSnippetThread(new_view, "orm")
        thread.start()

class QuarkPHPInsertSnippetThread(threading.Thread):
    def __init__(self, view, snippet):
        self.view = view
        self.snippet = snippet
        threading.Thread.__init__(self)

    def run(self):
        while self.view.is_loading():
            continue
        
        # Abrir el archivo con el snippet
        snippet_file = open(os.path.join(sublime.packages_path(), 'QuarkPHP', 'snippets', self.snippet), "r")

        # Insertar snippet
        self.view.run_command("move_to", {"to": "eof", "extend": False})
        self.view.run_command("insert_snippet", {"contents": snippet_file.read()})