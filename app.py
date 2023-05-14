from flask import Flask,render_template,request
import pymysql

app = Flask(__name__)

conn = pymysql.connect(host='localhost', user='root', password='abc2206228', database='student_db',port=3306)
sql_create_table = '''CREATE TABLE IF NOT EXISTS student(id INT PRIMARY KEY AUTO_INCREMENT,name VARCHAR(20),student_id VARCHAR(20),age INT)'''
cursor = conn.cursor()
cursor.execute(sql_create_table)
user=['zhangkaipeng']
pwd=['123456']

def denglu(users,pwds):
    if users in user and pwds in pwd:
        return True
    else:
        return False
def zhuce(users,pwds):
    user.append(users)
    pwd.append(pwds)
def showInfo():
    print("-" * 30)
    print("1.添加学生的信息")
    print("2.删除学生的信息")
    print("3.修改学生的信息")
    print("4.查询学生的信息")
    print("5.遍历学生的信息")
    print("6.退出系统")
    print("-" * 30)
class StudentManager:
    class Student:
            def __init__(self, name, id, age):
                self.name = name
                self.id = id
                self.age = age

    def __init__(self):
        self.student_list = []
    def addNewStu(self,name,id,age):
            student = self.Student(name, id, age)
            self.student_list.append(student)
            # 插入数据
            sql_insert = f"INSERT INTO student(name, student_id, age) VALUES('{name}', '{id}', {age})"
            cursor.execute(sql_insert)
            conn.commit()  # 提交操作

    def del_info(self,del_name):
            for student in self.student_list:
                if del_name == student.name:
                    self.student_list.remove(student)
                    sql_delete = f"DELETE FROM student WHERE name='{del_name}'"
                    cursor.execute(sql_delete)
                    conn.commit()
                    return True
            return False

    def modify_info(self,modify_name,new_id,new_age):
            if (self.student_list.__len__() == 0):
                return False
            for student in self.student_list:
                if modify_name == student.name:
                    student.id = new_id
                    student.age = new_age
                    sql_update = f"UPDATE student SET student_id='{student.id}', age={student.age} WHERE name='{student.name}'"
                    cursor.execute(sql_update)
                    conn.commit()
                    return True
            return False

    def search_info(self,search_name):
            # 查询数据
            sql_select = f"select * from student where name='{search_name}'"
            cursor.execute(sql_select)
            result = cursor.fetchone()
            if result:
                student = self.Student(result[1], result[2], result[3])
                return student
            else:
                return None

    def print_all(self):
            student_list = []
            # 查询数据
            sql_select = "select * from student"
            cursor.execute(sql_select)
            results = cursor.fetchall()
            for result in results:
                student = self.Student(result[1], result[2], result[3])
                student_list.append({'name': student.name, 'id': student.id, 'age': student.age})
            return student_list
student_manager = StudentManager()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users = request.form['username']
    pwds = request.form['password']
    if users in user and pwds in pwd:
        return render_template('student.html')
    else:
        return render_template('index.html', error='Invalid credentials')

@app.route('/register', methods=['POST'])
def register():
    users=request.form['username']
    pwds=request.form['password']
    user.append(users)
    pwd.append(pwds)
    return render_template('index.html', message='Registration successful')

@app.route('/student', methods=['GET'])
def show_student():
    student_list = student_manager.print_all()
    return render_template('student.html', student_list=student_list)

@app.route('/addStudent', methods=['POST'])
def add_student():
    name = request.form['name']
    id = request.form['id']
    age = request.form['age']
    student_manager.addNewStu(name, id, age)
    return 'success'

@app.route('/deleteStudent', methods=['POST'])
def delete_student():
    del_name = request.form['del_name']
    if student_manager.del_info(del_name):
        return 'success'
    else:
        return 'fail'

@app.route('/modifyStudent', methods=['POST'])
def modify_student():
    modify_name = request.form['modify_name']
    new_id = request.form['new_id']
    new_age = request.form['new_age']
    if student_manager.modify_info(modify_name, new_id, new_age):
        return 'success'
    else:
        return 'fail'

@app.route('/searchStudent', methods=['POST'])
def search_student():
    search_name = request.form['search_name']
    student = student_manager.search_info(search_name)
    if student:
        return f"姓名:{student.name}, 学号:{student.id}, 年龄:{student.age}"
    else:
        return 'fail'

if __name__ == '__main__':
    app.run()


