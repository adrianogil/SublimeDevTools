import sublime, sublime_plugin, subprocess

class FindMeCurrentSourceCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        current_file = self.view.file_name()

        if current_file is None:
            return

        where_to_search = current_file

        self.view.window().run_command("show_panel", {"panel": "find_in_files", "where": where_to_search})

class AutomatedNumberedDebugCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        current_file = self.view.file_name()

        if current_file is None:
            return

        current_clipboard = sublime.get_clipboard()

        print("AutomatedNumberedDebugCommand  " + str(current_file))
        print("AutomatedNumberedDebugCommand  " + current_clipboard)

        repl_pattern_str = '%LV%'

        if not repl_pattern_str in current_clipboard:
            return

        for region in self.view.sel():
            selected_text = self.view.substr(region)
            replace_text = ''
            print("AutomatedNumberedDebugCommand  selected: " + str(selected_text))
            n_debug = 0
            valid_content_between_newlines = False
            for s in selected_text:
                replace_text = replace_text + s
                if s == ';':
                    valid_content_between_newlines = True
                if s == '\n':
                    print("AutomatedNumberedDebugCommand - Identified newline")
                    if valid_content_between_newlines:
                        current_debug = current_clipboard.replace(repl_pattern_str, str(n_debug))
                        n_debug = n_debug + 1
                        replace_text = replace_text + current_debug + '\n'
                        valid_content_between_newlines = False

            self.view.replace(edit, region, replace_text)

class OpenProjectInTerminal(sublime_plugin.TextCommand):
    def run(self, edit):
        folders = self.view.window().folders()

        open_in_terminal_cmd = 'open -a Terminal "' + folders[0] + '"'
        subprocess.check_output(open_in_terminal_cmd, shell=True)


class InvertMe(sublime_plugin.TextCommand):
    def run(self, edit):

        for region in self.view.sel():
            selected_text = self.view.substr(region)

            self.view.replace(edit, region, selected_text[::-1])

class SplitMe(sublime_plugin.TextCommand):
    def run(self, edit):
        split_object = sublime.get_clipboard()

        for region in self.view.sel():
            selected_text = self.view.substr(region)

            split_text = selected_text.split(split_object)

            new_text = ''

            for s in split_text:
                new_text = new_text + s + '\n'

            self.view.replace(edit, region, new_text)

class SortMe(sublime_plugin.TextCommand):
    def run(self, edit):

        for region in self.view.sel():
            selected_text = self.view.substr(region)

            split_text = selected_text.split('\n')

            split_text.sort()

            new_text = ''

            for s in split_text:
                new_text = new_text + s + '\n'

            self.view.replace(edit, region, new_text)

class SmartSelectionFromClipboard(sublime_plugin.TextCommand):
    def run(self, edit):
        current_file = self.view.file_name()

        if current_file is None:
            return

        target_from_clipboard = sublime.get_clipboard()

        print("SmartSelectionFromClipboard: " + target_from_clipboard)

        targets = []

        for region in self.view.sel():
            current_begin = region.begin()
            current_end = region.end()

            found_all = False

            while current_begin < current_end and not found_all:
                current_region = sublime.Region(current_begin, current_end)
                content = self.view.substr(current_region)
                begin = content.find(target_from_clipboard)
                if begin == -1:
                    found_all = True
                else:
                    begin = begin + current_begin
                    end = begin + len(target_from_clipboard)
                    target_region = sublime.Region(begin, end)

                    print("SmartSelectionFromClipboard: added region " + str(begin) + " - " + str(end))

                    targets.append(target_region)

                    current_begin = end + 1

        self.view.sel().clear()
        for t in targets:
            self.view.sel().add(t)
