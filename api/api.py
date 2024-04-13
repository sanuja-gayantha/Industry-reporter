# Developed by @sanuja : https://github.com/sanuja-gayantha



class Api():
    def __init__(self):
        self.pdf_data_list_path = os.path.join(os.getcwd(), 'pdfDataList.json')

    
    def read_json_file(self, path):
        with open(path) as json_file:
            result = json.load(json_file)
            return result













