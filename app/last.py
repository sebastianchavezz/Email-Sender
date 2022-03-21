import tkinter as tk
from tkinter import *
from tkinter import ttk
from turtle import width
from .treeviewOverride import Tree
from .data import Datahandler

class Appsjoen(tk.Tk):

    
    amount_of_products: int
    #boolean is flaggin the ENTER event
    selected_record : bool = False


    def __init__(self):
        super().__init__()
        self.df = Datahandler()
        
        self.amount_of_products = len(self.df.dataframe)
        #print(f'amount of products: {self.amount_of_products}')
        #style
        self._add_style()
        #create TreeFrame
        self._init_Frames()
        #init treeView
        self._init_treeView()
        
        #add the Columns and Headings
        self.add_columns_and_heading()
        #fill with data from dataframe
        self.add_data()
        #add labels
        self.labels()
        #add entry Boxes
        self.entry_Boxes()
        #add buttons
        self.buttons()
    
    def _add_style(self)-> None:
        """Add style to the pathetic looking app"""
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('Treeview',
            background= 'silver',
            foreground = 'black',
            rowheight=35,
            fieldbackground='silver'
            )
        self.style.map('Treeview', background=[('selected','green')])

    def _init_Frames(self)->None:
        '''Init all the Frames'''
        self.title('Send Nudes')
        self.geometry('1500x1000')
        self.resizable(True,True)
        #add the tree frame
        self.tree_frame= Frame(self, width=1000, height=1000, background="black")
        self.tree_frame.pack()
        #add the 'add Frame'
        self.add_frame = Frame(self)
        self.add_frame.pack(pady=20)


    def _init_treeView(self)->None:
        '''Init the treeview'''
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)
        self.tree = Tree(self.tree_frame,yscrollcommand=self.tree_scroll.set)
        
        self.tree.pack()
        #bind the double click to method
        self.tree.bind('<<TreeviewSelect>>',self.clicking)
        self.bind('<Return>',self.checkEnterEvent)
        #self.tree.bind("<<TreeviewSelect>>",self.print_element)
        self.tree_scroll.config(command=self.tree.yview)
    
    
    def add_columns_and_heading(self)->None:
        #define columns
        self.tree['columns'] =  ('keuze','Producten','Opmerking')
        #fromate the columns
        
        self.tree.column('#1', minwidth=25, width=50)
        self.tree.column('#2',anchor=W,width=400)
        self.tree.column('#3',anchor=W,width=800)

        #create Heading
        self.tree.heading('keuze', text="keuze", anchor='w')
        self.tree.heading("Producten",text='Product',anchor=W)
        self.tree.heading('Opmerking',text='Opmerkinge',anchor=W)

    def add_data(self)->None:
        '''add data to the headings and columns'''
        for i,data in self.df.dataframe.iterrows():
            self.tree.insert(parent='',index='end',iid=i,text='',values=('',data[0],data[1]))
            


    def labels(self)->None:
        '''Handles the labels'''
        self.product_label = Label(self.add_frame, text='Product')
        self.product_label.grid(row=0,column=0)

        self.opmerking_label = Label(self.add_frame, text='Opmerking')
        self.opmerking_label.grid(row=0,column=1)
     
    def entry_Boxes(self)->None:
        #Entry boxes
        self.product_box = Entry(self.add_frame,width=50,)
        self.product_box.grid(row=1,column=0)

        self.opmerking_box = Entry(self.add_frame,width=100)
        self.opmerking_box.grid(row=1,column=1)

    def buttons(self)->None:

        send_button = Button(self,text='SEND NUDES',command=self.send)
        send_button.pack(pady=10)
        #Remove ONE
        remove_one = Button(self,text='RemoveChecks',command=self.removeChecks)
        remove_one.pack(pady=10)

        
    

    def product_toevoegen(self)->None:
        '''Toevoegen van producten'''
        #products box must be filled in
        if self.product_box.get() == '' or self.product_box.get() == ' ':
            return
    
        temp_array = [self.product_box.get(),self.opmerking_box.get()] 
        self.df.update_df_toevoegen(temp_array)
        self.update_screen()
        #clear boxes
        self.product_box.delete(0,END)
        self.opmerking_box.delete(0,END)
    
    def update_product(self)->None:
        '''Updates Selected data from Frame'''
        print(f'flag in update_prduct:{self.selected_record}')
        selected= self.tree.focus()
        # Save new data
        #print(selected)
        self.tree.item(selected, text='',value=('',self.product_box.get(),self.opmerking_box.get()))
        self.df.update_df(selected,self.product_box.get(),self.opmerking_box.get())
        #clear boxes
        self.update_screen()
        self.product_box.delete(0,END)
        self.opmerking_box.delete(0,END)
        self.selected_record=False

    def delete_buffer_in_labels(self):
        if len(self.tree.selection()) <= 0:
            return        
        self.tree.selection_remove(self.tree.selection()[0])

    def checkEnterEvent(self,event=None):
        """Handles ENTER EVENT"""
        if self.selected_record:
            print('AAAN')
            print(f'flag in check: {self.selected_record}')
            self.update_product()
            self.selected_record= False
            #deselect items
            self.delete_buffer_in_labels()
            #clear boxes
            return
        print('UIT')
        print(f'flag in check: {self.selected_record}')
        self.product_toevoegen()
        self.selected_record=False
    
    def removeAll(self)->None:
        '''Removes all the data from Frame'''
        for record in self.tree.get_children():
            self.tree.reset_checks()
            self.tree.delete(record)
            

    def removeChecks(self)->None:
        '''Removes Selected data from Frame'''
        print(f'removeChecks: {self.tree.get_checks()}')
        self.df.update_df_remove(self.tree.get_checks())
        self.update_screen()
            

    def update_screen(self)->None:
        """Update the scree: remove all the data from screen; add all the data to the screen
        dataframe must be well indexed"""
        self.removeAll()
        self.add_data()

    def selectRecord(self)->None:
        '''Double click event Handler, gets the data selected and pass it to labels'''
        
        self.product_box.delete(0,END)
        self.opmerking_box.delete(0,END)
        # Grab record number
        selected= self.tree.focus()
        # Grab record value
        value = self.tree.item(selected,'values')
        #output to entry boxes
        self.product_box.insert(0,value[1])
        self.opmerking_box.insert(0,value[2])
        #boolean flag 
        self.selected_record = True
    #create binding click function
    def clicking(self,e)->None:
        '''handles click event'''
        self.selectRecord()
        print(f'flag in clickEvent: {self.selected_record}')

    def send(self)->None:
        '''Sends the selected data to Email'''
        indexes = list(self.tree.checks)
        self.df.send_email(indexes)
        self.update_screen()
        print(indexes)
    

    def on_closing(self):
        '''HANDLES CLOSING WINDOW -> EVERYTIME IT CLOSES ->SAVES THE DATA'''
        self.df.save_df()
        print('json file saved')
        self.destroy()

