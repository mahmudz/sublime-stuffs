import sublime
import sublime_plugin
import re


class AssetingSourceCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		def on_done(input_string):
			self.view.run_command( 'asseting_source_helper', { 'location' : input_string } )


		def on_change(input_string):
			pass

		def on_cancel():
			print("User cancelled the input")
					
		window = self.view.window()
		window.show_input_panel("Text to Insert:", "", on_done, on_change, on_cancel)		
	

class AssetingSourceHelperCommand(sublime_plugin.TextCommand):
	def run(self, edit, location = ''):
		reg = sublime.Region(0, self.view.size())
		content = self.view.substr(reg)
		
		links = re.findall(r'<link\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1', content)
		for link in links:
		  content = content.replace(link[1], "{{ asset('" + location + "/" + link[1] +"') }}")

		links = re.findall(r'<script\s+(?:[^>]*?\s+)?src=(["\'])(.*?)\1', content)
		for link in links:
		  content = content.replace(link[1], "{{ asset('" + location + "/" + link[1] +"') }}")

		links = re.findall(r"\<img.+src\=(?:\"|\')(.+?)(?:\"|\')(?:.+?)\>", content)
		for link in links:
		  content = content.replace(link, "{{ asset('" + location + "/" + link +"') }}")

		content = content.replace("{{ asset('"+location+"/{{", "{{")
		content = content.replace("}}') }}", "}}")
		content = content.replace("{{ asset('"+location+"/{{ asset('"+location+"/{{", "{{")
		content = content.replace("}}') }}') }}", "}}")

		
		self.view.erase(edit, reg)
		self.view.insert(edit, 0, content)
		
