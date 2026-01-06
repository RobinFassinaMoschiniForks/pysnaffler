import codecs
from pysnaffler.rules.rule import SnaffleRule
from pysnaffler.rules.constants import EnumerationScope, MatchAction, MatchLoc, MatchListType, Triage
from typing import List, Union

class SnafflerContentsEnumerationRule(SnaffleRule):
	def __init__(self, enumerationScope:EnumerationScope, ruleName:str, matchAction:MatchAction, relayTargets:List[str], description:str, matchLocation:MatchLoc, wordListType:MatchListType, matchLength:int, wordList:List[str], triage:Triage):
		super().__init__(enumerationScope, ruleName, matchAction, relayTargets, description, matchLocation, wordListType, matchLength, wordList, triage)
	
	def match(self, data:Union[str, bytes], chars_before:int = 100, chars_after:int = 100):
		matches = []
		for rex in self.wordList:
			for match in rex.finditer(data):
				text = match.group(0)
				if chars_before > 0:
					text = data[max(match.start() - chars_before, 0) : match.start()] + text
				if chars_after > 0:
					text += data[match.end() : min(match.end() + chars_after, len(data))]
				matches.append(text)
		return '\r\n'.join(matches)

	def open_and_match(self, filename:str, chars_before:int = 100, chars_after:int = 100):
		try:
			if self.matchLocation == MatchLoc.FileContentAsString:
				with codecs.open(filename, 'r', 'latin-1') as f:
					data = f.read()
					return self.match(data, chars_before, chars_after), None
			elif self.matchLocation == MatchLoc.FileContentAsBytes:
				with open(filename, 'rb') as f:
					data = f.read()
					return self.match(data, chars_before, chars_after), None
			else:
				return False, Exception('ERROR: Unknown match location: %s' % self.matchLocation)
		except Exception as e:
			return False, e

	def determine_action(self, data, **kwargs):
		pass