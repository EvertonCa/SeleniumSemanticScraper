import os
import pickle
from pathlib import Path

# saves current directory in a string
current_directory = os.getcwd()

# saves the Files directory in a string
directory_files = current_directory + '/Files/'

# saves the Unite directory in a string
directory_unite = directory_files + 'Unite/'

# check if the Files folder exists and creates it if not
if os.path.exists(directory_files):
    pass
else:
    os.mkdir('Files')

# check if the Unite folder exists and creates it if not
if os.path.exists(directory_unite):
    pass
else:
    os.chdir(directory_files)
    os.mkdir('Unite')

# return to root folder
os.chdir(current_directory)

quantity_files = int(input('How many searches would you like to merge in one Excel file?\n'))

print('Please put the Articles.pkl and Authors.pkl files of the searches you would '
      'like to merge in the /Files/Unite/ folder')
print('Rename the files to ArticlesX.pkl and AuthorsX.pkl, where X is a number starting from 1 to '
      'the quantity of searches you would like to merge.')
