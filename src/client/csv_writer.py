import logging
from csv import writer
from csv import DictWriter
import os

class csvwriter:

    log = logging.getLogger('csvwriter')

    def writeToCsv(self, file, listings):
        """Write the data rows to the CSV file"""

        if self.is_file_empty(file):
            headers = list(listings.keys())
            self.writeHeaderToCsv(file, headers)

        csvwriter().log.info('Write to CSV ' )
        with open(file, 'a', encoding='utf8', newline='') as f:
            try:
                thewriter = writer(f)
                thewriter.writerow(list(listings.values()))
            except:
                logging.error('Fail to write the data to the csv file:%s', file)
            finally:
                f.close()

    def writeHeaderToCsv(self, file, headers):
        """Write the headers to the new CSV"""

        logging.info("CSV Headers written")
        with open(file, 'w', encoding='utf8', newline='') as f:
            try:
                thewriter = writer(f)
                thewriter.writerow(headers)
            except:
                logging.error('Fail to write the header to the csv file:%s', file)
            finally:
                f.close()

    def temp_remove_existing_csv(self, file):
        """Temp feature: Remove previous extract csv before scraping again"""
        if os.path.exists(file):
            os.remove(file)

    def is_file_empty(self, file_path):
        return not os.path.exists(file_path) or os.path.exists(file_path) and os.stat(file_path).st_size == 0
        # return os.path.exists(file_path) and os.stat(file_path).st_size == 0
