from faker import Faker
import sqlite3

conn = sqlite3.connect('contacts.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS contacts(
            name TEXT,
            number TEXT,
            email TEXT,
            PRIMARY KEY (name, number, email)
            )''')

faker = Faker()
keys = ['NAME','PHONE NUMBER','EMAIL',]


def generate_fake_data(rows):
    data = []
    for _ in range(rows):
        list_data = {
            'name': faker.name(),
            'number': ''.join(filter(str.isdigit, faker.phone_number())),
            'email': faker.email(),
        }
        data.append(list_data)
    return data

def main():
    rows = int(input("How Much Rows YOu Want : "))
    data = generate_fake_data(rows)
    for row in data:
        cur.execute('INSERT INTO contacts VALUES(?,?,?)',(row['name'],row['number'],row['email']))
    conn.commit()

if __name__ == '__main__':
    try:
        main()
    finally:
        conn.close