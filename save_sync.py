import pickle
import os.path

class show_data():
    def __init__(self, path):
        self.path = path
        if os.path.isfile(path):
            self.data = pickle.load(path)
        else:
            self.data = []

    def save(self):
        pickle.dump(self.data, self.path)

    def update_show_list(self, urls):
        for url in urls:
            match = False
            for d in self.data:
                if d['url'] == url:
                    match = True
            if not match:
                self.data.append({"url":url})
    
    

        