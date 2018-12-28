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


class GenerateMayaCall(sublime_plugin.TextCommand):
    def run(self, edit):
        current_file = self.view.file_name()

        script_path = os.path.dirname(current_file)
        module_name = os.path.basename(current_file)
        module_name = module_name.replace('.py', '')

        call_str = 'import sys\n'
        call_str += 'script_path = "' + script_path + '"\n'
        call_str += 'sys.path.insert(0, script_path)\n\n'
        call_str += 'loaded = "' + module_name + '" in sys.modules\n\n'
        call_str += 'import ' + module_name + '\n\n'
        call_str += 'if loaded:\n'
        call_str += '\treload(' + module_name + ')\n'

        sublime.set_clipboard(call_str)
