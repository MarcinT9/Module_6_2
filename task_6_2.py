import sqlite3
from sqlite3 import Error, paramstyle


def create_connection(db_file):
    """ create a database connection to a SQLite database 
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def execute_sql(conn, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def add_student(conn, student):
    """
    Create a new student into the students table
    :param conn:
    :param student:
    :return: student id
    """
    sql = '''INSERT INTO students(id, first_name, last_name, start_year, study_year)
            VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, student)
    conn.commit()
    return cur.lastrowid

def add_subject(conn, subject):
    """
    Create a new subject into the subjects table
    :param conn:
    param subject:
    :return: subject id
    """
    sql = '''INSTER INTO subjects(subject_id, name, description, hours_a_year, year_of_study)
            VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, subject)
    conn.commit()
    return cur.lastrowid

def select_all(conn, table):
    """
    Query all rows in the table
    :param comm: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM {table}')
    rows = cur.fetchall()
    return rows

def select_where(conn, table, **query):
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param table: table name
    :param query: dict of attributes and values
    :return:
    """
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f'{k}=?')
        values += (v,)
    q = ' AND '.join(qs)
    cur.execute(f'SELECT * FROM {table} WHERE {q}', values)
    rows = cur.fetchall()
    return rows

def update(conn, table, id, **kwargs):
    """
    Update status, statr_date and end_date of a task
    :param conn:
    :param table: table name
    :param id: row id
    :return:
    """
    parameters = [f'{k} = ?' for k in kwargs]
    parameters = ', '.join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id, )

    sql = f''' UPDATE {table}
            SET {parameters}
            WHERE id = ?'''

    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print('OK')
    except sqlite3.OperationalError as e:
        print(e)

def delete_where(conn, table, **kwargs):
    """
    Delete from table where attributes from
    :para conn: Connection to the SQLite database
    :param table: table name
    :para kwargs: dict of attributes and values
    :return:
    """
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f'{k}=?')
        values += (v, )
    q = ' AND '.join(qs)

    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print('Delete')

def delete_all(conn, table):
    """
    Delete all rows from table
    :param conn: Connection to the SQlite database
    :param table: table name
    :return:
    """
    sql = f'DELETE FROM {table}'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print('Delete')


if __name__ == "__main__":

    create_students_sql = """
    -- students table
    CREATE TABLE IF NOT EXISTS students (
        id integer PRIMARY KEY,
        fitst_name text NOT NULL,
        last_name text NOT NULL,
        start_year text,
        study_year text
    );
    """

    create_subjects_sql = """
    -- subjects table
    CREATE TABLE IF NOT EXISTS subjects (
        id integer PRIMARY KEY,
        student_id integer NOT NULL,
        name VARCHAR(250) NOT NULL,
        description TEXT,
        hours_a_year VARCHAR(15) NOT NULL,
        year_of_study VARCHAR(15) NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (id)
        );
        """

    conn = create_connection("database.db")
    if conn is not None:
        execute_sql(conn, create_students_sql)
        execute_sql(conn, create_subjects_sql)
        conn.close()