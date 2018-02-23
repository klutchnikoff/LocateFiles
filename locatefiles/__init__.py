from fman import DirectoryPaneCommand, show_alert
from fman import PLATFORM
from fman import show_quicksearch, QuicksearchItem

from fman.url import basename, dirname, as_url
from subprocess import run, PIPE

class LocateFiles(DirectoryPaneCommand):

	def __call__(self):
		result = show_quicksearch(self._get_items)
		if result:
			query, value = result
			value = value.decode("utf-8")
			value = as_url(value)
			self.pane.set_path(dirname(value))
			#self.pane.place_cursor_at(value)
		else:
			return

	def _get_items(self, query):
		located_files = run(self._locate(query), stdout=PIPE)
		located_files = located_files.stdout.split()
		for filep in located_files:
			yield QuicksearchItem(filep)

	def _locate(self, query):
		if PLATFORM == 'Linux':
			return ['/usr/bin/locate', '-l10', query]
		#elif PLATFORM == 'Mac':
		#	return ['/usr/bin/mdfind', '-name ', query]
		raise NotImplementedError(PLATFORM)
