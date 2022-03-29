import sublime
import sublime_plugin
import os
import subprocess
import json
import re

cached_dir_results = {}

class DprintFmtCommand(sublime_plugin.TextCommand):
	def description(self):
		return "Formats source code using dprint."

	def run(self, edit):
		try:
			file_path = self.view.file_name()
			if file_path is not None:
				extension = os.path.splitext(file_path)[1].replace(".", "")
				dir_path = os.path.dirname(file_path)
				if dir_path in cached_dir_results:
					extensions = cached_dir_results[dir_path]
				else:
					plugin_infos = dprint_exec.get_plugin_infos(dir_path)
					extensions = [file_ext for plugin_info in plugin_infos for file_ext in plugin_info["fileExtensions"]]
					cached_dir_results[dir_path] = extensions

				if extension in extensions:
					file_region = sublime.Region(0, self.view.size())
					file_text = self.view.substr(file_region)
					formatted_text = dprint_exec.format_text(dir_path, file_path, file_text)

					if file_text != formatted_text:
						self.view.replace(edit, file_region, formatted_text)
						print("dprint: Formatted " + file_path)

		except Exception as err:
			print("dprint: " + str(err))

class EventListener(sublime_plugin.EventListener):
	def on_pre_save(self, view):
		view.run_command("dprint_fmt")

class DprintExec:
	def get_plugin_infos(self, dir_path):
		expected_schema_version = 4
		json_text = subprocess.check_output(["dprint", "editor-info"], cwd=dir_path).decode("utf8")
		editor_info = json.loads(json_text)

		if editor_info["schemaVersion"] != expected_schema_version:
			if editor_info["schemaVersion"] > expected_schema_version:
				raise Exception("Please upgrade your editor extension to be compatible with the installed version of dprint.")
			else:
				raise Exception("Your installed version of dprint is out of date. Please update it.")

		return editor_info["plugins"]

	def format_text(self, dir_path, file_path, file_text):
		from subprocess import Popen, PIPE

		p = Popen(["dprint", "fmt", "--stdin", os.path.basename(file_path)],
			stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=dir_path)
		stdout, stderr = p.communicate(bytes(file_text, "utf8"))

		if p.returncode == 0:
			return stdout.decode("utf8")
		else:
			raise Exception("Error formatting: " + stderr.decode("utf8"))

dprint_exec = DprintExec()

