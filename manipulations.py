import sqlite3

conn = sqlite3.connect('films.db')
c = conn.cursor()

c.execute('''  
SELECT * FROM films
          ''')
for col in c:
    print('Title =', col[1])
    print('Cert =', col[6])
    print()

conn.close()