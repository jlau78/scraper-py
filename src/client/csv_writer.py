from csv import writer
from csv import DictWriter
import os

class csvwriter:

    def writeToCsv(self, file, listings):
        if self.is_file_empty(file):
            self.writeHeaderToCsv(file)

        with open(file, 'a', encoding='utf8', newline='') as f:
            attributes = []
            thewriter = writer(f)
            for info in listings:
                for keyvalue_attr in info:
                    attributes.append(keyvalue_attr)
                thewriter.writerow(attributes)

            f.close()

    def writeHeaderToCsv(self, file):
        with open(file, 'w', encoding='utf8', newline='') as f:
            header = ['Title', 'Short Description', 'Full Description', 'Price', 'Link']
            thewriter = writer(f)
            thewriter.writerow(header)
            f.close()

    def is_file_empty(self, file_path):
        return os.path.exists(file_path) and os.stat(file_path).st_size == 0

