# Mummer-Alignment-To-Dataframe
Mummer Alignment To Dataframe.

This script takes as input a Mummer .txt file, converts it into a dataframe with headers, iterating over each aligned pair of sequences and calculating number of aligned bases by removal of unaligned nucleotides.
Iterates over an ~10000 line file in 10-15 seconds.
An accompanying CSV is also generated for user reference.
Each aligned pair's position is determined and then duplicated accordingly to how many times the positions aligned.
Final output is converted into list format for input into Jupyter Notebook / matplotlib for parallel plots as shown in genomic comparison analysis, e.g. gregornickel's pcp package at 
https://github.com/gregornickel/pcp.


![image](https://github.com/aryehjc/Mummer-Alignment-To-Dataframe/assets/83979895/dfda0328-111f-4784-a86d-72e6e40e028a)



Above image depicts matching nucleotides between two genomes, with positions on both axes.

Prior to using this script you must remove all BEGIN, END, header, footer in Mummer .txt file and ensure 2x space between each pair of aligned sequences.

Insert a text file in:

```
filename = "/home/aryeh/filefortesting"
```

replacing the example above with your chosen file path. Then run the script
```
python3 MummerToDataframe.py
```
The program commences after prompting you to ensure the Mummer file has been prepared accordingly.

```
lines = []
with open(filename) as f:
    for line in f:
        line = line.strip()
        if line:
            lines.append(line)

lines = pd.DataFrame(lines, columns=['Sequence'])
lines[['Position', 'Sequence']] = lines['Sequence'].str.split(' ', n=1, expand=True) #Create 2 columns
lines = lines.replace(r"^ +| +$", r"", regex=True) #remove trailing spaces
lines['Sequence Length']  = lines['Sequence'].str.len() #Extract length of sequence
print(lines)
```
This parses the text file for conversion to dataframe, creating columns for the nucleotide sequence, the positions of aligned bases and removes trailing & leading spaces in the sequence to calculate its length.
Base length of aligned sequences is calculated.

```
#Subsequent pairs of values in 'Position' column, with their respective Sequences, have aligned.
lines.to_csv('out.csv', sep=',') #hardcoded, change csv name

data = pd.read_csv("out.csv", sep=',')

names = data["Sequence"].to_list()

print(names)
```

Creates a CSV file with the dataframe, and converts the Sequence data to a list format for iteration, to remove unaligned bases. Change CSV name to your preference.
```
# Function 1
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
```

```
# Function 2
def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)
```

Two functions are created, one to find 'differences' between nucleotides, e.g.

```
A: GTACCCCC
B: GTCCCCCC
```
The third character in above strings A and B shows a 'different' unmatching base, A contains letter A at position 3, B contains a letter C at position 3. This is counted as an unaligned base, and removed from total length of the sequence to calculate number of aligned bases.

The second function iterates over each pair of elements (pair of aligned sequences) in the Sequence list, using the first function repeatedly to calculate number of aligned bases over each pair.
```
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
```

Creating two lists from the data, one to append a column of number of unaligned bases for each pair of sequences to the dataframe.
The other will duplicate this value, as the dataframe occurs as follows:

```
1      10
5289   10  
```
Meaning position 1 and 5289, as an example, have 10 unaligned bases. 

```
lines = lines.join(pd.DataFrame({'Unaligned': duplicatecolumn}))
print(lines)
lines['Unaligned'] = lines['Unaligned'].astype(int)

lines['Aligned Count'] = lines['Sequence Length'] - lines['Unaligned']
print(lines)

#lines = lines.groupby(['Aligned Count','Position']).agg(tuple).applymap(list).reset_index()


Aligned_Count_List = lines['Aligned Count'].tolist()
Aligned_Count_List = list(dict.fromkeys(Aligned_Count_List))
Position_List = lines['Position'].tolist()
```

Joining unaligned base count as a column to dataframe and enabling them to be subtracted from the Sequence Length.


```
print(Aligned_Count_List)
 ```

For reference to see number of aligned count.

```
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

```

Finally, converting aligned sequence count to list format in 'chunks' of 2, showing aligned positions, and duplicating each chunk according to the number of times the pair aligns,
for graphing in Matplotlib. Multiple lines shared between 2 points = how many alignments.

Sequences can be highlighted in the list format and pasted into a Jupyter Notebook for easy plotting of data coordinates for graphing. 

Wrap the script in a Bash script to remove quotation '' marks and allow pasting coordinates into Jupyter notebook cells to produce graphs.

```
#!/bin/bash
python3 /home/aryeh/MummerToDataframe.py > output.txt
tr -d \' < output.txt > DataArray.txt
sed -i -e 's/]/],/g' DataArray.txt
```
