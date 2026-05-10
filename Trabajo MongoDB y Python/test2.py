from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://grupoinacap3_db_user:Grupo3inacap@grupo3.f4jqd0z.mongodb.net/")
db = client["SistemaAlumnos"]
alumnos = db["alumnos"]  

def menu():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registra alumno")
        print("2. Listar alumnos")
        print("3. Buscar por operador de comparación")
        print("4. Buscar alumno por nombre")
        print("5. Buscar por rango de fechas")
        print("6. Buscar alumnos por comunas/array")
        print("7. Actualizar campo raíz (nombre)")
        print("8. Actualizar dentro de subdocumento/array (nota)")
        print("9. Eliminar alumno")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            Registrar_alumno()
        elif opcion == "2":
            listar_alumnos()
        elif opcion == "3":
            buscar_comparacion()
        elif opcion == "4":
            buscar_regex()
        elif opcion == "5":
            buscar_rango_fechas()
        elif opcion == "6":
            buscar_subdocumento()
        elif opcion == "7":
            actualizar_raiz()
        elif opcion == "8":
            actualizar_array()
        elif opcion == "9":
            eliminar_alumno()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

def Registrar_alumno():
    rut = input("RUT: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    fecha_nacimiento = datetime.strptime(input("Fecha nacimiento (YYYY-MM-DD): "), "%Y-%m-%d")

    direccion = {
        "calle": input("Calle: "),
        "numero": int(input("Número: ")),
        "comuna": input("Comuna: "),
        
    }
    apoderado = {
        "nombre": input("Nombre apoderado: "),
        "contacto": input("Contacto apoderado (teléfono): "),
        "parentesco": input("Parentesco con el alumno: ")
    }
    cursos = []
    n = int(input("¿Cuántos cursos agregar?: "))
    for i in range(n):
        curso = {
            "nombre": input(f"Nombre curso {i+1}: "),
            "nota": float(input("Nota: ")),
            "fecha_inscripcion": datetime.strptime(input("Fecha inscripción (YYYY-MM-DD): "), "%Y-%m-%d")
        }
        cursos.append(curso)

    alumno = {
        "rut": rut,
        "nombre": nombre,
        "apellido": apellido,
        "fecha_nacimiento": fecha_nacimiento,
        "direccion": direccion,
        "cursos": cursos
    }

    alumnos.insert_one(alumno)
    print("Alumno Registrado exitosamente.")

def listar_alumnos():
    for a in alumnos.find():
        print(a)

def buscar_comparacion():
    nota_min = float(input("Buscar alumnos con nota mayor a: "))
    for a in alumnos.find({"calificaciones.nota": {"$gt": nota_min}}):
        print(a)

def buscar_regex():
    patron = input("El alumno: ")
    for a in alumnos.find({"nombre": {"$regex": patron, "$options": "i"}}):
        print(a)

def buscar_rango_fechas():
    inicio = datetime.strptime(input("Fecha inicio (YYYY-MM-DD): "), "%Y-%m-%d")
    fin = datetime.strptime(input("Fecha fin (YYYY-MM-DD): "), "%Y-%m-%d")
    for a in alumnos.find({"fecha_nacimiento": {"$gte": inicio, "$lte": fin}}):
        print(a)

def buscar_subdocumento():
    comuna = input("Alumnos de la comuna de: ")
    for a in alumnos.find({"direccion.comuna": comuna}):
        print(a)

def actualizar_raiz():
    rut = input("RUT del alumno a actualizar: ")
    nuevo_nombre = input("Nuevo nombre: ")
    alumnos.update_one({"rut": rut}, {"$set": {"nombre": nuevo_nombre}})
    print("Nombre actualizado.")

def actualizar_array():
    rut = input("RUT del alumno: ")
    curso_antiguo = input("Nombre curso a modificar: ")
    nueva_nota = float(input("Nueva nota: "))
    alumnos.update_one(
        {"rut": rut, "cursos.nombre": curso_antiguo},
        {"$set": {"cursos.$.nota": nueva_nota}}
    )
    print("Nota actualizada.")

def eliminar_alumno():
    rut = input("RUT del alumno a eliminar: ")
    alumnos.delete_one({"rut": rut})
    print("Alumno eliminado.")

# Ejecutar menú
menu()