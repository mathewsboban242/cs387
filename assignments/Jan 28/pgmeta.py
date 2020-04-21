import psycopg2
import dbexec
from dbmeta import Meta, Table, Column

def get_meta_data(conn):
    """Populates a dbmeta.Meta object with Tables, Columns and inter-Table relationships"""
    meta = Meta()
    load_columns(conn, meta)  # Same query as exercise 1.
    # 1/0
    constraints = load_table_constraints(conn) # constraint_name -> table mapping
    load_relationships(conn, meta, constraints)
    return meta

def load_columns(conn, meta: Meta):
    c = conn.cursor()
    query = """
with A(table_name,column_name,is_pk) as(
    select distinct co.table_name, co.column_name,'*' as is_pk
    from information_schema.columns as co left outer join information_schema.key_column_usage as kc on (co.table_name) = (kc.table_name)
    where co.table_schema='public'
    order by co.table_name
),
B(table_name,column_name,is_pk) as(
select distinct table_name,column_name,'*' as is_pk
from information_schema.table_constraints natural join information_schema.key_column_usage
where constraint_type='PRIMARY KEY'
),
M as ((select * from A) except (select * from B)),
C(table_name,column_name,is_pk) as (
select table_name,column_name,'' as is_pk
from M
),
D(table_name,column_name,is_pk) as (
select *
from ((select * from B) union (select * from C)) as M1
),
E(table_name,column_name,is_pk,data_type)as(
select table_name,column_name,is_pk,data_type
from information_schema.columns natural join D
)
select * from E
order by table_name, case when is_pk='*' THEN 1 else 0 end DESC, column_name DESC;
    """
    (header, rows) = dbexec.exec_query(conn, query);
    tables = set()
    for row in rows:
        # TODO: create Table and Column objects and attach to meta.
        # print(row)
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
        table_constraints[row[2]] = row[5]

    c.close()
    return table_constraints

def load_relationships(conn, meta, constraints):
    c = conn.cursor()

    # TODO : query referential_constraints table, which maps constraint in one table
    #      : to unique constraint in another table
    # TODO : for each row create meta.tables[from_table].refersTo += meta.tables[to_table]

    query = 'select distinct constraint_name, unique_constraint_name from information_schema.referential_constraints'
    (header, rows) = dbexec.exec_query(conn, query);

    for row in rows:
        if(meta.tables[constraints[row[1]]] not in meta.tables[constraints[row[0]]].refersTo):
            meta.tables[constraints[row[0]]].refersTo.append(meta.tables[constraints[row[1]]])
    
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
