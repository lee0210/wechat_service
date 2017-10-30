from . import dbc
import uuid
import datetime
import traceback

class query_builder(object):
    def __init__(self):
        self.sql = ''
        self.converter = dbc.converter()
        self.data = {'columns':'','table':'','where':'','order':'','group':'','limit':'','option':''}
    def table(self, table, alias = ''):
        self.data['table'] = table if alias == '' else '%s as %s'%(table, alias)
        return self
    def select(self, *columns):
        return self
    def insert(self, table, alias = ''):
        return self
    def update(self, table, alias = ''):
        return self
    def delete(self, table, alias = ''):
        return self
    def where(self, key={}):
        return self
    def orderby(self, *columns):
        self.data['order'] = 'order by ' + ','.join(columns)
        return self
    def groupby(self, *columns):
        self.data['group'] = 'group by ' + ','.join(columns)
        return self

class sql(object):
    def __init__(self):
        self.converter = dbc.converter()
    def table(self, table):
        self.table = table
        return self
        
    def read_in(self, keys, orderby=[], lock=False, iteration=False):
        if keys == []:
            return None;
        sql = 'select * from %(table)s %(where)s %(order)s %(option)s'
        sql_data = {'table' : self.table, 'where' : '', 'order' : '', 'option' : ''}
        if lock:
            if not dbc.in_transaction():
                 raise RuntimeError('Not in transaction but trying to use lock')
            sql_data['option'] = 'for update'
        in_list = []
        one_key = '(%s)' % ','.join(['%({0})s'.format(k) for k in keys[0].keys()])
        for key in keys:
            d = {}
            for k, v in key.items():
                conv = v
                conv = self.converter.to_mysql(conv)
                conv = self.converter.escape(conv)
                conv = self.converter.quote(conv)
                d[k] = conv.decode('utf-8')
            in_list.append(one_key % d)
        sql_data['where'] = 'where (%s) in (%s)' % (','.join(keys[0].keys()), ','.join(in_list))
        if orderby != []:
            sql_data['order'] = 'order by ' + ','.join(orderby)
        sql = sql % sql_data
        print(sql)
        try:
            c = None
            c = dbc.connect().cursor(buffered=True, dictionary=True) 
            c.execute(sql)
            rt = c.fetchall()
            if iteration:
                self.rt = rt
                return self
            return rt
        except Exception as e:
            raise e
        finally:
            if c is not None: c.close()
         
        
    def read(self, key={}, orderby=[], lock=False, iteration=False):
        sql = 'select * from %(table)s %(where)s %(order)s %(option)s'
        sql_data = {'table' : self.table, 'where' : '', 'order' : '', 'option' : ''}
        if lock:
            if not dbc.in_transaction():
                 raise RuntimeError('Not in transaction but trying to use lock')
            sql_data['option'] = 'for update'
        if key != {}:
            sql_data['where'] = 'where ' + ' and '.join(['{0}=%({0})s'.format(k) for k, v in key.items()]) 
        if orderby != []:
            sql_data['order'] = 'order by ' + ','.join(orderby)
        sql = sql % sql_data
        try:
            c = None
            c = dbc.connect().cursor(buffered=True, dictionary=True) 
            c.execute(sql, key)
            rt = c.fetchall()
            if iteration:
                self.rt = rt
                return self
            return rt
        except Exception as e:
            raise e
        finally:
            if c is not None: c.close()

    def write(self, data):
        sql = 'insert into %(table)s(%(column)s) value(%(data)s)'
        sql_data = {'table' : self.table, 'column' : '', 'data' : ''}
        sql_data['column'] = ','.join([k for k, v in data.items()])
        sql_data['data'] = ','.join(['%({0})s'.format(k) for k, v in data.items()])
        sql = sql % sql_data
        try:
            c = None
            c = dbc.connect().cursor(buffered=True, dictionary=True) 
            c.execute(sql, (data))
        except Exception as e:
            raise e
        finally:
            if c is not None: c.close()
        
    def update(self, data, key={}):
        sql = 'update %(table)s set %(data)s %(where)s'
        sql_data = {'table' : self.table, 'data' : '', 'where' : ''}
        sql_data['data'] = ','.join(['{0}=%(d{0})s'.format(k) for k, v in data.items()])
        data = {'d'+k : v for k, v in data.items()}
        if key != {}:
            sql_data['where'] = 'where ' + ' and '.join(['{0}=%(k{0})s'.format(k) for k, v in key.items()]) 
            key = {'k'+k : v for k, v in key.items()}
        sql = sql % sql_data
        data.update(key)
        try:
            c = None
            c = dbc.connect().cursor(buffered=True, dictionary=True) 
            c.execute(sql, (data))
        except Exception as e:
            raise e
        finally:
            if c is not None: c.close()

    def delete(self, key={}):
        sql = 'delete from %(table)s %(where)s'
        sql_data = {'table' : self.table, 'where' : ''}
        if key != {}:
            sql_data['where'] = 'where ' + ' and '.join(['{0}=%({0})s'.format(k) for k, v in key.items()]) 
        sql = sql % sql_data
        #print(sql)
        try:
            c = None
            c = dbc.connect().cursor(buffered=True, dictionary=True) 
            c.execute(sql, (key))
        except Exception as e:
            raise e
        finally:
            if c is not None: c.close()

    def __iter__(self):
        for rt in self.rt:
            yield rt
if __name__ == '__main__':
    dbc.connect()
    for i in range(0, 5):
        sql().table('images_unit_test').write({
            'id': uuid.uuid1().hex,
            'name': 'test{0}.jpg'.format(i),
            'path': '/test/test{0}.jpg'.format(i),
            'ctime': datetime.datetime.now(),
        })
    in_list = []
    for i in range(0, 5):
       in_list.append({
            'name': 'test{0}.jpg'.format(i),
            'path': '/test/test{0}.jpg'.format(i),
       }) 
    sql().table('images_unit_test').update({'path': 'fuck you'}, {'name': 'test1.jpg'})
    for i in sql().table('images_unit_test').read_in(in_list, iteration=True):
        print(i)
    sql().table('images_unit_test').delete()
    print(sql().table('images_unit_test').read(orderby=['name']))

    print(sql().table('test').read_in([{'id': 1, 'f1': 1, 'f2': 1},{'id': 1, 'f2': 3, 'f1': 2}]))

    dbc.close()


