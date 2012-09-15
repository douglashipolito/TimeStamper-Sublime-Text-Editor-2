import sublime, sublime_plugin, datetime, re

class TimeStamper(sublime_plugin.EventListener):        

    def on_pre_save(self, view):

        if not view.is_dirty():
            return

        self.settings = sublime.load_settings("TimeStamper.sublime-settings")
        timestamp_str = datetime.datetime.now().strftime("/* %Y%m%d-%H%M */")
        edit = view.begin_edit()

        acceptedPath = False
        acceptedExtension = False

        #Test if Path Accepted
        for path in self.settings.get('accepted_paths'):
            if path == '*':
                acceptedPath = True
                break
            rgPath = re.compile(path, re.IGNORECASE|re.DOTALL)
            rPath = rgPath.search(view.file_name())
            if rPath:
                acceptedPath = True
                break
        
        #Is Not Accepted Path
        if not acceptedPath:
           return ''

        #
        for ext in self .settings.get('accepted_extensions'):
            if view.file_name().endswith('.' + ext):
                acceptedExtension = True
                break

        #Test if File Extension Accepted
        if acceptedExtension:

            #Regex for verify Exists TimeStamp
            sTimeStamp = '(\\/\\*[\\d\\D]*?\\*\\/)'
            rg = re.compile(sTimeStamp, re.IGNORECASE|re.DOTALL)
            m = rg.search(view.substr(view.line(0)))

            #Exists, Replace this
            if m:
                #Regex Blank Spaces after TimeStamp
                rgSpaces = view.find(sTimeStamp + "+(\\n)",0)
                erSpaces = re.search('(\\n\\n)', view.substr(view.full_line(rgSpaces)))
                
                #No Blank Spaces, Add Blank Space before TimeStamp
                if erSpaces is None:
                    timestamp_str = timestamp_str + "\n"
                #Replace    
                view.replace(edit, view.line(0), timestamp_str)
            else:
                #Add
                view.insert(edit, 0, timestamp_str + "\n\n")
        
        
        view.end_edit(edit)
