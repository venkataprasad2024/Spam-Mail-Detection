# Importing the libraries.
import os
import re
import numpy as np


# Setting the path of the train files
train_path = "./train"


# Setting the path of the test files
test_path = "./test"


def number_of_allEmails():
    counter = 0
    for directories, subdirectories, files in os.walk(train_path):
        for filename in files:
            counter += 1
    return counter


def number_of_spamEmails():
    counter = 0
    for directories, subdirectories, files in os.walk(train_path):
        for filename in files:
            if "spam" in filename:
                counter += 1
    return counter


def number_of_hamEmails():
    counter = 0
    for directories, subdirectories, files in os.walk(train_path):
        for filename in files:
            if "ham" in filename:
                counter += 1
    return counter


def text_parser(text):
    words = re.split("[^a-zA-Z]", text)
    lower_words = [word.lower() for word in words if len(word) > 0]
    return lower_words


def trainWord_generator():
    all_words = []
    spam_words = []
    ham_words = []

    for directories, subdirectories, files in os.walk(train_path):
        for filename in files:
            full_path = os.path.join(directories, filename)
            with open(full_path, 'r', encoding='latin-1') as target_file:
                data = target_file.read()
                words = text_parser(data)
                for word in words:
                    all_words.append(word)
                    if "ham" in filename:
                        ham_words.append(word)
                    elif "spam" in filename:
                        spam_words.append(word)

    all_words = sorted(all_words)
    spam_words = sorted(spam_words)
    ham_words = sorted(ham_words)

    return all_words, spam_words, ham_words


def unique_words(all_trainWords):
    return sorted(list(set(all_trainWords)))


def frequency_calculator(words):
    wf = {}
    for word in words:
        wf[word] = wf.get(word, 0) + 1
    return wf


def bagOfWords_genarator(all_uniqueWords, spam_trainWords, ham_trainWords):
    spam_bagOfWords = frequency_calculator(spam_trainWords)
    ham_bagOfWords = frequency_calculator(ham_trainWords)

    for word in all_uniqueWords:
        spam_bagOfWords.setdefault(word, 0)
        ham_bagOfWords.setdefault(word, 0)

    return dict(sorted(spam_bagOfWords.items())), dict(sorted(ham_bagOfWords.items()))


def smoothed_bagOfWords(all_uniqueWords, spam_bagOfWords, ham_bagOfWords, delta):
    smoothed_spamBOW = {word: spam_bagOfWords[word] + delta for word in spam_bagOfWords}
    smoothed_hamBOW = {word: ham_bagOfWords[word] + delta for word in ham_bagOfWords}
    return dict(sorted(smoothed_spamBOW.items())), dict(sorted(smoothed_hamBOW.items()))


def spam_probability(nb_of_allEmails, nb_of_spamEmails):
    return nb_of_spamEmails / nb_of_allEmails


def ham_probability(nb_of_allEmails, nb_of_hamEmails):
    return nb_of_hamEmails / nb_of_allEmails


def spam_condProbability(all_uniqueWords, spam_bagOfWords, smoothed_spamBOW, delta):
    total = sum(spam_bagOfWords.values()) + delta * len(all_uniqueWords)
    return {word: smoothed_spamBOW[word] / total for word in smoothed_spamBOW}


def ham_condProbability(all_uniqueWords, ham_bagOfWords, smoothed_hamBOW, delta):
    total = sum(ham_bagOfWords.values()) + delta * len(all_uniqueWords)
    return {word: smoothed_hamBOW[word] / total for word in smoothed_hamBOW}


def model_output_generator(word_numbers, words, ham_wf, ham_cp, spam_wf, spam_cp):
    output = ""
    for i in range(word_numbers):
        w = words[i]
        output += f"{i+1}  {w}  {ham_wf[w]}  {ham_cp[w]}  {spam_wf[w]}  {spam_cp[w]}\n"
    return output


def modelFileBuilder(model_output):
    with open("model.txt", "w", encoding="utf-8") as f:
        f.write(model_output)


def get_testFileNames():
    file_names = []
    for _, _, files in os.walk(test_path):
        file_names.extend(files)
    return file_names


def get_actualLabels():
    labels = []
    for _, _, files in os.walk(test_path):
        for f in files:
            labels.append("ham" if "ham" in f else "spam")
    return labels


def score_calculator(all_uniqueWords, spam_prob, ham_prob, spam_condProb, ham_condProb, delta):
    ham_scores, spam_scores, predicted, decisions = [], [], [], []

    for _, _, files in os.walk(test_path):
        for filename in files:
            label = "ham" if "ham" in filename else "spam"
            path = os.path.join(test_path, filename) if os.path.isdir(test_path) else os.path.join("./test", filename)
            with open(path, 'r', encoding='latin-1') as f:
                words = text_parser(f.read())

            log_spam = np.log(spam_prob)
            log_ham = np.log(ham_prob)
            for w in words:
                if w in all_uniqueWords:
                    log_spam += np.log(spam_condProb.get(w, 1e-10))
                    log_ham += np.log(ham_condProb.get(w, 1e-10))

            spam_scores.append(log_spam)
            ham_scores.append(log_ham)
            pred = "spam" if log_spam > log_ham else "ham"
            predicted.append(pred)
            decisions.append("right" if pred == label else "wrong")

    return ham_scores, spam_scores, predicted, decisions


def result_output_generator(fileNumbers, fileNames, predictedLabels, hamScores, spamScores, actualLabels, decisionLabels):
    output = ""
    for i in range(fileNumbers):
        output += f"{i+1}  {fileNames[i]}  {predictedLabels[i]}  {hamScores[i]}  {spamScores[i]}  {actualLabels[i]}  {decisionLabels[i]}\n"
    return output


def resultFileBuilder(result_output):
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(result_output)


# === All evaluation functions restored ===

def get_spamPrecision(fileNumbers, actualLabels, predictedLabels):
    tp = fp = 0
    for i in range(fileNumbers):
        if actualLabels[i] == "spam" and predictedLabels[i] == "spam":
            tp += 1
        if actualLabels[i] == "ham" and predictedLabels[i] == "spam":
            fp += 1
    return tp / (tp + fp) if (tp + fp) > 0 else 0.0


def get_spamRecall(fileNumbers, actualLabels, predictedLabels):
    tp = fn = 0
    for i in range(fileNumbers):
        if actualLabels[i] == "spam" and predictedLabels[i] == "spam":
            tp += 1
        if actualLabels[i] == "spam" and predictedLabels[i] == "ham":
            fn += 1
    return tp / (tp + fn) if (tp + fn) > 0 else 0.0


def get_spamAccuracy(fileNumbers, actualLabels, predictedLabels):
    tp = tn = fp = fn = 0
    for i in range(fileNumbers):
        if actualLabels[i] == predictedLabels[i] == "spam": tp += 1
        if actualLabels[i] == predictedLabels[i] == "ham": tn += 1
        if actualLabels[i] == "ham" and predictedLabels[i] == "spam": fp += 1
        if actualLabels[i] == "spam" and predictedLabels[i] == "ham": fn += 1
    return (tp + tn) / (tp + tn + fp + fn)


def get_spamFmeasure(spam_precision, spam_recall):
    return 2 * (spam_precision * spam_recall) / (spam_precision + spam_recall) if (spam_precision + spam_recall) > 0 else 0.0


def spamConfusionParams(fileNumbers, actualLabels, predictedLabels):
    tp = tn = fp = fn = 0
    for i in range(fileNumbers):
        if actualLabels[i] == predictedLabels[i] == "spam": tp += 1
        if actualLabels[i] == predictedLabels[i] == "ham": tn += 1
        if actualLabels[i] == "ham" and predictedLabels[i] == "spam": fp += 1
        if actualLabels[i] == "spam" and predictedLabels[i] == "ham": fn += 1
    return tp, tn, fp, fn


def get_hamPrecision(fileNumbers, actualLabels, predictedLabels):
    tp = fp = 0
    for i in range(fileNumbers):
        if actualLabels[i] == "ham" and predictedLabels[i] == "ham":
            tp += 1
        if actualLabels[i] == "spam" and predictedLabels[i] == "ham":
            fp += 1
    return tp / (tp + fp) if (tp + fp) > 0 else 0.0


def get_hamRecall(fileNumbers, actualLabels, predictedLabels):
    tp = fn = 0
    for i in range(fileNumbers):
        if actualLabels[i] == "ham" and predictedLabels[i] == "ham":
            tp += 1
        if actualLabels[i] == "ham" and predictedLabels[i] == "spam":
            fn += 1
    return tp / (tp + fn) if (tp + fn) > 0 else 0.0


def get_hamAccuracy(fileNumbers, actualLabels, predictedLabels):
    return get_spamAccuracy(fileNumbers, actualLabels, predictedLabels)  # Same formula


def get_hamFmeasure(ham_precision, ham_recall):
    return 2 * (ham_precision * ham_recall) / (ham_precision + ham_recall) if (ham_precision + ham_recall) > 0 else 0.0


def hamConfusionParams(fileNumbers, actualLabels, predictedLabels):
    tp = tn = fp = fn = 0
    for i in range(fileNumbers):
        if actualLabels[i] == predictedLabels[i] == "ham": tp += 1
        if actualLabels[i] == predictedLabels[i] == "spam": tn += 1
        if actualLabels[i] == "spam" and predictedLabels[i] == "ham": fp += 1
        if actualLabels[i] == "ham" and predictedLabels[i] == "spam": fn += 1
    return tp, tn, fp, fn


def evaluation_result(spam_accuracy, spam_precision, spam_recall, spam_fmeasure, ham_accuracy, ham_precision, ham_recall, ham_fmeasure):
    return (
        "################################################################################## \n"
        "#                           *** Evaluation Results ***                           # \n"
        "#                                                                                # \n"
        "#                  Accuracy |     Precission    | Recall |     F1-measure        # \n"
        "# ==========================|===================|========|====================== # \n"
        f"#  Spam Class :    {spam_accuracy:.4f}   | {spam_precision:.4f}     | {spam_recall:.4f}   | {spam_fmeasure:.4f}    # \n"
        "# --------------------------|-------------------|--------|---------------------- # \n"
        f"#  Ham  Class :    {ham_accuracy:.4f}   | {ham_precision:.4f}     | {ham_recall:.4f}  | {ham_fmeasure:.4f}    # \n"
        "#                           |                   |        |                       # \n"
        "################################################################################## \n"
    )


def spam_confusionMatrix(tp, tn, fp, fn):
    return (
        "             ########################################################### \n"
        "             #          *** Confusion Matrix (Spam Class) ***          # \n"
        "             #                                                         # \n"
        "             #                |    Spam     |     Ham     |            # \n"
        "             #      ==========|=============|=============|======      # \n"
        f"             #        Spam    |  TP = {tp}   |  FN = {fn}    |            # \n"
        "             #      ==========|=============|=============|======      # \n"
        f"             #        Ham     |  FP = {fp}     |  TN = {tn}   |            # \n"
        "             #                |             |             |            # \n"
        "             ########################################################### \n"
    )


def ham_confusionMatrix(tp, tn, fp, fn):
    return (
        "             ########################################################### \n"
        "             #          *** Confusion Matrix (Ham Class) ***           # \n"
        "             #                                                         # \n"
        "             #                |    Spam     |     Ham     |            # \n"
        "             #      ==========|=============|=============|======      # \n"
        f"             #        Ham     |  TP = {tp}   |  FN = {fn}     |            # \n"
        "             #      ==========|=============|=============|======      # \n"
        f"             #        Spam    |  FP = {fp}    |  TN = {tn}   |            # \n"
        "             #                |             |             |            # \n"
        "             ########################################################### \n"
    )


def evaluation_output_generator(eval_res, spam_cm, ham_cm):
    return eval_res + "\n\n\n" + spam_cm + "\n\n\n" + ham_cm


def evaluationFileBuilder(evaluation_output):
    with open("evaluation.txt", "w", encoding="utf-8") as f:
        f.write(evaluation_output)