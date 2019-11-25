from pdf2image import convert_from_path
import tempfile
import os
from multiprocessing import Pool
from multiprocessing import cpu_count
from tqdm import tqdm


class PDFtoImage:
    def __init__(self):
        self.root_directory = os.getcwd()
        self.pdf_directory = self.root_directory + '/PDFs/'
        self.images_directory = self.root_directory + '/Images/'

        if os.path.exists(self.pdf_directory):
            pass
        else:
            os.mkdir('PDFs')

        if os.path.exists(self.images_directory):
            pass
        else:
            os.mkdir('Images')

    # convert all pdfs in the /PDFs folder to images in the /Images/~NAME~ folder
    def convert_all(self, all_pdfs_names):
        os.chdir(self.images_directory)
        print('~~~~~~ CONVERTING FILES TO IMAGE ~~~~~~')
        with Pool(cpu_count()) as p:
            r = list(tqdm(p.imap(self.convert_one, all_pdfs_names), total=len(all_pdfs_names)))
        os.chdir(self.root_directory)
        print('')

    # convert one pdf to image
    def convert_one(self, pdf_name):
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(self.pdf_directory + pdf_name, output_folder=path)
            temp_index = 1

            folder_name = pdf_name[:-4]

            if os.path.exists(self.images_directory + folder_name):
                pass
            else:
                os.mkdir(folder_name)

            os.chdir(self.images_directory + folder_name)

            for page in images_from_path:
                page.save('Page' + str(temp_index) + '.jpg', 'JPEG')
                temp_index += 1
            os.chdir(self.images_directory)

    # return all the pdfs names in a list
    def pdf_files_names(self):
        all_files = os.listdir(self.pdf_directory)
        all_pdfs_names = []
        for temp_file_names in all_files:
            if temp_file_names[-4:] == '.pdf':
                all_pdfs_names.append(temp_file_names)

        return all_pdfs_names

    # return all the folders names in a list
    def folder_names(self):
        all_folders = os.listdir(self.images_directory)
        all_folders_names = []
        for temp_folder_names in all_folders:
            if temp_folder_names[0] != '.':
                all_folders_names.append(temp_folder_names)

        return all_folders_names

    # deletes all the images created as well the correspondent folders
    def clean_folders(self, all_folders_names):
        for folder in all_folders_names:
            files_list = os.listdir(self.images_directory + folder)
            os.chdir(self.images_directory + folder)
            for file in files_list:
                os.remove(file)
            os.rmdir(self.images_directory + folder)
        os.chdir(self.root_directory)
