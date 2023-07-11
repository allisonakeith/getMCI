import spacy
import random
import pandas as pd
from statistics import mean
from nltk.stem import SnowballStemmer

# I'm using nltk's SnowballStemmer for German because it is better at printing the root of the word than spacy's lemmatizer
stemmer = SnowballStemmer('german')

nlp = spacy.load("de_core_news_md")


def within_subset_variety(samples):
    within_subset_varieties = []
    # calculate the number of unique forms in each sample
    for sample in samples:
        within_subset_variety = len(set(sample))
        within_subset_varieties.append(within_subset_variety)
    wsv = mean(within_subset_varieties)
    # print("the within subset variety is: ", wsv)
    return wsv


def between_subset_diversity(samples):
    symmetric_differences = []
    # Iterate through every possible pair of samples
    for i in range(len(samples)):
        for j in range(i + 1, len(samples)):
            list1 = set(samples[i])
            list2 = set(samples[j])
            # Calculate the symmetric difference between the two lists
            symmetric_diff = len(list1.symmetric_difference(list2))
            # Append the symmetric difference to the list of symmetric differences so that the mean can be calculated
            symmetric_differences.append(symmetric_diff)
    bsv = mean(symmetric_differences)
    # print("the Between Subset Diversity is: ", bsv)
    return bsv


def compute_MCI(forms):
    samples = []
    if len(forms) >= 10:
        for i in range(100):
            sample = random.sample(forms, 10)
            samples.append(sample)
            # print(samples)
        wsv = within_subset_variety(samples)
        bsv = between_subset_diversity(samples)
    else:
        for i in range(100):
            sample = random.sample(forms, (len(forms) - 1))
            samples.append(sample)
        wsv = within_subset_variety(samples)
        bsv = between_subset_diversity(samples)
    MCI = wsv + (bsv / 2) - 1
    return MCI


def MCI(text):
    verbs = []
    nouns = []
    lemmas = []
    doc = nlp(text.lower())
    for token in doc:
        if token.pos_ == "NOUN":
            stem = stemmer.stem(token.text)
            lemmas.append(stem.lower())
            if stem.lower() == token.text:
                inflection = "Ø"

            if stem.lower() != token.text:
                inflection = token.text.replace(stem.lower(), "")
            nouns.append(inflection)

        if token.pos_ == "VERB" or token.pos_ == "AUX":
            if token.lemma_ == token.text:
                inflection = "Ø"

            if token.lemma_ != token.text:
                inflection = token.text.replace(token.lemma_, "")
            verbs.append(inflection)

    # print(lemmas)
    # print(nouns)
    # print(verbs)

    N_MCI = compute_MCI(nouns)
    V_MCI = compute_MCI(verbs)

    return (N_MCI, V_MCI)


# text = "Die eigentlichen Hauptsprachen sind English, Frazösisch, und Spanisch. Jedoch finde ich es sehr wichtig und angebracht auch Deutsch zu studieren. Es gibt einige Bücher, Gedichte und Stücke die zwar in anderen Sprachen übersetzt werden, jedoch ist der deutscher Stil von grosser Bedeutung. Falls man solche wundervolle Kunstwerke in einer anderen Sprache liest, wird es einen ganz anderen Eindruck auf den Lesen haben. Auch in anderen Bereichen ist Deutsch notwendig und manchmal gar unerlässlich. Wenn man zum Beispiel Deutschland oder Österreich wohnt ist das Beherrschen von der deutschen Sprache ein Muss. Wie soll man ohne vollständige Deutschkenntnisse eine gut bezahlte Arbeit finden?"
# nmci, vmci = MCI(text)
# print("German C2 MCI")
# print(f"NounMCI: {nmci}\nVerbMCI: {vmci}\n")


df = pd.read_csv('MERLIN.csv', encoding='utf-8')
# Create new columns for NounMCI and VerbMCI

# Loop through each row in the dataframe and compute the MCI for the text
for index, row in df.iterrows():
    text = row['Text']
    nmci, vmci = MCI(text)

    # Update the NounMCI and VerbMCI values in the dataframe
    df.loc[index, 'N_MCI'] = nmci
    df.loc[index, 'V_MCI'] = vmci

    # print(f"NounMCI: {nmci}\nVerbMCI: {vmci}\n")

# Write the updated dataframe to CSV
df.to_csv('MERLIN.csv', encoding='utf-8', index=False)

df = pd.read_csv('MERLIN_GROUPED.csv', encoding='utf-8')
texts = df['Learner text'].tolist()
for x in texts:
    x = x[:54097]
    print("The text is:", len(x), "characters long")
    nmci, vmci = MCI(x)
    print("GERMAN GROUPED MCI")
    print(f"Text: \nNounMCI: {nmci}\nVerbMCI: {vmci}\n")
