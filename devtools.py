import sublime_plugin
import sublime

import subprocess
import os


class ConvertToSnakeFromCamelCaseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            selected_text = self.view.substr(region)

            new_text = ""

            for s in selected_text:
                if s.isupper():
                    if new_text != "":
                        new_text += "_" + s.lower()
                    else:
                        new_text += s.lower()
                else:
                    new_text += s

            self.view.replace(edit, region, new_text)


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

        if repl_pattern_str not in current_clipboard:
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


class InvertLines(sublime_plugin.TextCommand):
    def run(self, edit):

        for region in self.view.sel():
            selected_text = self.view.substr(region)

            selected_text_lines = selected_text.split("\n")
            selected_text_lines = selected_text_lines[::-1]

            new_text = ""
            for line in selected_text_lines:
                new_text += line + "\n"

            self.view.replace(edit, region, new_text)


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

        print("SmartReplaceFromClipboard - using replace_format: " + str(replace_format))
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


smart_symbol = "%LV%"


class InsertSmartValueSymbol(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.replace(edit, self.view.sel()[0], smart_symbol)


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

            for i in range(number_1, number_2 + 1):
                instances_values.append(str(i))

        elif instances[0] == '{' and instances[len(instances) - 1] == '}':
            instances_values = instances[1:len(instances) - 1].split(',')
        else:
            return

        replace_string = smart_symbol

        index = 0
        for region in self.view.sel():
            selected_text_pattern = self.view.substr(region)

            new_text = ''

            if len(self.view.sel()) == len(instances):
                instance = instances[index]
                index += 1

                if is_int(instance):
                    i = 0
                    while i < len(selected_text_pattern):
                        if i < len(selected_text_pattern) - 4 and selected_text_pattern[i:i + 3] == '%LV':
                            current_number = int(instance)
                            current_operation = ''
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

                continue

            for instance in instances_values:
                if is_int(instance):
                    i = 0
                    while i < len(selected_text_pattern):
                        if i < len(selected_text_pattern) - 4 and selected_text_pattern[i:i + 3] == '%LV':
                            current_number = int(instance)
                            current_operation = ''
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
                if selected_text[s + 1] == '==':
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


def run_terminal_command(cmd_obj, cmd_txt):
    ibash_exe = "/usr/local/bin/interactive_bash"

    current_file = cmd_obj.view.file_name()

    if not os.path.exists(ibash_exe):
        ibash_create_cmd = "echo '#!/bin/bash' >> " + ibash_exe + \
            " &&    echo '/bin/bash -i \"$@\"' >> " \
            + ibash_exe + " && chmod +x " + ibash_exe
        print(ibash_create_cmd)
        ibash_create_output = subprocess.check_output(ibash_create_cmd, shell=True)
        ibash_create_output = ibash_create_output.strip()
        print(ibash_create_output)

    subprocess_cmd = cmd_txt

    folders = cmd_obj.view.window().folders()
    if folders is not None and len(folders) > 0:
        if '$SBTPROJ' in subprocess_cmd:
            subprocess_cmd = subprocess_cmd.replace('$SBTPROJ', folders[0])

    if current_file is not None and os.path.exists(current_file):
        current_path = os.path.dirname(current_file)
        subprocess_cmd = "cd '" + current_path + "' && " + subprocess_cmd

        if '$FILE' in subprocess_cmd:
            subprocess_cmd = subprocess_cmd.replace('$FILE', current_file)
        if '$CURDIR' in subprocess_cmd:
            subprocess_cmd = subprocess_cmd.replace('$CURDIR', current_path)
    else:
        if folders is not None and len(folders) > 0:
            subprocess_cmd = "cd '" + folders[0] + "' && " + subprocess_cmd

    print(subprocess_cmd)
    subprocess_output = subprocess.check_output(subprocess_cmd, shell=True, executable=ibash_exe)
    subprocess_output = subprocess_output.decode("utf8")
    subprocess_output = subprocess_output.strip()
    print("Output: " + subprocess_output)

    return subprocess_output


class RunTerminalCommandInsideSublime(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            selected_text = self.view.substr(region)

            terminal_output = run_terminal_command(self, selected_text)

            self.view.replace(edit, region, terminal_output)


class RunTerminalCommandInsideSublimeBuffer(sublime_plugin.TextCommand):
    def run(self, edit):

        for region in self.view.sel():
            selected_text = self.view.substr(region)

            terminal_output = run_terminal_command(self, selected_text)

            scratch_file = self.view.window().new_file()
            scratch_file.set_name('Command Output')
            scratch_file.set_scratch(True)
            args = {
                'contents': terminal_output
            }
            scratch_file.run_command('insert_snippet', args)
            scratch_file.set_read_only(True)
            scratch_file.settings().set('word_wrap', True)


class RunPythonOnText(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            selected_text = self.view.substr(region)

            python_cmd = sublime.get_clipboard()

            cmd_output = ''

            if python_cmd and 's' in python_cmd:
                try:
                    python_cmd += "\nwith open('/tmp/tmp_sublime_buffer', 'w') as f:\n\tf.write(str(s))"

                    print("RunPythonOnText: " + python_cmd)

                    s = selected_text
                    exec(python_cmd)

                    with open('/tmp/tmp_sublime_buffer', 'r') as f:
                        cmd_output_from_file = f.readlines()

                    cmd_output = cmd_output_from_file[0]
                except Exception as exception:
                    cmd_output = eval(selected_text)
            elif selected_text:
                cmd_output = eval(selected_text)

            cmd_output = str(cmd_output)

            print("RunPythonOnText: " + cmd_output)

            self.view.replace(edit, region, cmd_output)


def get_python_module(python_file):
    module_name = os.path.basename(python_file).replace('.py', '')

    folders = python_file.split('/')

    for i in range(1, len(folders)):
        current_folder = folders[-(i + 1)]
        folder_path = "/".join(folders[:-i])

        possible_init_path = os.path.join(folder_path, '__init__.py')
        print('Testing folder %s' % (possible_init_path,))

        if os.path.exists(possible_init_path):
            module_name = current_folder + "." + module_name
        else:
            break
    return module_name


class PrintFuncLog(sublime_plugin.TextCommand):
    def get_current_scope(self, view, target_scope_type):
        sel = view.sel()[0]
        functionRegs = view.find_by_selector(target_scope_type)
        cf = None
        for r in reversed(functionRegs):
            if r.a < sel.a:
                cf = view.substr(r)
                break

        return cf

    def run(self, edit):
        print("PrintFuncLog::run")

        current_file = self.view.file_name()
        if current_file is None:
            return

        regions = self.view.sel()
        if len(regions) <= 0:
            return

        class_name = self.get_current_scope(self.view, 'entity.name.class')
        function_name = self.get_current_scope(self.view, 'entity.name.function')

        if class_name is None:
            debug_name = function_name
        else:
            debug_name = class_name + ":" + function_name

        print("PrintFuncLog: " + str(debug_name))

        target_region = regions[0]
        target_vars = []

        if len(regions) > 1:
            for i in range(0, len(regions)):
                region = regions[i]
                selected_text = self.view.substr(region)
                if selected_text == '':
                    target_region = region
                else:
                    target_vars.append(selected_text)

        debug_statement = ""
        if current_file.endswith(".py"):
            module_name = get_python_module(current_file)
            if len(target_vars) > 0:
                debug_statement = "print('[%s] %s -'" % (module_name, debug_name)
                for variable in target_vars:
                    debug_statement += " + ' %s - ' + str(%s)" % (variable, variable)
                debug_statement += ')'
            else:
                debug_statement = "print('[%s] %s')" % (module_name, debug_name)
        elif current_file.endswith(".cs"):
            if len(target_vars) > 0:
                debug_statement = "Debug.Log($\"%s " % (debug_name)
                for variable in target_vars:
                    debug_statement += "| %s - {%s} " % (variable, variable)
                debug_statement += '\");'
            else:
                debug_statement = 'Debug.Log("%s");' % (debug_name,)
        self.view.replace(edit, target_region, debug_statement)


class GetPythonFullModuleName(sublime_plugin.TextCommand):
    def run(self, edit):
        current_file = self.view.file_name()

        if not current_file or not current_file.endswith('.py'):
            return

        module_name = get_python_module(current_file)

        sublime.set_clipboard(module_name)
