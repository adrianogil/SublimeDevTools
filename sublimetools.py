import sublime, sublime_plugin

import json

class LoadSublimeWindowLayoutCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        layout_file = sublime.get_clipboard()

        with open(layout_file, 'r') as f:
            layout_dict = json.load(f)

        self.view.window().run_command('set_layout', layout_dict['layout'])

        for g in layout_dict['groups']:
            for v in layout_dict['groups'][g]:
                self.view.window().focus_group(int(g))
                self.view.window().open_file(v)


class SaveSublimeWindowLayoutCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        num_groups = self.view.window().num_groups()

        layout_dict = {}

        layout = self.view.window().get_layout()
        layout_dict['layout'] = layout
        layout_dict['groups'] = {}

        for i in range(0, num_groups):
            views = self.view.window().views_in_group(i)

            files_in_view = []

            for v in views:
                print("Group: %s - file %s" % (i, v.file_name()))
                files_in_view.append(v.file_name())

            layout_dict['groups'][str(i)] = files_in_view

        layout_file = sublime.get_clipboard()

        print(layout_file)

        with open(layout_file, 'w') as f:
            json.dump(layout_dict, f)


class closeOtherTabsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window = self.view.window()
        group_index, view_index = window.get_view_index(self.view)
        window.run_command("close_others_by_index", { "group": group_index, "index": view_index})
