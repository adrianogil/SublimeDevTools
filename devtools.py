import sublime, sublime_plugin

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
            valid_content_between_newlines = True
            for s in selected_text:
                replace_text = replace_text + s
                if s == '\n':
                    print("AutomatedNumberedDebugCommand - Identified newline")
                    if valid_content_between_newlines:
                        current_debug = current_clipboard.replace(repl_pattern_str, str(n_debug))
                        n_debug = n_debug + 1
                        replace_text = replace_text + current_debug + '\n'
                        valid_content_between_newlines = False
                elif s != ' ' or s != '\t':
                    valid_content_between_newlines = True
                
            self.view.replace(edit, region, replace_text)