import os
from PDF import PDF
import pytesseract
from PIL import Image
import pickle
from multiprocessing import Pool
from multiprocessing import cpu_count
from tqdm import tqdm


class ImageToText:
    def __init__(self, all_pdfs_names, root_directory, pdfs_directory, images_directory):
        self.all_pdfs_names = all_pdfs_names
        self.root_directory = root_directory
        self.images_directory = images_directory
        self.pdfs_directory = pdfs_directory
        self.results_directory = os.path.join(self.pdfs_directory, 'PDFsToText')

        os.chdir(self.pdfs_directory)
        if os.path.exists(self.results_directory):
            pass
        else:
            os.mkdir('PDFsToText')

        self.convert_all()

    # convert all images to strings using Tesseract and saves them as an Article object and to file
    def convert_all(self):
        os.chdir(self.images_directory)
        print('~~~~~~ CONVERTING FILES TO .txt ~~~~~~')
        with Pool(cpu_count()) as p:
            r = list(tqdm(p.imap(self.convert_one, self.all_pdfs_names), total=len(self.all_pdfs_names)))
        os.chdir(self.root_directory)
        print('')

    # convert one folder of images to string
    def convert_one(self, pdf_name):
        folder_name = pdf_name[:-4]

        os.chdir(os.path.join(self.images_directory, folder_name))

        temp_directory = os.getcwd()

        all_images = os.listdir(temp_directory)

        new_pdf = PDF(folder_name)

        for page in range(len(all_images)):
            new_pdf.add_page(pytesseract.image_to_string(Image.open(os.path.join(temp_directory,
                                                                        'Page' + str(page + 1) + '.jpg'))))

        self.save_to_file(folder_name, new_pdf)

        os.chdir(self.images_directory)

    # saves the articles to .pkl and .txt files
    def save_to_file(self, folder_name, pdf):
        os.chdir(self.results_directory)

        with open(folder_name + '.pkl', 'wb') as file_output:
            pickle.dump(pdf, file_output, -1)

        text_file = open(folder_name + '.txt', 'w')
        for page in pdf.pages:
            text_file.write(page)
        text_file.close()

        os.chdir(self.root_directory)
