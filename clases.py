class Employee:
    def __init__(self, numEmp, nombre, puesto, numJefe, salario, comision, departamento):
        self.numEmp = numEmp
        self.nombre = nombre
        self.puesto = puesto
        self.numJefe = numJefe
        self.salario = salario
        self.comision = comision
        self.numDep = departamento

class Department:
    def __init__(self, numDep, nombre, ciudad):
        self.numDep = numDep
        self.nombre = nombre
        self.ciudad = ciudad
