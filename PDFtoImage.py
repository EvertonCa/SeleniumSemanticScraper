from pdf2image import convert_from_path
import tempfile
import os
from multiprocessing import Pool
import Timer


class PDFParameter:
    def __init__(self, root_directory, images_directory, pdfs_directory, pdf_name):
        self.root_directory = root_directory
        self.images_directory = images_directory
        self.pdfs_directory = pdfs_directory
        self.pdf_name = pdf_name


# creates the list with PDFParameter objects and passes it to the function convert_one using multiprocessing
def convert_all_multithread(all_pdfs_names, root_directory, images_directory, pdfs_directory):
    all_pdfs_parameters = []
    for pdf in all_pdfs_names:
        pdf_parameter = PDFParameter(root_directory, images_directory, pdfs_directory, pdf)
        all_pdfs_parameters.append(pdf_parameter)

    start_timer = Timer.timeNow()
    print(start_timer)

    # more than 4 threads will end up in i/o bottleneck (even with NVME SSD)
    with Pool(4) as pool:
        r = pool.map(convert_one, all_pdfs_parameters)

    print("Total time PDF to image = " + str(Timer.totalTime(start_timer, Timer.timeNow())))


# convert one pdf to image
def convert_one(pdf_parameter):
    os.chdir(pdf_parameter.images_directory)

    # uses temporary folder to avoid filling up the RAM when converting several pdfs at a time.
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(os.path.join(pdf_parameter.pdfs_directory, pdf_parameter.pdf_name),
                                             output_folder=path)
        temp_index = 1

        folder_name = pdf_parameter.pdf_name[:-4]

        if os.path.exists(os.path.join(pdf_parameter.images_directory, folder_name)):
            pass
        else:
            os.mkdir(folder_name)

        os.chdir(os.path.join(pdf_parameter.images_directory, folder_name))

        for page in images_from_path:
            page.save('Page' + str(temp_index) + '.jpg', 'JPEG')
            temp_index += 1

    os.chdir(pdf_parameter.root_directory)
    print("CONVERTED: " + pdf_parameter.pdf_name)


class PDFtoImage:
    def __init__(self, root_directory, pdfs_directory, images_directory):
        self.root_directory = root_directory
        self.pdfs_directory = pdfs_directory
        self.images_directory = images_directory
        self.all_pdfs_names = []
        self.all_folders_names = []

        self.pdf_files_names()

        self.convert_all(self.all_pdfs_names)

        self.folder_names()

    # convert all pdfs in the /PDFs folder to images in the /Images/~NAME~ folder
    def convert_all(self, all_pdfs_names):
        os.chdir(self.images_directory)
        print('~~~~~~ CONVERTING FILES TO IMAGE ~~~~~~')
        convert_all_multithread(all_pdfs_names, self.root_directory, self.images_directory, self.pdfs_directory)
        os.chdir(self.root_directory)
        print('')

    # return all the pdfs names in a list
    def pdf_files_names(self):
        all_files = os.listdir(self.pdfs_directory)
        for temp_file_names in all_files:
            if temp_file_names[-4:] == '.pdf':
                self.all_pdfs_names.append(temp_file_names)

    # return all the folders names in a list
    def folder_names(self):
        all_folders = os.listdir(self.images_directory)
        for temp_folder_names in all_folders:
            if temp_folder_names[0] != '.':
                self.all_folders_names.append(temp_folder_names)

    # deletes all the images created as well the correspondent folders
    def clean_folders(self):
        for folder in self.all_folders_names:
            files_list = os.listdir(os.path.join(self.images_directory, folder))
            os.chdir(os.path.join(self.images_directory, folder))
            for file in files_list:
                os.remove(file)
            os.rmdir(os.path.join(self.images_directory, folder))
        os.chdir(self.root_directory)
