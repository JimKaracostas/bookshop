# main.py

# IMPORTS
import tkinter as tk
from controllers.controller import MainController

def main():
    root = tk.Tk()
    
    root.title("Σύστημα Διαχείρισης Βιβλιοπωλείου")
    root.geometry("600x450")
    root.resizable(True, True)
    
    app = MainController(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()