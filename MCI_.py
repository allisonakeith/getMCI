import spacy
import random
import pandas as pd
from statistics import mean

nlp = spacy.load("en_core_web_sm")


def within_subset_variety(samples):
    within_subset_varieties = []
    # calculate the number of unique forms in each sample
    for sample in samples:
        within_subset_variety = len(set(sample))
        within_subset_varieties.append(within_subset_variety)
    wsv = mean(within_subset_varieties)
    print("the within subset variety is: ", wsv)
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
    print("the Between Subset Diversity is: ", bsv)
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

                nouns.append(inflection)
            if token.lemma_ != token.text:
                inflection = token.text.replace(token.lemma_, "")
                nouns.append(inflection)
            # print("text: ", token.text, "root: ",
            #       token.lemma_, "inflection: ", inflection)

        if token.pos_ == "VERB" or token.pos_ == "AUX":
            if token.lemma_ == token.text:
                inflection = "Ø"
                verbs.append(inflection)
            elif token.text.endswith('ed'):
                # print(token.text)
                inflection = "ed"
                verbs.append(inflection)
            elif token.text.endswith('ing'):
                inflection = "ing"
                verbs.append(inflection)
            elif token.lemma_ != token.text:
                inflection = token.text.replace(token.lemma_, "")
                verbs.append(inflection)
            # print("text: ", token.text, "root: ",
            #       token.lemma_, "inflection: ", inflection)

    # print(nouns)
    # print(verbs)

    N_MCI = compute_MCI(nouns)
    V_MCI = compute_MCI(verbs)

    return (N_MCI, V_MCI)


# A1_text = "One day,... uno boy had a one frog and a dog, at night when the boy is sleep the frog scape. At the morning the frog desapear and the boy is worry because the frog is scape. the boy very fast go to the forest and search the frog with his dog. The boy very worry don't find the dog and he cry. He search on the forest' trees, he shout at forest' mountain and the frog don't find. the dog and the boy crying old the night and the dog at night get up the boy and the dog run to the river and the boy run with the dog, and in the river the boy listen the frog and he seacrh the frog. And he find this. The boy and the dog its very funny and they went at home very happy."
# # When the boy climbed on the deer's back looking for the frog it pushed him and his dog of an edge. The puddle of mud they fell in was right next to a fallen tree where they coincidentally found the frog and his whole family. The boy knew he couldn't take all of them and especially not the father, so he decided to take one of the smaller ones to take home with him and raise it."
# B2_text = "Once upon a time a little boy and his dog found a frog. The boy decided to make it their pet by taking it home and putting it into a small glass jar. Every night the boy and the dog were watching the frog until they fell asleep, but one night, when both of them were asleep, the frog managed to escape. When the boy and his dog woke up and noticed that the frog was gone they were desperate and decided to go out into the forest and look for him. After hours of searching all over the forest they still couldn't find the frog. They stepped on rocks, climbed on trees and even got to know other animals living in the forest. One of those animals was a deer."

# nmci, vmci = MCI(A1_text)
# print("ENGLISH A1 MCI")
# print(f"NounMCI: {nmci}\nVerbMCI: {vmci}\n")

# nmci, vmci = MCI(B2_text)
# print("ENGLISH B2 MCI")
# print(f"NounMCI: {nmci}\nVerbMCI: {vmci}\n")

# write results to CORELF file
def write_to_file(text, filename):
    with open(filename, 'a') as f:
        nmci, vmci = MCI(text)
        f.write(f"{nmci}\t{vmci}\n")
