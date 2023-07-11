import spacy
import random
import pandas as pd
from statistics import mean
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

# I'm using nltk's SnowballStemmer for Spanish because it is better at printing the root verb of the word than spacy's lemmatizer

stemmer = SnowballStemmer('german')

nlp = spacy.load("es_core_news_sm")


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
    doc = nlp(text.lower())
    for token in doc:
        if token.pos_ == "NOUN":

            if token.lemma_ == token.text:
                inflection = "Ø"

            elif token.lemma_ != token.text:
                inflection = token.text.replace(token.lemma_, "")

            nouns.append(inflection)
            # print("text: ", token.text, "root: ",
            #       token.lemma_, "inflection: ", inflection)

        elif token.pos_ == "VERB" or token.pos_ == "AUX":
            if token.lemma_ == "ser" and token.text[0] != token.lemma_[0]:
                inflection = token.text
            elif token.lemma_ == "ir" and token.text[0] != token.lemma_[0]:
                inflection = token.text
            elif token.lemma_ == token.text:
                inflection = "Ø"

            elif token.lemma_ != token.text:

                inflection = token.text.replace(token.lemma_[:-2], "")

            verbs.append(inflection)
            # print("text: ", token.text, "root: ",
            #       token.lemma_, "inflection: ", inflection)

    # print(nouns)
    # print(verbs[:20])

    N_MCI = compute_MCI(nouns)
    V_MCI = compute_MCI(verbs)

    return (N_MCI, V_MCI)


# df = pd.read_csv('CEDEL2_min_length.csv', encoding='utf-8')
# # Create new columns for NounMCI and VerbMCI
# df['NounMCI'] = 0.0
# df['VerbMCI'] = 0.0

# # Loop through each row in the dataframe and compute the MCI for the text
# for index, row in df.iterrows():
#     text = row['Text']
#     nmci, vmci = MCI(text)

#     # Update the NounMCI and VerbMCI values in the dataframe
#     df.loc[index, 'N_MCI'] = nmci
#     df.loc[index, 'V_MCI'] = vmci

#     # print(f"Text: {text}\nNounMCI: {nmci}\nVerbMCI: {vmci}\n")

# # Write the updated dataframe to CSV
# df.to_csv('CEDEL2.csv', encoding='utf-8', index=False)

# now get MCI for grouped texts and print in console

# df = pd.read_csv('CEDEL2_GROUPED.csv', encoding='utf-8')
# texts = df['Learner text'].tolist()
# for x in texts:
#     x = x[:54000]
#     print("The text is:", len(x), "characters long")
#     nmci, vmci = MCI(x)
#     print("SPANISH GROUPED MCI")
#     print(f"NounMCI: {nmci}\nVerbMCI: {vmci}\n")
