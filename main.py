# using regex to extract knowledge triplets (entity/relation/entity)
# from limited, predictable aristotelian syllogisms

import re

text = "Every human is mortal\nEvery Socrates is human\nEvery Socrates is mortal"
# Step 1: Regex extraction.

universal_affirmation = re.compile(r'^Every (\w+) is (\w+)$')
particular_affirmation = re.compile(r'^Some (\w+) is (\w+)$')
universal_denial = re.compile(r'^No (\w+) is (\w+)$')
particular_denial = re.compile(r'^Not every (\w+) is (\w+)$')

lines = text.split('\n')

matches = []

for line in lines:
    match = universal_affirmation.match(line)
    if match:
        matches.append((match.group(1), 'UA', match.group(2)))
    else:
        match = particular_affirmation.match(line)
        if match:
            matches.append((match.group(1), 'PA', match.group(2)))
        else:
            match = universal_denial.match(line)
            if match:
                matches.append((match.group(1), 'UD', match.group(2)))
            else:
                match = particular_denial.match(line)
                if match:
                    matches.append((match.group(1), 'PD', match.group(2)))

# Step 2: Porter stemmer

from nltk.stem import PorterStemmer
ps = PorterStemmer()

vocab = set() 

for i in range(len(matches)):
    matches[i]=(ps.stem(matches[i][0]), matches[i][1], ps.stem(matches[i][2]))
    vocab.add(matches[i][0])
    vocab.add(matches[i][2])
print(vocab)

# Step 3: Matches to Graph

vocab = list(vocab)
graph = [['']*len(vocab) for _ in range(len(vocab))]
for match in matches:
    graph[vocab.index(match[0])][vocab.index(match[2])]=match[1]+">"
    graph[vocab.index(match[2])][vocab.index(match[0])]=match[1]+"<"



# Step 4: Visualization
for word in vocab:
    print(word, end = " ")
print()
for row in graph:
    print(str(row)+" "+str(vocab[graph.index(row)]))

# Step 5: Reasoning

#reason through the graph
