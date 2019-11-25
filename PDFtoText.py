import os
from PDFtoImage import PDFtoImage
from ImageToText import ImageToText


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

        pdf_to_image = PDFtoImage(self.root_directory, self.pdfs_directory, self.temp_images_directory)
        image_to_text = ImageToText(pdf_to_image.all_pdfs_names, self.root_directory, self.pdfs_directory,
                                    self.temp_images_directory)



temp = PDFtoText(os.getcwd(), os.path.join(os.getcwd(), 'Results/Neural Networks/PDFs'))