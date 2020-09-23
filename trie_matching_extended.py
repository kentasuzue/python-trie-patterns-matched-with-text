# python3
import sys
import heapq
PATTERN_END = '$'


def make_trie(patterns):
	trie = dict()
	cur_pos = 0
	trie[cur_pos] = dict()

	for pattern in patterns:
		cur_pos = 0
		for symbol in pattern:
			if symbol in trie[cur_pos]:
				cur_pos = trie[cur_pos][symbol]
			else:
				new_pos = len(trie)
				trie[cur_pos][symbol] = new_pos
				trie[new_pos] = dict()
				cur_pos = new_pos
		if PATTERN_END not in trie[cur_pos]:
			new_pos = len(trie)
			trie[cur_pos][PATTERN_END] = new_pos
			trie[new_pos] = len(pattern)
			# did not bother to create ending node to terminate ending edge
	return trie


def trieMatching(text, textStartPos, trie, textStartHeap):
	textIndex = textStartPos
	# print(f"text[{textStartPos}:]={text[textStartPos:]}")
	trieIndex = 0
	while True:
		# print(f"textIndex={textIndex} text[textIndex]={text[textIndex:]} trieIndex={trieIndex} trie[trieIndex]={trie[trieIndex]}")
		if PATTERN_END in trie[trieIndex]:
			pattern_length = trie[trie[trieIndex][PATTERN_END]]
			# print(f"pattern_length={pattern_length}")
			heapq.heappush(textStartHeap, textIndex - pattern_length)
			# print(f"textStartHeap={textStartHeap}")
			return
		elif textIndex < len(text) and text[textIndex] in trie[trieIndex]:
			nextTrieIndex = trie[trieIndex][text[textIndex]]
			textIndex += 1
			trieIndex = nextTrieIndex
		else:
			return


def prefixTrieMatching(text, trie):
	textStartHeap = []
	for textStartPos in range(len(text)):
		trieMatching(text, textStartPos, trie, textStartHeap)
	# print(textStartHeap)
	return textStartHeap


def solve(text, n, patterns):
	trie = make_trie(patterns)
	# print(trie)
	text_start_heap = prefixTrieMatching(text, trie)
	result = []

	while text_start_heap:
		result.append(heapq.heappop(text_start_heap))
		# empty heap into result

	return result

if __name__ == '__main__':
	text = sys.stdin.readline().strip()
	n = int(sys.stdin.readline().strip())
	patterns = []
	for i in range(n):
		patterns += [sys.stdin.readline().strip()]

	ans = solve(text, n, patterns)

	sys.stdout.write(' '.join(map(str, ans)) + '\n')
