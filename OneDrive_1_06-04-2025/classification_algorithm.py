import sklearn
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import FakeNewsDetector2 as fnd

v = open("words.csv")
vocab = list(set(v.read().lower().split("\n")))


def act(z):
    return 1/(1+math.exp(-z))
a = sklearn.feature_extraction.text.TfidfVectorizer(use_idf = True, vocabulary = vocab, smooth_idf = True)
# f = open("test.txt")
# content = f.read().split(";")
# b = a.fit_transform(content)
# d = a.get_feature_names_out()
# z = input()

W = np.zeros(len(vocab))

def prob(text):
    global articles
    articles.append(text)
    x = a.fit_transform(articles)
    x1 = x[-1].toarray()[0]
    z = W@x1
    y = 0 if act(z) < 0.5 else 1
    return y



def regression(x, alpha, momentum, expected):
    deltaW = np.zeros(len(vocab))
    
    W = fnd.Main2(x, len(vocab))
    #global W
    W = np.zeros(len(vocab))
    w = 0
    costs = []
    #for j in range (len(W)):
     #   W[j] = random.random() - 0.5
    for i in range((math.floor(0.8 * len(articles)/100)-1)):
        sumands = np.zeros((100, len(W)))
        cost = 0
        for j in range (100):
            x1 = x[100 * i + j].toarray()[0]
            z = W@x1
            y = 0 if act(z) < 0.5 else 1
            sumands[j] = (act(z) - expected[100 * i+j]) * x1
            cost -= expected[100 * i + j] * math.log(act(z)) + (1-expected[100 * i+j]) * math.log(act(z))
        costs.append(cost)
        deltaW = - alpha/100 * np.sum(sumands, axis=0) + deltaW * momentum
        W = W + deltaW
 

    correct = 0
    for i in range(round(0.8 * len(articles)), len(articles)):
        x1 = x[i].toarray()[0]
        z = w + W@x1
        y = 0 if act(z) < 0.5 else 1
        if (expected[i] == y):
            correct += 1
    
    accuracy = correct / (0.2 * len(articles))

    #plt.plot(costs)
    #plt.show()


    f = 1







fake = open("Fake.csv")

lines = []
expected1 = []
for i in range(23503):
    try:
        lines.append(",".join(fake.readline().split(",\"")[1].split(",")[0:-2]))
        expected1.append(0)
        if len(lines[-1]) < 100:
            lines.pop()
            expected1.pop()
    except:
        pass

real = open("True.csv")

for i in range(21418):
    try:
        lines.append("-".join(",".join(real.readline().split(",\"")[1].split("\",")[0:-1]).split("-")[1:]))
        expected1.append(1)
        if len(lines[-1]) < 100:
            lines.pop()
            expected1.pop()
    except:
        pass

articles = []
expected = []
for i in range(len(lines)):
    ran = random.randint(0, len(lines) - 1)
    articles.append(lines[ran])
    if len(lines[ran]) < 100:
        t = lines[ran]
        pass
    del lines[ran]
    expected.append(expected1[ran])
    del expected1[ran]

for article in articles:
    if (len(article) < 100):
        articles.remove(article)

b = a.fit_transform(articles)

removed = 0
idf = a.idf_
r = len(idf)
for i in range(r):
    if idf[i] > 9:
        del vocab[i - removed]
        removed += 1

a = sklearn.feature_extraction.text.TfidfVectorizer(use_idf = True, vocabulary = vocab, smooth_idf = True)
b = a.fit_transform(articles)


regression(b, 0.1, 0.9, expected)







        




