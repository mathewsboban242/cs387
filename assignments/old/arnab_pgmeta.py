import psycopg2
import dbexec
from dbmeta import Meta, Table, Column

def get_meta_data(conn):
    """Populates a dbmeta.Meta object with Tables, Columns and inter-Table relationships"""
    meta = Meta()
    load_columns(conn, meta)  # Same query as exercise 1.
    constraints = load_table_constraints(conn) # constraint_name -> table mapping
    load_relationships(conn, meta, constraints)
    return meta

def load_columns(conn, meta):
    c = conn.cursor()
    query = '''select c1.table_name, c1.column_name, replace(replace(replace(c2.constraint_type,'CHECK_KEY',''), 'FOREIGN KEY',''), 'PRIMARY KEY' ,'*'), 
    data_type FROM information_schema.columns c1, information_schema.table_constraints c2, information_schema.key_column_usage c3  WHERE c2.table_schema = 'public' and
    c1.table_name = c3.table_name and
    c1.column_name = c3.column_name and
    c1.table_name = c2.table_name and
    c3.table_name = c2.table_name
    ORDER BY c1.table_name, case
    when constraint_type='PRIMARY_KEY' THEN 1
    else 0
    END, constraint_type DESC,
    c1.column_name;'''
    (header, rows) = dbexec.exec_query(conn, query);

    tables = set()

    for row in rows:
        #TODO: create Table and Column objects and attach to meta. 
        if row[0] not in tables:
            tables.add(row[0])
            tbl = Table(name=row[0])
        tbl.columns.append(Column(name=row[1], table = tbl, data_type = row[3], is_pk = (row[2]=='*')))
        meta.tables[tbl.name] = tbl
    c.close()

def load_table_constraints(conn):
    table_constraints = dict() # Map of constraint name -> containing table name
    c = conn.cursor()

    # TODO: Load table_constraints table for primary and foreign keys, and record
    # the constraint_table and the containing table name.
    query = "select * from information_schema.table_constraints where constraint_type = 'PRIMARY KEY' or constraint_type = 'FOREIGN KEY'"
    (header, rows) = dbexec.exec_query(conn, query);

    for row in rows:
        #if row[2].split('_')[-1] == 'fkey' or row[2].split('_')[-1] == 'pkey':
        table_constraints[row[2]] = row[5]

    c.close()
    return table_constraints

def load_relationships(conn, meta, constraints):
    c = conn.cursor()

    # TODO : query referential_constraints table, which maps constraint in one table
    #      : to unique constraint in another table
    # TODO : for each row create meta.tables[from_table].refersTo += meta.tables[to_table]

    query = 'select * from information_schema.referential_constraints'
    (header, rows) = dbexec.exec_query(conn, query);

    for row in rows:
        meta.tables[constraints[row[2]]].refersTo.append(meta.tables[constraints[row[5]]])
    
    c.close()
    
def to_graph(meta):
    str = ""
    for tbl in meta.tables.values():
        str += "[" + tbl.name + "|"
        str += "|".join([col.name for col in tbl.columns])
        str += "]\n"
        for t in tbl.refersTo:
            str += "[%s] -> [%s]\n"%(tbl.name, t.name)
    return str

if __name__ == "__main__":
    import config
    conn = dbexec.connect()
    meta = get_meta_data(conn) # returns dbmeta 'Meta'
    conn.close()
    print(to_graph(meta))
