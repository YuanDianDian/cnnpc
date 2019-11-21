import pymysql
import openpyxl
from src_cnnpc import tools

class MySQL:
    '''
    This file creat a MySQL database in your server. And in MySQL class, we can appoint the server ip, user and table name.
    The structure of data will be recorded as follows:
        column name:    com_1       rate_1      com_2       rate_2        accuracy         res_dir

            type：       int        double       int        double         double          vchar(60) 

          meaning:     com_1, rate_1: first compression layer index and its compression rate 
                       com_2, rate_2: second compression layer index and its compression rate 
                       accuracy: the accuracy of this strategy
                       res_dir: the path where program saves the model 
    '''
    def __init__(self, severIp='127.0.0.1', 
                       password=' ', 
                       database='cnnpc', 
                       table='mobilenet_search', 
                       user=' '):
        '''init the parameters'''
        self.severIp = severIp
        self.password = password
        self.database = database
        # self.table = table
        self.user = user

        table = tools.get_net_name() + '_search'
        self.table = table

    def SQL_connect(self):
        '''connect to your server'''
        connect = pymysql.connect(
            host = self.severIp,
            port = 3306,
            user = self.user,
            password = self.password,
            db = self.database,
            charset = 'utf8'
        )  
        if(not connect):
            print("Failed to connect MySQL!")
        cursor = connect.cursor()  
        return connect, cursor

    def save_result(self, com_1, rate_1, com_2, rate_2, accuracy=0.0, res_dir='NO_DIR_INPUT'):
        '''add one result to MySQL'''
        connect, cursor = self.SQL_connect()
        sql = "INSERT INTO %s (com_1, rate_1, com_2, rate_2, accuracy, res_dir) VALUES ( %d, %.6f, %d, %.6f, %.6f, '%s' )"
        data = (self.table, com_1, rate_1, com_2, rate_2, accuracy, res_dir)
        cursor.execute( sql % data )
        connect.commit()
        print('Successful one group results')        
        cursor.close() # close the connect
        connect.close()  


    def delete_acc(self, com_1, rate_1, com_2, rate_2):
        '''delete one result from MySQL'''
        connect, cursor = self.SQL_connect()
        sql = "DELETE FROM %s WHERE com_1 = %d and rate_1 = %.6f and com_2 = %d and rate_2 = %.6f"
        data = (self.table, com_1, rate_1, com_2, rate_2)
        cursor.execute( sql % data )
        connect.commit()
        print('Successful delete one row!')
        cursor.close()
        connect.close()      


    def search_acc(self, com_1, rate_1, com_2, rate_2):
        '''search the accuracy according to the given strategy'''
        if com_2 == com_1: # judge the compression type
            return self.search_acc_onePar(com_1, rate_1)
        connect, cursor = self.SQL_connect()
        sql = "SELECT accuracy, res_dir FROM %s WHERE com_1 = %d and rate_1 = %.6f and com_2 = %d and rate_2 = %.6f"
        data = (self.table, com_1, rate_1, com_2, rate_2)
        cursor.execute( sql % data )
        result = cursor.fetchall() # if there is no result fit requirement, return NULL 
        cursor.close()
        connect.close()
        return result

    def search_acc_onePar(self, com_1, rate_1):
        '''search the accuracy according to the given strategy (the situation of single layer compression)'''
        connect, cursor = self.SQL_connect()
        sql = "SELECT accuracy, res_dir FROM %s WHERE com_1 = %d and rate_1 = %.6f and com_2 = %d and rate_2 = %.6f"
        data = (self.table, com_1, rate_1, com_1, rate_1)
        cursor.execute( sql % data )    
        result = cursor.fetchall() # if there is no result fit requirement, return NULL 
        cursor.close()
        connect.close()
        return result

    def search_rate2_acc(self, com_1, rate_1, com_2):
        '''search the results from MySQL which have the same com_1 and rate_1'''
        connect, cursor = self.SQL_connect()
        sql = "SELECT rate_2, accuracy, res_dir FROM %s WHERE com_1 = %d and rate_1 = %.6f and com_2 = %d"
        data = (self.table, com_1, rate_1, com_2)
        cursor.execute( sql % data )       
        result = cursor.fetchall() # if there is no result fit requirement, return NULL
        cursor.close()
        connect.close()
        return result

    def search_rate1_acc(self, com_1, com_2, rate_2):
        '''search the results from MySQL which have the same com_2 and rate_2'''
        if com_2 == com_1:
            return self.search_rate1_acc_onePar(com_1, com_2)
        connect, cursor = self.SQL_connect()
        sql = "SELECT rate_1, accuracy, res_dir FROM %s WHERE com_1 = %d and com_2 = %d and rate_2 = %.6f"
        data = (self.table, com_1, com_2, rate_2)
        cursor.execute( sql % data )      
        result = cursor.fetchall() # if there is no result fit requirement, return NULL
        cursor.close()
        connect.close()
        return result

    def search_rate1_acc_onePar(self, com_1, com_2):
        '''search the results from MySQL which have the same com_1'''
        connect, cursor = self.SQL_connect()
        sql = "SELECT rate_1, accuracy, res_dir FROM %s WHERE com_1 = %d and com_2 = %d"
        data = (self.table, com_1, com_2)
        cursor.execute( sql % data )   
        result = cursor.fetchall() # if there is no result fit requirement, return NULL
        cursor.close()
        connect.close()
        return result


    def search_rate1_rate2_acc(self, com_1, com_2):
        '''search the results from MySQL which have the same com_2'''
        connect, cursor = self.SQL_connect()
        sql = "SELECT rate_1, rate_2, accuracy, res_dir FROM %s WHERE com_1 = %d and com_2 = %d"
        data = (self.table, com_1, com_2)
        cursor.execute( sql % data )    
        result = cursor.fetchall() # if there is no result fit requirement, return NULL
        cursor.close()
        connect.close()
        return result


    def change_acc(self, com_1, rate_1, com_2, rate_2, accuracy):
        '''change one result in MySQL'''
        connect, cursor = self.SQL_connect()
        sql = "UPDATE %s SET accuracy = %.6f WHERE com_1 = %d and rate_1 = %.6f and com_2 = %d and rate_2 = %.6f"
        data = (self.table, accuracy, com_1, rate_1, com_2, rate_2)
        cursor.execute( sql % data )
        connect.commit()
        print('Successful change accuracy')
        cursor.close()
        connect.close()


    def get_all_to_excel(self):
        '''save all results to a local excel'''
        connect, cursor = self.SQL_connect()
        sql = "SELECT * FROM %s"
        data = (self.table)
        cursor.execute( sql % data)
        res = cursor.fetchall()
        workbook=openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "All-reslut"
        for row in res:
            worksheet.append(list(row))
        workbook.save('./all-reslut.xlsx')
        print('Successful output excel')
        cursor.close()
        connect.close()

    def search_pureacc(self, com_1, rate_1, com_2, rate_2):
        '''search the accuracy according to the given strategy'''
        if com_2 == com_1: # judge the number of compression layer
            result = self.search_acc_onePar(com_1, rate_1)
        else:    
            connect, cursor = self.SQL_connect()
            sql = "SELECT accuracy FROM %s WHERE com_1 = %d and rate_1 = %.6f and com_2 = %d and rate_2 = %.6f"
            data = (self.table, com_1, rate_1, com_2, rate_2)
            cursor.execute( sql % data )     
            result = cursor.fetchall() # if there is no result fit requirement, return NULL
            cursor.close()
            connect.close()
        if result :
            acc = result[0][0]
        else:
            acc = None
        return acc

    def search_puredir(self, com_1, rate_1, com_2, rate_2):
        '''search the save path according to the given strategy'''
        if com_2 == com_1: # judge the number of compression layer
            result = self.search_acc_onePar(com_1, rate_1)
            if result :
                res_dir = result[0][1]
            else:
                res_dir = None
        else:    
            connect, cursor = self.SQL_connect()
            sql = "SELECT res_dir FROM %s WHERE com_1 = %d and rate_1 = %.6f and com_2 = %d and rate_2 = %.6f"
            data = (self.table, com_1, rate_1, com_2, rate_2)
            cursor.execute( sql % data )      
            result = cursor.fetchall() # if there is no result fit requirement, return NULL
            cursor.close()
            connect.close()
            if result :
                res_dir = result[0][0]
            else:
                res_dir = None
        return res_dir


    def DELETE_ALL(self):
        '''delete all result in MySQL'''
        connect, cursor = self.SQL_connect()
        sql = "DELETE FROM %s"
        data = (self.table)
        cursor.execute( sql % data)
        connect.commit()
        print('All data have been deleted')
        cursor.close()
        connect.close()


    def get_row_numbers(self):
        '''get the total number of results'''
        connect, cursor = self.SQL_connect()
        sql = "SELECT count(*) FROM %s"
        data = (self.table)
        cursor.execute( sql % data)
        row_numbers = cursor.fetchall()
        cursor.close()
        connect.close()
        return row_numbers[0][0]

if __name__ == '__main__':
    # test content
    SQL = MySQL()
    # SQL.save_result(1, 0.9, 2, 0.9, 0.99, 'D://test')
    print(SQL.get_row_numbers())
    # SQL.get_all_to_excel()
    # acc = SQL.search_acc(1, 0.5, 2, 0.8)
    # acc = SQL.search_rate2_acc(1, 0.5, 2)
    # acc = SQL.search_rate1_rate2_acc(1, 2)
    acc = SQL.search_puredir(1, 0.984375, 1, 0.984375)
    print(acc)
    # SQL.change_acc(1, 0.5, 2, 0.8, 0.91)
    # SQL.delete_acc(1, 0.5, 2, 0.8)
