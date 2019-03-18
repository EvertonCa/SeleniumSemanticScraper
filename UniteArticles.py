import os
import pickle
import ExcelExporter

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

# user message

print('Please put the Articles.pkl and Authors.pkl files of the searches you would '
      'like to merge in the /Files/Unite/ folder.')
print('Rename the files to ArticlesX.pkl and AuthorsX.pkl, where X is a number starting from 1 to '
      'the quantity of searches you would like to merge.')

input('Press ENTER when ready!')

all_pkl_files = os.listdir(directory_unite)
all_pkl_names = []
for temp_file_names in all_pkl_files:
    if temp_file_names[-4:] == '.pkl':
        all_pkl_names.append(temp_file_names)

quantity_files = int(len(all_pkl_files)/2)

# merge all files into one
articles_list = []
authors_list = []

for i in range(quantity_files):
    file_name_article = directory_unite + 'Articles' + str(i+1) + '.pkl'
    file_name_author = directory_unite + 'Authors' + str(i + 1) + '.pkl'
    with open(file_name_article, 'rb') as file_input:
        articles_temp_list = pickle.load(file_input)
    for article in articles_temp_list:
        articles_list.append(article)
    with open(file_name_author, 'rb') as file_input:
        authors_temp_list = pickle.load(file_input)
    for author in authors_temp_list:
        authors_list.append(author)

excelExporter = ExcelExporter.ExcelExporter()
excelExporter.merge_creator(articles_list, authors_list)

print('~~~~ Merged Excel created! ~~~~')
