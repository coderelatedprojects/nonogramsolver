from .reader import ReaderInterface
from .nonogram import Nonogram

config = {
    "rows" : [],
    "columns" : [],
    "height" : "int",
    "width" : "int",
    "catalogue" : "",
    "title" : "",
    "by" : "",
    "copyright" : "",
    "license" : "",
    "goal" : ""
}

class FileReader(ReaderInterface):
    def read_nonogram(path) -> Nonogram:
        reading_rows = False
        reading_cols = False

        
        #add error handling and incomplete/impossible puzzle detection
        with open(path, 'r') as reader:
            for line in reader:
                keyword = line.split(' ')[0].strip()
                if keyword in config.keys():
                    reading_rows = keyword == "rows"
                    reading_cols = keyword == "columns"
                    if not reading_rows and not reading_cols:
                        value = line.removeprefix(keyword).strip()
                        # not sure how to do it better
                        if config[keyword] == "int":
                            value = int(value)
                        config[keyword] = value
                else:
                    #if line is not empty
                    if line.strip():
                        if reading_rows:
                            config["rows"].append([int(el) for el in line.split(',')]) 
                        if reading_cols: 
                            config["columns"].append([int(el) for el in line.split(',')])
                        
        return Nonogram(config)
                