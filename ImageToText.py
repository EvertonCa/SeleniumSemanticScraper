import os
from PDF import PDF
import pytesseract
from PIL import Image
import pickle
from multiprocessing import Pool
from multiprocessing import cpu_count
import Timer


class PDFParameter:
    def __init__(self, root_directory, images_directory, pdfs_directory, pdf_name):
        self.root_directory = root_directory
        self.images_directory = images_directory
        self.pdfs_directory = pdfs_directory
        self.pdf_name = pdf_name
        self.results_directory = os.path.join(self.pdfs_directory, 'PDFsToText')


# creates the list with PDFParameter objects and passes it to the function convert_one using multiprocessing
def convert_all_multithread(all_pdfs_names, root_directory, images_directory, pdfs_directory):
    all_pdfs_parameters = []
    for pdf in all_pdfs_names:
        pdf_parameter = PDFParameter(root_directory, images_directory, pdfs_directory, pdf)
        all_pdfs_parameters.append(pdf_parameter)

    start_timer = Timer.timeNow()
    print(start_timer)

    cpu_threads = cpu_count()

    # tesseract has a cap of 4 threads per instance.
    if cpu_threads >= 4:
        divisions = int(cpu_threads / 4)
        cpu_threads = cpu_threads / divisions

    # start converting using all threads available
    with Pool(cpu_threads) as p:
        r = p.map(convert_one, all_pdfs_parameters)

    print("Total time image to text = " + str(Timer.totalTime(start_timer, Timer.timeNow())))


# convert one folder of images to string
def convert_one(pdf_parameter):
    folder_name = pdf_parameter.pdf_name[:-4]

    os.chdir(os.path.join(pdf_parameter.images_directory, folder_name))

    temp_directory = os.getcwd()

    all_images = os.listdir(temp_directory)

    new_pdf = PDF(folder_name)

    for page in range(len(all_images)):
        new_pdf.add_page(pytesseract.image_to_string(Image.open(os.path.join(temp_directory,
                                                                    'Page' + str(page + 1) + '.jpg'))))

    save_to_file(folder_name, new_pdf, pdf_parameter)

    os.chdir(pdf_parameter.images_directory)

    print("Converted: " + pdf_parameter.pdf_name)


# saves the articles to .pkl and .txt files
def save_to_file(folder_name, pdf, pdf_parameter):
    os.chdir(pdf_parameter.results_directory)

    with open(folder_name + '.pkl', 'wb') as file_output:
        pickle.dump(pdf, file_output, -1)

    text_file = open(folder_name + '.txt', 'w')
    for page in pdf.pages:
        text_file.write(page)
    text_file.close()

    os.chdir(pdf_parameter.root_directory)


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

        convert_all_multithread(self.all_pdfs_names, self.root_directory, self.images_directory, self.pdfs_directory)

        os.chdir(self.root_directory)
        print('')

