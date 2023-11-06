#!/usr/bin/python3

from collections import Counter
import time
import os
import itertools
import pandas as pd

print("Please ensure Mummer text file is prepared properly. Starting in 5 seconds, Ctrl + C to exit.")
time.sleep(5)
# after removing all BEGIN, END, header in mummer file and ensuring 2x space between each alignment
filename = "/home/aryeh/filefortesting" # Insert your Mummer file here.
lines = []
with open(filename) as f:
    for line in f:
        line = line.strip()
        if line:
            lines.append(line)
           
lines = pd.DataFrame(lines, columns=['Sequence'])
#lines['Sequence'].str.partition(' ')[[1, 2]].rename({1: 'Position', 2: 'Sequence'}, axis=1)
lines[['Position', 'Sequence']] = lines['Sequence'].str.split(' ', n=1, expand=True) #Create 2 columns
lines = lines.replace(r"^ +| +$", r"", regex=True) #remove trailing spaces
lines['Sequence Length']  = lines['Sequence'].str.len() #Extract length of sequence
#print(lines['Position'].to_string(index=False))
#print(lines['Sequence'].to_string(index=False))
print(lines)
#Subsequent pairs of values in 'Position' column, with their respective Sequences, have aligned.
lines.to_csv('out.csv', sep=',') #hardcoded, change csv name

data = pd.read_csv("out.csv", sep=',')

names = data["Sequence"].to_list()

print(names)

def compare(x, y, no_match_c=' ', match_c='|'):
 if len(y) < len(x):
  x, y = y, x
 result = ''
 n_diff = 0
 for c1, c2 in zip(x, y):
     if c1 == c2:
         result += match_c
     else:
         result += no_match_c
         n_diff += 1
 delta = len(y) - len(x)
 result += delta * no_match_c
 n_diff += delta
 return (result, n_diff)

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)

addcolumn = []
duplicatecolumn = []
for x, y in pairwise(names):
   result, n_diff = compare(x, y, no_match_c='_')
   addcolumn.append("%d" % n_diff)
   print(addcolumn)
   #list(map(int, addcolumn))
   
for i in addcolumn:
   duplicatecolumn.extend([i,i])
   print(duplicatecolumn)


lines = lines.join(pd.DataFrame({'Unaligned': duplicatecolumn}))
print(lines)
lines['Unaligned'] = lines['Unaligned'].astype(int)

lines['Aligned Count'] = lines['Sequence Length'] - lines['Unaligned']
print(lines)

#lines = lines.groupby(['Aligned Count','Position']).agg(tuple).applymap(list).reset_index()


Aligned_Count_List = lines['Aligned Count'].tolist()
Aligned_Count_List = list(dict.fromkeys(Aligned_Count_List))
Position_List = lines['Position'].tolist()



   #append this to dataframe and then subtract from length for aligned,(done)
   #split above lists then duplicate pairs of Aligned Count by each Position value
   #make arrays out of each first 2 row values in Sequence Position, and new column (a b c)
   #print("%d + %d = %d" % (x, y, x + y))
#def process_data(Sequence):
 #   for x in Sequence:
  #      print(f"{name}: {subnet}")

#if __name__ == "__main__":
 #   process_data(names, subnets)

#start = 0
#end = len(Position_List)
#step = 2
#for i in range(start, end, step):
 #   x = i
  #  print(Position_List[x:x+step])
 

print(Aligned_Count_List)
 
# How many elements each
# list should have
n = 2
 
# using list comprehension
final = [Position_List[i * n:(i + 1) * n] for i in range((len(Position_List) + n - 1) // n )]
#print(final)

#print(first)  
#print('\n'.join(final))

#[elem for n, elem in zip(Aligned_Count_List, final) for i in range(n)]


out = []
for v,n in zip(final, Aligned_Count_List):
    out.extend([v]*n)
    print(*out, sep='\n')
