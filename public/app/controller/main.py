import psycopg2
from flask import (
    Blueprint, jsonify, render_template, request
)


import pandas as pd

bp = Blueprint('main', __name__)
con = psycopg2.connect(database='postgres', user='postgres', password='password', host='postgresdb.cnxya6luktyc.ap-southeast-1.rds.amazonaws.com', port='5432')

@bp.route('/')
def index():
    return render_template('main/index.html',
                           title='Dashboard')

@bp.route('/add')
def add():
    return render_template('main/add.html',
                           title='Add Employee')

# GET all users
@bp.route('/users')
def getUsers():

    maxSalary = request.args.get('maxSalary')
    minSalary = request.args.get('minSalary')
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    sortQuery = request.args.get('sort')
    
    if not limit:
        limit = 30
    
    if not offset:
        offset = 0

    # con = psycopg2.connect(database='postgres', user='postgres', password='password', host='postgresdb.cnxya6luktyc.ap-southeast-1.rds.amazonaws.com', port='5432')
    cur = con.cursor()

    sql = '''
    SELECT emp_id, login, name, salary
	FROM public.employees'''

    if minSalary and maxSalary:
        sql +=  '''
        where salary >= {0} and salary <= {1}
        '''.format(minSalary,maxSalary)
    elif minSalary:
        sql +=  '''
        where salary >= {0}
        '''.format(minSalary)
    elif maxSalary:
        sql +=  '''
        where salary <= {0}
        '''.format(maxSalary)

    if sortQuery:
        order = sortQuery[0:2]
        orderQuery = ''
        if order == '43':
            orderQuery = 'desc'
        elif order == '45':
            orderQuery = 'asc'
        else:
            return("Sort is not in right format",400)

        colName = sortQuery[2:]
        if colName == 'id':
            colName = 'emp_id'

        validateCol = ['emp_id','login','name','salary']
        if colName not in validateCol:
            return("Sort is not in right format",400)

        sql += '''
        order by {0} {1}
        ''' .format(colName,orderQuery)
        
    sql += '''
	OFFSET {0} ROWS
	FETCH FIRST {1} ROW ONLY;
    '''.format(offset,limit)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) > 0:
        json_data=[]
        for result in rows:
            content = {'id': result[0], 'login': result[1], 'name': result[2], 'salary': float(result[3])}
            json_data.append(content)
            content = {}  
        # return json.dumps(json_data)
    cur.close()

    return jsonify({'result':json_data})


@bp.route('/users', methods=['POST'])
def createUser():
    json = request.json
    if json:
        try:
            # con = psycopg2.connect(database='postgres', user='postgres', password='password', host='postgresdb.cnxya6luktyc.ap-southeast-1.rds.amazonaws.com', port='5432')
            cur = con.cursor()
            sql='''
            INSERT INTO public.employees(
            emp_id, login, name, salary)
            VALUES ('{0}','{1}','{2}',{3});
            '''.format(json['id'],json['login'],json['name'],json['salary'])
            cur.execute(sql)
            con.commit()
            cur.close()
            return("User created successfully")

        except psycopg2.errors.UniqueViolation as e:
            return("User already exist in database",400)

@bp.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    json = request.json
    if json:
        # try:
        # con = psycopg2.connect(database='postgres', user='postgres', password='password', host='postgresdb.cnxya6luktyc.ap-southeast-1.rds.amazonaws.com', port='5432')
        cur = con.cursor()
        sql='''
        UPDATE public.employees
        set 
        '''
        
        temp_sql = []

        if 'id' in json:
            if json['id']:
                temp_sql.append('''
                emp_id = '{0}'
                '''.format(json['id']))
        
        if 'login' in json:
            if json['login']:
                temp_sql.append( '''
                login = '{0}'
                '''.format(json['login']))

        if 'name' in json:
            if json['name']:
                temp_sql.append( '''
                name = '{0}'
                '''.format(json['name']))

        if 'salary' in json:
            if json['salary']:
                temp_sql.append('''
                salary = '{0}'
                '''.format(json['salary']))

        if temp_sql:
            if len(temp_sql) == 1:
                sql+=temp_sql[0]
            else:
                sql+=','.join(temp_sql)

        sql+='''
        WHERE emp_id = '{0}'
        '''.format(id)

        print(sql)
        cur.execute(sql)
        con.commit()
        cur.close()
        return("User updated successfully")

        # except psycopg2.errors.UniqueViolation as e:
        #     return("User already exist in database",400)

@bp.route('/users/<id>')
def getUser(id):
    
    # con = psycopg2.connect(database='postgres', user='postgres', password='password', host='postgresdb.cnxya6luktyc.ap-southeast-1.rds.amazonaws.com', port='5432')
    cur = con.cursor()

    sql = '''
    SELECT emp_id, login, name, salary
	FROM public.employees
	where emp_id = '{0}'
    '''.format(id)

    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) > 0:
        for row in rows:
            content = {'id': row[0], 'login': row[1], 'name': row[2], 'salary': float(row[3])}
            return(jsonify({'result':[content]}))
    else:
        return("No user with this ID exist",400)

@bp.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    # con = psycopg2.connect(database='postgres', user='postgres', password='password', host='postgresdb.cnxya6luktyc.ap-southeast-1.rds.amazonaws.com', port='5432')
    cur = con.cursor()

    sql = '''
    DELETE FROM public.employees
	WHERE emp_id='{0}';
    '''.format(id)

    cur.execute(sql)
    con.commit()
    cur.close()
    return("Deleted user with id",id)

@bp.route('/users/upload', methods=['POST'])
def uploadUsers():
    # get the uploaded file
    if request.files['file']:
        uploaded_file = request.files['file']
        message = parseCSV(uploaded_file)
    print(message)
    # return status code 400 if file is not uploaded
    if message == "Successful upload":
        return(message,200)
    else:
        return(message,400)

def parseCSV(file):
    
    try:
        col_names = ['id','login','name', 'salary']
        csvData = pd.read_csv(file,names=col_names, header=None)
        # ignore lines that with id that contains #
        csvData = csvData[csvData['id'].str.contains('#') == False]

        duplicateId = csvData['id'].duplicated().sum()
        duplicateLogin = csvData['login'].duplicated().sum()
        nonPositiveSalary = (pd.to_numeric(csvData['salary']) < 0).sum()

        if duplicateId == 0 and duplicateLogin == 0:
            if nonPositiveSalary == 0:
                message = updateDB(csvData)
                return(message)
                    
            else:
                return("Unsuccessful upload, Negative salary")
        else:
            return("Unsuccessful upload, Duplicated id/login")
    
    except pd.errors.EmptyDataError as e:
        return("Unsuccessful upload, Empty File")

    except KeyError as e:
        return("Unsuccessful upload, Columns are not right")
    
    except ValueError as e:
        return("Unsuccessful upload, Salary is not decimal value")

def updateDB(csvData):

    # con = psycopg2.connect(database='postgres', user='postgres', password='password', host='postgresdb.cnxya6luktyc.ap-southeast-1.rds.amazonaws.com', port='5432')
    cur = con.cursor()

    for i,row in csvData.iterrows():
        if row['id'].startswith('#'):
            print("Comment")
        else:
            try:
                sql = '''
        INSERT INTO public.employees (emp_id, login, name, salary)  
    VALUES ('{0}','{1}','{2}',{3})
    ON CONFLICT (emp_id) DO UPDATE 
    SET 
        login = excluded.login,
        name = excluded.name, 
        salary = excluded.salary;
    '''.format(row['id'],row['login'],row['name'],row['salary'])
                print(sql)
                cur.execute(sql)
                con.commit()
            except psycopg2.errors.UniqueViolation:
                return("Unsuccessful upload, login already exist")
    cur.close()
    return("Successful upload")

    

    
