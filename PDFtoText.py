import os
from PDFtoImage import PDFtoImage
from ImageToText import ImageToText
import pickle


class PDFtoText:
    def __init__(self, root_directory, pdfs_directory):
        self.root_directory = root_directory
        self.pdfs_directory = pdfs_directory
        self.temp_images_directory = os.path.join(self.pdfs_directory, 'Temp_Images')

        os.chdir(self.pdfs_directory)

        if os.path.exists(self.temp_images_directory):
            pass
        else:
            os.mkdir('Temp_Images')

    def convert_pdf_to_image(self):
        pdf_to_image = PDFtoImage(self.root_directory, self.pdfs_directory, self.temp_images_directory)

        with open(os.path.join(self.pdfs_directory, 'Results_pdfs_to_images.pkl'), 'wb') as file_output:
            pickle.dump(pdf_to_image, file_output, -1)

    def convert_image_to_text(self):
        with open(os.path.join(self.pdfs_directory, 'Results_pdfs_to_images.pkl'), 'rb') as file_input:
            saved_pdf_to_image = pickle.load(file_input)

        ImageToText(saved_pdf_to_image.all_pdfs_names, self.root_directory, self.pdfs_directory,
                    self.temp_images_directory)

        return saved_pdf_to_image

    def convert_total(self):
        self.convert_pdf_to_image()
        saved_pdf_to_image = self.convert_image_to_text()

        saved_pdf_to_image.clean_folders()


if __name__ == "__main__":
    temp = PDFtoText(os.getcwd(), os.path.join(os.getcwd(), 'Results/Neural Networks/PDFs'))
    temp.convert_total()
