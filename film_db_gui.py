from tkinter import *
from tkinter import messagebox
import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="guest",
        database="IMDb"
    )
except:
    print("SQL DB not found. Creating new one.")

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="guest"
    )
    mycursor = db.cursor()
    mycursor.execute("CREATE DATABASE IMDb")
    db.commit()
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="guest",
        database="IMDb"
    )
    mycursor = db.cursor()
    Q1 = "CREATE TABLE films (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(50), director VARCHAR(50))"
    mycursor.execute(Q1)
    db.commit()

mycursor = db.cursor()


root = Tk()
root.title('Film Database')
root.geometry('600x250')

def select(variable):
    # label = Label(update_window, text=variable.get()).pack()
    global ID_reference
    sTitle = variable
    SQLcommand = "SELECT * FROM films WHERE title = %s"
    mycursor.execute(SQLcommand, sTitle)
    data = mycursor.fetchall()
    title_entry.delete(0, 'end')
    director_entry.delete(0, 'end')
    # print(data)
    title_entry.insert(0, data[0][1])
    # first 0 is the insert into entry widget (so at the start), second is which list (because we might bring up more than one)
    # , third is the item in the list we want
    director_entry.insert(0, data[0][2])
    ID_reference = data[0][0] # database ID number, when we edit the button will use this number to overwrite/update what is in that ID
    # print(ID_reference)

def closing_update_database():
    update_btn.config(state=NORMAL)
    update_window.destroy()

def update_database():
    global update_window, variable, title_entry, director_entry
    update_window = Toplevel()
    update_window.title('Update Entry')
    update_window.geometry('700x250')

    update_btn.config(state=DISABLED)
    update_window.protocol("WM_DELETE_WINDOW", closing_update_database)

    mycursor.execute("SELECT title FROM films")
    sql_label = mycursor.fetchall()
    records_list = []
    for x in sql_label:
        title = x
        records_list.append(title)

    variable = StringVar(update_window)
    variable.set("Select Entry")
    drop_down = OptionMenu(update_window, variable, *records_list, command=select)
    drop_down.pack()

    title_text = Label(update_window, text="Update Title Entry")
    title_text.pack()
    title_entry = Entry(update_window, width=35, font=(20), borderwidth=5)
    title_entry.pack()
    director_text = Label(update_window, text="Update Director Entry")
    director_text.pack()
    director_entry = Entry(update_window, width=35, font=(20), borderwidth=5)
    director_entry.pack()
    update_button = Button(update_window, text="Update Entry", command=update_entry)
    update_button.pack()

def update_entry():
    new_title = title_entry.get()
    new_dir = director_entry.get()
    #SQL_arguement = "UPDATE films SET title = %s, director = %s WHERE ID = %s"
    mycursor.execute("UPDATE films SET title = %s, director = %s WHERE ID = %s", (new_title, new_dir, ID_reference))
    db.commit()
    title_entry.delete(0, 'end')
    director_entry.delete(0, 'end')
    messagebox.showinfo("", "Entry was updated succesfully")
    # confirm_text = Label(update_window, text="Database has been updated").pack()

def close_delete_db():
    delete_button.config(state=NORMAL)
    delete_window.destroy()

def delete_database():
    global title_entry, director_entry, delete_window
    delete_window = Toplevel()
    delete_window.title('Delete Entry')
    delete_window.geometry('700x250')

    delete_button.config(state=DISABLED)

    mycursor.execute("SELECT title FROM films")
    sql_label = mycursor.fetchall()
    records_list = []
    for x in sql_label:
        title = x
        records_list.append(title)

    variable = StringVar(delete_window)
    variable.set("Select Entry")
    drop_down = OptionMenu(delete_window, variable, *records_list, command=select)
    drop_down.pack()

    title_text = Label(delete_window, text="Update Title Entry")
    title_text.pack()
    title_entry = Entry(delete_window, width=35, font=(20), borderwidth=5)
    title_entry.pack()
    director_text = Label(delete_window, text="Update Director Entry")
    director_text.pack()
    director_entry = Entry(delete_window, width=35, font=(20), borderwidth=5)
    director_entry.pack()
    delete_entry_btn = Button(delete_window, text="Delete Entry", command=delete)
    delete_entry_btn.pack()
    delete_window.protocol("WM_DELETE_WINDOW", close_delete_db)
                        # DELETE_WINDOW regardless of window name, just happens to have same name.

def delete():
    response = messagebox.askyesno("Warning!", "Do you wish to delete this entry?")
    # yes = 1, no = 0, you'd think with 0 being 1 in list it be flipped but it isn't
    if response == 1:
        mycursor.execute("DELETE FROM films WHERE ID = " + str(ID_reference))
        # doing %s then ID_reference kept getting a "Could not process parameters error", even when we make it a string and
        # despite update_entry doing it that way.
        db.commit()
        title_entry.delete(0, 'end')
        director_entry.delete(0, 'end')
        messagebox.showinfo("", "Entry was deleted succesfully")
        # confirm_text = Label(delete_window, text="Entry has been deleted").pack()
    if response == 0:
        pass

def closing_show_database():
    show_database_btn.config(state=NORMAL)
    database_window.destroy()
def show_database():
    global database_window, update_btn, delete_button
    database_window = Toplevel()
    database_window.title('All Entries')
    database_window.geometry('500x500')

    mycursor.execute("SELECT * FROM films")
    sql_label = mycursor.fetchall()
    print_records = ''
    for x in sql_label:
        print_records += str(x) + "\n"
    show_database_label = Label(database_window, text=print_records)
    show_database_label.pack()

    update_btn = Button(database_window, text="Update Entry", command=update_database)
    update_btn.pack()
    delete_button = Button(database_window, text="Delete Entry", command=delete_database)
    delete_button.pack()

    show_database_btn.config(state=DISABLED)
    database_window.protocol("WM_DELETE_WINDOW", closing_show_database)

def closing_new_entry():
    new_entry_btn.config(state=NORMAL)
    new_entry_window.destroy()
def new_entry():
    global new_entry_window, entry_bar, entry_bar_2
    new_entry_window = Toplevel()
    new_entry_window.title('New Entry')
    new_entry_window.geometry('700x250')

    new_entry_btn.config(state=DISABLED)

    film_title = Label(new_entry_window, text="New film title:").pack()
    entry_bar = Entry(new_entry_window, width=35, font=(20), borderwidth=5)
    entry_bar.pack()
    film_director = Label(new_entry_window, text="New film director:").pack()
    entry_bar_2 = Entry(new_entry_window, width=35, font=(20), borderwidth=5)
    entry_bar_2.pack()
    add_entry_btn = Button(new_entry_window, text="Add Film", command=add_entry).pack()
    new_entry_window.protocol("WM_DELETE_WINDOW", closing_new_entry)

def add_entry():
    mycursor.execute("INSERT INTO films(title, director) VALUES (%s, %s)", (entry_bar.get(), entry_bar_2.get()))
    db.commit() # Q1 method causes connection error, but having the input equal an object works (no idea why)
    entry_bar.delete(0, 'end')
    entry_bar_2.delete(0, 'end')
    messagebox.showinfo("", "New entry added succesfully")
    new_entry_btn.config(state=NORMAL)
    new_entry_window.destroy()
    # 0, 'end' is from start to finish even though arguement is a string

def clear_database():
    response = messagebox.askokcancel(title="Confirm", message="This action cannot be undone. Do you wish to proceed?")
    if response == 1:
        mycursor.execute("DELETE FROM films;")
        db.commit()
        SQLcommand = "ALTER TABLE films AUTO_INCREMENT = 1"
        mycursor.execute(SQLcommand)
        messagebox.showinfo("", "Database successfully cleared.")
    if response == 0:
        pass

show_database_btn = Button(root, text="Show Database", command=show_database)
show_database_btn.pack()
new_entry_btn = Button(root, text="Add new entry", command=new_entry)
new_entry_btn.pack()
clear_database_btn = Button(root, text="Clear Database", command=clear_database)
clear_database_btn.pack(pady=50)

root.mainloop()


# remember edit function needs to COMMIT() any changes
