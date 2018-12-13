import sublime, sublime_plugin, subprocess, os

import webbrowser

class ShowMayaDocs(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            selected_text = self.view.substr(region)

            maya_docs_url = "http://help.autodesk.com/cloudhelp/2016/ENU/" + \
                            "Maya-Tech-Docs/CommandsPython/" + selected_text + \
                            ".html"

            webbrowser.open(maya_docs_url, autoraise=True)