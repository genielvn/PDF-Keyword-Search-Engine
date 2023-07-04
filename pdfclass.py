import PyPDF2
import threading

class PDF():
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
        
        self.content = self.convert_to_text(self.file_path)

        self.included = True

    def convert_to_text(self, file_path):
        pdf_file = open(file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        number_of_pages = len(pdf_reader.pages)

        list_of_texts = []

        for i in range(number_of_pages):
            page_object = pdf_reader.pages[i]
            extracted_text = page_object.extract_text()
            list_of_texts.append(extracted_text)

        contents = ""

        return contents.join(list_of_texts)
    
    def get_text(self):
        return self.content