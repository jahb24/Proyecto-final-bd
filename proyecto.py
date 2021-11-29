from pymongo import MongoClient, errors # El cliente de MongoDB
from clases import Employee, Department # La clase employee
from bson.objectid import ObjectId # Para crear ObjectId, porque _id como cadena no funciona
from os import system, name, environ
from prettytable import PrettyTable
import getpass

# Screen cleaner function
def clear():
    
    # for Windows
    if name == 'nt': system('cls')
    
    # for mac and Linux
    else: system('clear')

# Pause screen function
def pause():
    input("\nPresione <ENTER> para continuar...")

def obtener_bd():
    base_de_datos = "Scott"
    cliente = MongoClient("mongodb://localhost:27017")
    return cliente[base_de_datos]

## CREATE
def insertar(data):
    base_de_datos = obtener_bd()
    if type(data).__name__ == "Employee":
        employees = base_de_datos.employees
        return employees.insert_one({
            "empno": data.numEmp,
            "ename": data.nombre,
            "job": data.puesto,
            "mgr": data.numJefe,
            "sal": data.salario,
            "comm": employee.comision,
            "deptno": data.numDep
        }).inserted_id
    else:
        departments = base_de_datos.departments
        return departments.insert_one({
            "deptno": data.numDep,
            "dname": data.nombre,
            "loc": data.ciudad
        }).inserted_id

## READ
def obtener(collection):
    base_de_datos = obtener_bd()
    return base_de_datos[collection].find().sort("_id")

def obtenerUno(collection, id):
    base_de_datos = obtener_bd()
    if(collection == "employees"): return base_de_datos[collection].find({"empno":id})
    else: return base_de_datos[collection].find({"deptno":id})

## UPDATE
def actualizar(id, data):
    try:
        base_de_datos = obtener_bd()
        if type(data).__name__ == "Employee":
            resultado = base_de_datos["employees"].update_one(
                {
                    "empno": id
                    #'_id': ObjectId(id)
                }, 
                {
                    '$set': {
                        "ename": data.nombre,
                        "job": data.puesto,
                        "sal": data.salario,
                        "mgr": data.numJefe,
                        "comm": data.comision,
                        "deptno": data.numDep
                    }
                })
            return resultado.modified_count
        else:
            resultado = base_de_datos["departments"].update_one(
                {
                    "deptno": id
                    #'_id': ObjectId(id)
                }, 
                {
                    '$set': {
                        "dname": data.nombre,
                        "loc": data.ciudad
                    }
                })
            return resultado.modified_count
    except errors.InvalidId:
        print(
            """\n
            -----------------------------------
            Error: el Número ingresado es invalido.
            -----------------------------------
            \n""")
        return 0


## DELETE
def eliminar(collection, id):
    base_de_datos = obtener_bd()
    try:
        if collection == "employees":
            resultado = base_de_datos[collection].delete_one(
                {
                    "empno": id
                    #'_id': ObjectId(id)
                })
        else:
            resultado = base_de_datos[collection].delete_one(
                {
                    "deptno": id
                    #'_id': ObjectId(id)
                })
        return resultado.deleted_count
    except errors.InvalidId:
        print(
            """\n
            -----------------------------------
            Error: el Número ingresado es invalido.
            -----------------------------------
            \n""")
        return 0




creditos = """==========================================================
	                CRUD de MongoDB y Python
                                           
                                __ __          __         
	.-----.---.-.----.-----|__|  |--.--.--|  |_.-----.
	|  _  |  _  |   _|-- __|  |  _  |  |  |   _|  -__|
	|   __|___._|__| |_____|__|_____|___  |____|_____|
	|__|                            |_____|           

==========================================================\n"""

menu = f"""Bienvenido {getpass.getuser()}

01 - Insertar empleado
02 - Insertar departamento

03 - Ver un empleado
04 - Ver un departamento

05 - Ver todos los empleados
06 - Ver todos los departamentos

07 - Actualizar empleado
08 - Actualizar departamento

09 - Eliminar empleado
10 - Eliminar departamento

11 - Salir
"""
eleccion = None
while eleccion != 11:
    clear()
    print(creditos)
    print(menu)
    eleccion = int(input("Elige: "))
    if eleccion == 1:
        clear()
        print("\tNuevo empleado\n")
        numero = int(input("Número del empleado: "))
        nombre = input("Nombre del empleado: ")
        puesto = input("Puesto del empleado: ")
        jefe = int(input("Número del manager: "))
        salario = int(input("Salario del empleado: "))
        comision = int(input("Comision que recibe: "))
        departamento = int(input("Numero de departamento en el que trabaja: "))
        employee = Employee(numero, nombre, puesto, jefe, salario, comision, departamento)
        print(f"El empleado se ha insertado con el id: {insertar(employee)}")
        pause()
    elif eleccion == 2:
        clear()
        print("\tNuevo departamento\n")
        departamento = int(input("Número del departamento: "))
        nomDep = input("Nombre del departamento: ")
        ciudad = input("Ciudad del departamento: ")
        department = Department(departamento, nomDep, ciudad)
        print(f"El id del departamento insertado es: {insertar(department)}")
        pause()
    elif eleccion == 3:
        clear()
        id = int(input("Número del empleado: "))
        for employee in obtenerUno("employees", id):
            print()
            print("ID: ", employee["_id"])
            print("Número: ", int(employee["empno"]))
            print("Nombre: ", employee["ename"])
            print("Puesto: ", employee["job"])
            if employee["mgr"] == "null": print("Manager: ", employee["mgr"])
            else: print("Manager: ", int(employee["mgr"]))
            print("Salario: ", employee["sal"])
            print("Comision: ", employee["comm"])
            if employee["deptno"] == "null": print("Departamento: ", employee["deptno"])
            else: print("Departamento: ", int(employee["deptno"]))
        pause()
    elif eleccion == 4:
        clear()
        id = int(input("Número del departamento: "))
        for department in obtenerUno("departments", id):
            print()
            print("ID: ", department["_id"])
            print("Número: ", int(department["deptno"]))
            print("Nombre: ", department["dname"])
            print("Ciudad: ", department["loc"])
        pause()
    elif eleccion == 5:
        clear()
        print("Obteniendo empleados...")
        table = PrettyTable()
        table.field_names = ["ID", "Número", "Nombre", "Trabajo","Manager","Salario","Comisión","Departamento"]
        for employee in obtener("employees"):
            id = employee["_id"]
            num = int(employee["empno"])
            name = employee["ename"]
            job = employee["job"]
            mgr = "null"
            if employee["mgr"] != "null": mgr = int(employee["mgr"])
            sal = employee["sal"]
            comm = employee["comm"]
            dept = "null"
            if(employee["deptno"] != "null"): dept = int(employee["deptno"])
            table.add_row([id,num,name,job,mgr,sal,comm,dept])
        print(table)
        pause()
    elif eleccion == 6:
        clear()
        print("Obteniendo departamentos...")
        table = PrettyTable()
        table.field_names = ["ID", "Número", "Nombre", "Ciudad"]
        for department in obtener("departments"):
            id = department["_id"]
            num = int(department["deptno"])
            name = department["dname"]
            loc = department["loc"]
            table.add_row([id,num,name,loc])
        print(table)
        pause()
    elif eleccion == 7:
        clear()
        print("\tActualizar empleado\n")
        #id = input("Dime el ID del empleado: ")
        numero = int(input("Dime el Número del empleado: "))
        nombre = input("Nuevo Nombre del empleado: ")
        puesto = input("Nuevo Puesto del empleado: ")
        jefe = int(input("Nuevo Número del manager: "))
        salario = int(input("Nuevo Salario del empleado: "))
        comision = int(input("Nueva Comision: "))
        departamento = int(input("Nuevo Numero de departamento en el que trabaja: "))
        employee = Employee(numero, nombre, puesto, jefe, salario, comision, departamento)
        empleados_actualizados = actualizar(numero, employee)
        print("Número de empleados actualizados: ", empleados_actualizados)
        pause()
    elif eleccion == 8:
        clear()
        print("\tActualizar departamento\n")
        #id = input("Dime el ID del departamento: ")
        departamento = int(input("Dime el Número de departamento: "))
        nomDep = input("Nuevo Nombre del departamento: ")
        ciudad = input("Nueva Ciudad del departamento: ")
        department = Department(departamento, nomDep, ciudad)
        dept_actualizados = actualizar(departamento, department)
        print("Número de departamentos actualizados: ", dept_actualizados)
        pause()
    elif eleccion == 9:
        clear()
        print("\tEliminar\n")
        #id = input("Dime el ID del empleado: ")
        numero = int(input("Dime el Número del empleado: "))
        empleados_eliminados = eliminar("employees", numero)
        print("Número de empleados eliminados: ", empleados_eliminados)
        pause()
    elif eleccion == 10:
        clear()
        print("\tEliminar\n")
        #id = input("Dime el ID del departamento: ")
        departamento = int(input("Dime el Número de departamento: "))
        departamentos_eliminados = eliminar("departments", departamento)
        print("Número de departamentos eliminados: ", departamentos_eliminados)
        pause()
clear()