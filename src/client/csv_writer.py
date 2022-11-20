import logging
from csv import writer
from csv import DictWriter
import os

class csvwriter:

    def writeToCsv(self, file, listings):
        if self.is_file_empty(file):
            self.writeHeaderToCsv(file)

        with open(file, 'a', encoding='utf8', newline='') as f:
            thewriter = writer(f)
            for info in listings:
                row = []
                for keyvalue in info:
                    if keyvalue is not None:
                        logging.info('keyvalue:'+str(keyvalue))
                        row.append(str(keyvalue).strip())

                thewriter.writerow(row)

            f.close()

    def writeHeaderToCsv(self, file):
        with open(file, 'w', encoding='utf8', newline='') as f:
            header = ['Title', 'Short Description', 'Full Description', 'Price', 'Link']
            thewriter = writer(f)
            thewriter.writerow(header)
            f.close()

    def temp_remove_existing_csv(self, file):
        """Temp feature: Remove previous extract csv before scraping again"""
        if os.path.exists(file):
            os.remove(file)

    def is_file_empty(self, file_path):
        return os.path.exists(file_path) and os.stat(file_path).st_size == 0

    def clean_string(self, svalue):
        str(svalue).replace('\t', '  ')
        # str(svalue).replace('\b', ' ')
        str(svalue).replace('\r', ' ')
        str(svalue).replace('\n', '  ')
        return str(self.encode_ascii(svalue))

    def encode_ascii(self, svalue):
        return str(svalue).encode('ascii', 'ignore')