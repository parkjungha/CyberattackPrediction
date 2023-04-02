import os

directory = "C:/Users/jungh/Desktop/getTweetText/corpus/"
outfile_name= "merged_corpus.txt"

out_file = open(outfile_name,'w')
files = os.listdir(directory)

for filename in files:
    file=open(directory+filename)
    for line in file:
        out_file.write(line)
    out_file.write("\n")
    file.close()
out_file.close()
