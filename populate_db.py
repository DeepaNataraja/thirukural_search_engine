import psycopg2
import pandas as pd

def db_connection():
    try:
        conn = psycopg2.connect(
            database="Thirukural_db",
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None, None

def populate_db():
    conn, cursor = db_connection()
    if conn is None or cursor is None:
        print("Database connection failed.")
        return

    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS kural (
                            id SERIAL PRIMARY KEY,
                            chapter_number INTEGER NOT NULL,
                            couplet_number INTEGER NOT NULL,
                            couplet_text TEXT NOT NULL,
                            meaning TEXT NOT NULL
                        )''')
        print("Table created or already exists.")
        
        # Read the Excel file using pandas
        df = pd.read_excel(r'C:\Users\DC DC\Desktop\thirukural.csv.xlsx', engine='openpyxl')
        print("DataFrame columns:", df.columns)

        # Print the first five rows to debug
        print(df.head(5))

        # Use the actual column names from the DataFrame
        df.columns = [col.strip().lower() for col in df.columns]  # Standardize column names
        
        df['chapter_number'] = pd.to_numeric(df['chapter_number'], errors='coerce')
        df['couplet_number'] = pd.to_numeric(df['couplet_number'], errors='coerce')

        # Drop rows with NaN values (resulting from conversion errors)
        df = df.dropna(subset=['chapter_number', 'couplet_number'])

        # Ensure the columns are integers
        df['chapter_number'] = df['chapter_number'].astype(int)
        df['couplet_number'] = df['couplet_number'].astype(int)

        # Iterate over DataFrame rows and insert data into the database
        for index, row in df.iterrows():
            chapter_number = row['chapter_number']
            couplet_number = row['couplet_number']
            couplet_text = row['couplet_text']
            meaning = row['meaning']
            cursor.execute('''INSERT INTO kural (chapter_number, couplet_number, couplet_text, meaning)
                              VALUES (%s, %s, %s, %s)''', (chapter_number, couplet_number, couplet_text, meaning))
        
        # Commit the transaction
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error during database operations: {e}")
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    populate_db()
