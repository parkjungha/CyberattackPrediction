with open('C:/Users/jungh/Desktop/getTweetText/corpus/merged_corpus.txt', 'r') as f:
    list_file = []
    for line in f:
        list_file.append(line)

for i in range(len(list_file)):
    list_file.remove('\n')

with open('/Users/jungh/Desktop/getTweetText/corpus/corpus_.txt', 'w') as f:
    for item in list_file:
        f.write("%s\n" % item)