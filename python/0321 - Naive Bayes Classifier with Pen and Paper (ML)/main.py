import pandas as pd

words = ['a', 'besnerende', 'hakkuna', 'hakuna', 'magnifique', 'mais', 'matata',
         'ord', 'phrase', 'quelle', 'to', 'what', 'wonderful']

sent = [['hakuna', 'matata', 'what', 'a', 'wonderful', 'phrase', 'hakuna', 'matata'],
        ['hakkuna', 'matata', 'to', 'besnerende', 'ord', 'hakkuna', 'matata'],
        ['hakuna', 'matata', 'mais', 'quelle', 'phrase', 'magnifique', 'hakuna', 'matata']]

counts = {word: [text.count(word) for text in sent] for word in words}

df = pd.DataFrame(counts, columns=words, index=['English', 'Norwegian', 'French'])

df = df.add(1)
df['Total'] = df.sum(axis=1)
df.loc['Total'] = df.sum(axis=0)
df = df / df.loc['Total', 'Total']
print(df)