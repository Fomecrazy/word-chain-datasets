import os;
import random;

datasetDir = "refactoredDatasets"
groups = []

for root, dirs, files in os.walk(datasetDir):
	for file in files:
		category = root.split("\\")[1]
		name = os.path.splitext(file)[0]

		groups.append(f"{category}/{name}")
		

allowedGroups = {
    # Adjectives
    "adjectives/general": ["nouns/objects", "nouns/animals", "nouns/foods"],
    "adjectives/emotional": ["nouns/abstract", "nouns/animals", "feelings/positive", "feelings/negative"],
    "adjectives/descriptive": ["nouns/objects", "nouns/foods", "nouns/animals"],

    # Nouns
    "nouns/objects": ["verbs/physical", "places/outdoor", "places/indoor"],
    "nouns/animals": ["verbs/physical", "verbs/abstract", "nouns/abstract"],
    "nouns/foods": ["verbs/physical", "verbs/abstract"],
    "nouns/abstract": ["verbs/abstract", "adjectives/emotional"],

    # Verbs
    "verbs/physical": ["nouns/objects", "nouns/animals", "places/outdoor", "places/indoor"],
    "verbs/abstract": ["nouns/abstract", "feelings/positive", "feelings/negative"],
    "verbs/creative": ["nouns/objects", "nouns/abstract"],

    # Places
    "places/outdoor": ["verbs/physical", "nouns/objects", "nouns/animals"],
    "places/indoor": ["verbs/physical", "nouns/objects", "nouns/abstract"],
    "places/fantasy": ["verbs/creative", "nouns/abstract"],

    # Feelings
    "feelings/positive": ["adjectives/emotional", "nouns/abstract", "verbs/abstract"],
    "feelings/neutral": ["adjectives/general", "nouns/abstract", "verbs/abstract"],
    "feelings/negative": ["adjectives/emotional", "verbs/abstract", "nouns/abstract"]
}

groupedWords = {}
wordToGroup = {}

for group in groups:
	category, name = group.split("/")

	if not allowedGroups[group] or len(allowedGroups[group]) == 0:
		print(f"Group {group} has no groups to chain to!")

	file_path = os.path.join(f"{datasetDir}/{category}", f"{name}.txt")
	with open(file_path, "r", encoding="utf-8") as f:
		groupedWords[group] = [line.strip() for line in f if line.strip()]
		
for group, words in groupedWords.items():
	for word in words:
		wordToGroup[word] = group

chains = {}
phrases = set()
total = 0
test = ""

for word in wordToGroup:
	group = wordToGroup[word]
	ag = allowedGroups[group]

	candidates = []
	chosen = []
	for g in ag:
		candidates += groupedWords[g]
	
	for c in candidates:
		phrase = f"{word} {c}"
		if phrase in phrases:
			continue

		phrases.add(phrase)
		chosen.append(c)

	total += len(candidates)
	chains[word] = candidates # random.sample(chosen)

	for link in chains[word]:
		test += f"{word} {link} \n"

with open("test.txt", "w") as f:
	f.write(test)

print(chains, total)