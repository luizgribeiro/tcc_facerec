import tkinter
from tkinter import ttk

class DisplayAtendees:

    def __init__(self, window):
        
        self.frame = tkinter.Frame(window, width=700, height=12)
        self.frame.grid(row=0, column=0, sticky="n")
        

        self.separator = ttk.Separator(self.frame, orient=tkinter.VERTICAL)
        self.separator.grid(row=0, column=1, rowspan=3, sticky='ns')

        #TODO: substituir labels por controller que pega nomes
        tkinter.Label(self.frame, text="Alunos Presentes").grid(row=0,column=0)
        tkinter.Label(self.frame, text="José da silva").grid(row=2,column=0, sticky="w")
        tkinter.Label(self.frame, text="Matheus Camargo").grid(row=3,column=0, sticky="w")


    def update_atendees(self, aluno):

        pass

        #TODO: add label para aluno do display

    
    