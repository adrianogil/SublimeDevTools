import sublime, sublime_plugin, subprocess, os

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

class OpenPathInTerminal(sublime_plugin.TextCommand):
    def run(self, edit):
        current_file = self.view.file_name()

        if current_file is None:
            return

        current_path = os.path.dirname(current_file)

        open_in_terminal_cmd = 'open -a Terminal "' + current_path + '"'
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

class SmartReplaceFromClipboard(sublime_plugin.TextCommand):
    def run(self, edit):
        replace_format = sublime.get_clipboard()

        replace_string = '%LV%'

        for region in self.view.sel():
            selected_text = self.view.substr(region)

            new_text = replace_format.replace(replace_string, selected_text)

            self.view.replace(edit, region, new_text)

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        pass

    return False

def is_operation(s):
    return s == '*' or s == '+' or s == '-' or s == '/'

class EvolveFromClipboardInstances(sublime_plugin.TextCommand):
    def run(self, edit):
        instances = sublime.get_clipboard()

        instances_values = []

        if is_int(instances[0]):
            number_1 = ''
            number_2 = '.'

            for s in instances:
                if number_2 == '.':
                    if is_int(s):
                        number_1 = number_1 + s
                    else:
                        number_2 = ''
                elif is_int(s):
                    number_2 = number_2 + s

            number_1 = int(number_1)
            number_2 = int(number_2)

            for i in range(number_1, number_2+1):
                instances_values.append(str(i))

        elif instances[0] == '{' and instances[len(instances)-1] == '}':
            instances_values = instances[1:len(instances)-1].split(',')
        else:
            return

        replace_string = '%LV%'

        for region in self.view.sel():
            selected_text_pattern = self.view.substr(region)

            new_text = ''

            for instance in instances_values:
                if is_int(instance):
                    i = 0
                    while i < len(selected_text_pattern):
                        if i < len(selected_text_pattern) - 4 and selected_text_pattern[i:i+3] == '%LV':
                            current_number = int(instance)
                            current_operation=''
                            number_str = ''
                            i = i + 3
                            while selected_text_pattern[i] != '%':
                                if is_operation(selected_text_pattern[i]):
                                    if current_operation == '':
                                        pass
                                    elif number_str != '':
                                        if current_operation == '+':
                                            current_number = current_number + int(number_str)
                                        elif current_operation == '-':
                                            current_number = current_number - int(number_str)
                                        elif current_operation == '*':
                                            current_number = current_number * int(number_str)
                                        elif current_operation == '/':
                                            current_number = current_number / int(number_str)
                                        number_str = ''
                                    current_operation = selected_text_pattern[i]
                                elif is_int(selected_text_pattern[i]):
                                    number_str = number_str + selected_text_pattern[i]
                                i = i + 1
                            if number_str != '' and current_operation != '':
                                if current_operation == '+':
                                    current_number = current_number + int(number_str)
                                elif current_operation == '-':
                                    current_number = current_number - int(number_str)
                                elif current_operation == '*':
                                    current_number = current_number * int(number_str)
                                elif current_operation == '/':
                                    current_number = current_number / int(number_str)
                            new_text = new_text + str(current_number)
                            i = i + 1
                        else:
                            new_text = new_text + selected_text_pattern[i]
                            i = i + 1
                else:
                    new_text = new_text + selected_text_pattern.replace(replace_string, instance)

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

class OperationCounter(sublime_plugin.TextCommand):
    def run(self, edit):
        current_file = self.view.file_name()

        if current_file is None:
            return

        regions = self.view.sel()
        if len(regions) == 0:
            return

        region = regions[0]

        selected_text = self.view.substr(region)

        total_selected_text = len(selected_text)

        s = 0

        total_operations = 0

        while s < total_selected_text:
            current_char = selected_text[s]
            if current_char == '=':
                total_operations = total_operations + 1
                if selected_text[s+1] == '==':
                    s = s + 1
            elif current_char == '*' or \
                 current_char == '/' or \
                 current_char == '+' or \
                 current_char == '-':
                total_operations = total_operations + 1

            s = s + 1

        popup_text = "<b>Total operations:</b> " + str(total_operations)
        self.view.show_popup(popup_text)
        # print('Total operations - ' + str(total_operations))

class OpenPathInFinder(sublime_plugin.TextCommand):
    def run(self, edit):
        current_file = self.view.file_name()

        if current_file is None:
            return

        current_path = os.path.dirname(current_file)

        open_in_terminal_cmd = 'open "' + current_path + '"'
        subprocess.check_output(open_in_terminal_cmd, shell=True)

class OpenProjectInFinder(sublime_plugin.TextCommand):
    def run(self, edit):
        folders = self.view.window().folders()

        open_in_terminal_cmd = 'open "' + folders[0] + '"'
        subprocess.check_output(open_in_terminal_cmd, shell=True)

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        pass

    return False

class RepeatTool(sublime_plugin.TextCommand):
    def run(self, edit):

        repeat_time = sublime.get_clipboard()

        if not is_int(repeat_time):
            return

        repeat_time = int(repeat_time)

        for region in self.view.sel():
            selected_text = self.view.substr(region)

            repeat_text = ""

            for i in range(0, repeat_time):
                repeat_text = repeat_text + selected_text

            self.view.replace(edit, region, repeat_text)

class RunTerminalCommandInsideSublime(sublime_plugin.TextCommand):
    def run(self, edit):
        current_file = self.view.file_name()

        for region in self.view.sel():
            selected_text = self.view.substr(region)

            ibash_exe = "/usr/local/bin/interactive_bash"

            if not os.path.exists(ibash_exe):
                ibash_create_cmd = "echo '#!/bin/bash' >> " + ibash_exe + \
                    " &&    echo '/bin/bash -i \"$@\"' >> " \
                    + ibash_exe + " && chmod +x " + ibash_exe
                print(ibash_create_cmd)
                ibash_create_output = subprocess.check_output(ibash_create_cmd, shell=True)
                ibash_create_output = ibash_create_output.strip()
                print(ibash_create_output)

            subprocess_cmd = selected_text

            if current_file is not None and os.path.exists(current_file):
                current_path = os.path.dirname(current_file)
                subprocess_cmd = "cd '" + current_path + "' && " + subprocess_cmd

            print(subprocess_cmd)
            subprocess_output = subprocess.check_output(subprocess_cmd, shell=True, executable=ibash_exe)
            subprocess_output = subprocess_output.decode("utf8")
            subprocess_output = subprocess_output.strip()
            print("Output: " + subprocess_output)

            self.view.replace(edit, region, subprocess_output)