import csv
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#Parent class
class FileHandler:
    def __init__(self):
        # Encapsulation: Private attributes to store directory paths
        self.__core_dir = "data/core/"
        self.__user_dir = "data/user/"

    # GETTER methods to allow safe access to private attributes
    def get_core_dir(self):
        return self.__core_dir

    def get_user_dir(self):
        return self.__user_dir

    # SETTER methods (Standard A-Level practice)
    def set_core_dir(self, new_dir):
        self.__core_dir = new_dir

    def set_user_dir(self, new_dir):
        self.__user_dir = new_dir

    # POLYMORPHISM: This base method will be overridden by the child class
    def get_description(self):
        return "Generic system file handler"

    def get_all_decks(self):
        # Using getters to access our private directories
        c_dir = self.get_core_dir()
        u_dir = self.get_user_dir()
        
        core = [f[:-4] for f in os.listdir(c_dir) if f.endswith('.csv')]
        user = [f[:-4] for f in os.listdir(u_dir) if f.endswith('.csv')]
        return core, user


# =====================================================================
# 2. THE CHILD CLASS (Demonstrates Inheritance & Polymorphism)
# =====================================================================
class DeckController(FileHandler): # INHERITANCE: Inherits from FileHandler
    def __init__(self):
        # Calls the parent class constructor
        super().__init__()

    # POLYMORPHISM: Overriding the parent's get_description method
    def get_description(self):
        return "Subclass managing active deck operations"

    def create_deck(self, form):
        title = form.get('title', 'deck').strip().replace(" ", "_") + ".csv"
        user_folder = self.get_user_dir() # Accessing inherited private variable via getter
        
        os.makedirs(user_folder, exist_ok=True)
        path = os.path.join(user_folder, title)
        
        # Simple procedural file writing
        questions = form.getlist('q')
        answers = form.getlist('a')
        rows_to_write = []
        for i in range(len(questions)):
            rows_to_write.append([questions[i].strip(), answers[i].strip(), "2.5", "1"])
            
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows_to_write)

    def delete_deck(self, filename):
        path = f"{self.get_user_dir()}{filename}.csv"
        if os.path.exists(path):
            os.remove(path)

    def load_and_format(self, filename, idx):
        path = f"{self.get_core_dir()}{filename}.csv"
        if not os.path.exists(path):
            path = f"{self.get_user_dir()}{filename}.csv"
            
        if not os.path.exists(path):
            return None
            
        with open(path, "r", encoding="utf-8") as f:
            cards = list(csv.reader(f))
            
        if idx >= len(cards):
            return None
            
        row = cards[idx]
        
        # Simple textbook loop to format chemical subscripts
        raw_question = row[0]
        raw_answer = row[1]
        clean_q = ""
        clean_a = ""

        for char in raw_question:
            if char in "0123456789":
                clean_q += f"<sub>{char}</sub>"
            else:
                clean_q += char
                
        for char in raw_answer:
            if char in "0123456789":
                clean_a += f"<sub>{char}</sub>"
            else:
                clean_a += char

        return {"question": clean_q, "answer": clean_a, "ao": self.get_description()}

    def process_score(self, filename, idx, score):
        path = f"{self.get_core_dir()}{filename}.csv"
        if not os.path.exists(path):
            path = f"{self.get_user_dir()}{filename}.csv"
            
        with open(path, "r", encoding="utf-8") as f:
            cards = list(csv.reader(f))
            
        row = cards[idx]
        ef_idx = 3 if len(row) == 5 else 2
        int_idx = 4 if len(row) == 5 else 3
        
        ef = float(row[ef_idx])
        interval = int(row[int_idx])
        
        # Linear A-Level Spaced Repetition Math
        if score < 3:
            ef = ef - 0.2
            if ef < 1.3:
                ef = 1.3
            interval = 1
        else:
            ef = ef + 0.15
            interval = round(interval * ef)
            if interval > 180:
                interval = 180
                
        cards[idx][ef_idx] = str(ef)
        cards[idx][int_idx] = str(interval)
        
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(cards)
            
        return interval


# =====================================================================
# 3. TINY FLASK ROUTES (Kept short and simple just as you liked)
# =====================================================================
UI = DeckController()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.args.get('del'): UI.delete_deck(request.args.get('del'))
    if 'title' in request.form: UI.create_deck(request.form)
    return render_template('index.html', view=request.args.get('view', 'menu'), core=UI.get_all_decks()[0], user=UI.get_all_decks()[1])


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    sub, idx = request.args.get('subject', ''), request.args.get('idx', 0, type=int)
    if 'score' in request.form: 
        return render_template('index.html', view="done", days=UI.process_score(sub, idx, int(request.form['score'])), date="Scheduled!", subject=sub, idx=idx)
    return render_template('index.html', view="quiz", q=UI.load_and_format(sub, idx), subject=sub, idx=idx)


if __name__ == '__main__':
    os.makedirs("data/core", exist_ok=True)
    os.makedirs("data/user", exist_ok=True)
    app.run(debug=True)