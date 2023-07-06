import pathlib

import pandas
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess

data_name = 'JEOPARDY_CSV.csv'
bot_name = 'Ken Jennings'
model_name = 'JEOPARDY_CSV.model'

df = pandas.read_csv(data_name)
question_field = df.columns[5]
answer_field = df.columns[6]

print(f"Hello! I'm {bot_name}, a question answering bot who knows answers to all questions from the 'Jeopardy!' game.")

if not pathlib.Path(model_name).is_file():
    train_corpus = [
        TaggedDocument(simple_preprocess(question), [number])
        for number, question in enumerate(df[question_field])
    ]
    model = Doc2Vec(vector_size=124,
                    min_count=1,
                    epochs=40,
                    hs=1,
                    dbow_words=1)
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    model.save(model_name)
else:
    model = Doc2Vec.load(model_name)

while True:
    print('Ask me something!')
    question = input()
    print("Let's play!")
    response = model.dv.most_similar([model.infer_vector(simple_preprocess(question))], topn=1)
    question_number = response[0][0]
    question_certainty = round(response[0][1] * 100)
    print(f"I know this question: its number is {question_number}. I'm {question_certainty}% sure of this.")
    print(f'The answer is {df.loc[question_number, answer_field]}')
    print('Do you want to ask me again? (yes/no)')
    if input().casefold() == 'no':
        break

print('It was nice to play with you! Goodbye!')
