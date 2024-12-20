import sqlite3
import os
from tabulate import tabulate
import time

db_name = 'contacts.db'

def pause(n):
    time.sleep(n)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class ContactManager:
    def __init__(self):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS contacts
                    (name TEXT NOT NULL,
                    number TEXT PRIMARY KEY NOT NULL,
                    email TEXT NOT NULL)''')
        self.conn.commit()
    
    def add_contact(self,name,number,adress):
        self.cur.execute('INSERT INTO contacts VALUES(?,?,?)',(name,number,adress))
        print(f'Contact With Name {name} Added Successfuly !')
        self.conn.commit()
        pause(2)
        clear()
    
    def remove_contact(self,name):
        self.cur.execute('DELETE FROM contacts WHERE name =?',(name,))
        self.conn.commit()
        print(f"Contact With Name {name} Removed Permanently !")
        pause(2)
        clear()
    
    def update_contact(self,name,name1=None,number=None,email=None):
        row = self.cur.execute('SELECT * FROM contacts WHERE name=?',(name,)).fetchall()
        name0 = row[0][0]
        number0 = row[0][1]
        email0 = row[0][2]
        if not name1:
            name1 = name0
        if not number:
            number = number0
        if not email:
            email = email0
        self.cur.execute('UPDATE contacts SET name=?, number=?, email=? WHERE name=?',(name1,number,email,name))
        self.conn.commit()
        print(f"Contact With Name {name} Updated Successfuly")

    def view_contacts(self):
        headers = ["NAME","NUMBER","EMAIL"]
        self.row = self.cur.execute("SELECT * FROM contacts")
        print(tabulate(self.row, headers=headers,tablefmt='grid'))
    
    def MainMenu(self):
        while True:
            print("Welcome To Our Contact Manager!")
            print("1. Add Contact")
            print("2. Remove Contact")
            print("3. Update Contact")
            print("4. View Contacts")
            print("5. Exit")

            try:
                option = int(input("Choose An Option From Above (1-5)"))
            except ValueError:
                print("Enter A Valid Number")
                continue

            if option == 1:
                name = input("Enter The Name : ")
                number = input("Enter The Number : ")
                email = input("Enter The Email : ")
                self.add_contact(name,number,email)
            elif option == 2:
                name = input("Enter The Name Of The Contact To Delete :")
                self.cur.execute('SELECT name FROM contacts')
                names = [row[0] for row in self.cur.fetchall()]
                if not name in names:
                    print("There is no contact with this name")
                    continue
                self.remove_contact(name)
            elif option == 3:
                name = input("Enter The Name Of The Contact To Delete :")
                self.cur.execute('SELECT name FROM contacts')
                names = [row[0] for row in self.cur.fetchall()]
                if not name in names:
                    print("There is no contact with this name")
                    continue
                name1 = input("Enter The New Name (keep it empty for no changes) : ")
                number = input("Enter The New Number (keep it empty for no changes) : ")
                email = input("Enter The New Email (keep it empty for no changes) : ")
                self.update_contact(name,name1,number,email)
            elif option == 4:
                self.view_contacts()
            elif option == 5:
                print("Stopping Program ...")
                pause(2)
                clear()
                break
    
    def __del__(self):
        self.conn.close()

if __name__ == '__main__':
    contact_manager = ContactManager()
    contact_manager.MainMenu()