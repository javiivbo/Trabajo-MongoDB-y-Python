from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://grupoinacap3_db_user:Grupo3inacap@grupo3.f4jqd0z.mongodb.net/")
db = client["SistemaAlumnos"]
alumnos = db["alumnos"]  

def menu():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registra alumno")
        print("2. Mostrar todos los alumnos")
        print("3. Buscar por mayor nota")
        print("4. Buscar alumno por nombre")
        print("5. Buscar por fecha de matricula")
        print("6. Buscar alumnos por comunas")
        print("7. Agregar nueva asgnatura")
        print("8. Actualizar notas")
        print("9. Eliminar alumno")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            Registrar_alumno()
        elif opcion == "2":
            Mostrar_alumnos()
        elif opcion == "3":
            buscar_comparacion()
        elif opcion == "4":
            buscar_regex()
        elif opcion == "5":
            buscar_rango_fechas()
        elif opcion == "6":
            buscar_subdocumento()
        elif opcion == "7":
            agregar_asignatura()
        elif opcion == "8":
            actualizar_calificacion()
        elif opcion == "9":
            eliminar_alumno()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

def Registrar_alumno():
    rut = input("RUT: ")
    nombre = input("Nombre completo: ")
    edad = int(input("edad: "))
    fecha_nacimiento = input("Fecha nacimiento (YYYY-MM-DD): ")
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    
    
    direccion = {
        "calle": input("Calle: "),
        "numero": int(input("Número: ")),
        "comuna": input("Comuna: "),    
    }

    fecha_matricula = input("Fecha matricula (YYYY-MM-DD): ")
    fecha_matricula = datetime.strptime(fecha_matricula, "%Y-%m-%d")
    
    cursando = {
        "enseñanza": input("Enseñanza: ")
    }

    apoderado = {
        "nombre": input("Nombre apoderado: "),
        "contacto": input("Contacto apoderado (teléfono): "),
        "parentesco": input("Parentesco con el alumno: ")
    }

    calificaciones = []
    m = int(input("¿Cuántas calificaciones agregar?: "))
    for j in range(m):
        asignatura = input(f"Asignatura {j+1}: ")
        nota = float(input(f"Nota para {asignatura}: "))
        fecha = input("Fecha evaluación (YYYY-MM-DD): ")
        calificaciones.append({
            "asignatura": asignatura,
            "nota": nota,
            "fecha": datetime.strptime(fecha, "%Y-%m-%d")
        })

    alumno = {
        "rut": rut,
        "nombre": nombre,
        "edad": edad,
        "direccion": direccion,
        "fecha_matricula": fecha_matricula,
        "cursando": cursando,
        "jornada": "Completa",
        "apoderado": apoderado,
        "calificaciones": calificaciones
    }

    alumnos.insert_one(alumno)
    print("Alumno Registrado exitosamente.")

def Mostrar_alumnos():
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
    for a in alumnos.find({"fecha_matricula": {"$gte": inicio, "$lte": fin}}):
        print(a)

def buscar_subdocumento():
    comuna = input("Alumnos de la comuna de: ")
    for a in alumnos.find({"direccion.comuna": comuna}):
        print(a)

def agregar_asignatura():
    rut = input("RUT del alumno: ")
    nombre_asignatura = input("Nombre de la asignatura: ")
    nota = float(input("Nota inicial: "))
    fecha = input("Fecha (YYYY-MM-DD): ")

    alumno = alumnos.find_one({"rut": rut})

    if not alumno:
        print("Alumno no encontrado.")
        return

    
    if "calificaciones" in alumno:
        nueva_calificacion = {
            "asignatura": nombre_asignatura,
            "nota": nota,
            "fecha": datetime.strptime(fecha, "%Y-%m-%d")
        }
        alumnos.update_one(
            {"rut": rut},
            {"$push": {"calificaciones": nueva_calificacion}}
        )
        print("Asignatura agregada en calificaciones.")


    elif "cursos" in alumno:
        nuevo_curso = {
            "nombre": nombre_asignatura,
            "nota": nota
        }
        alumnos.update_one(
            {"rut": rut},
            {"$push": {"cursos": nuevo_curso}}
        )
        print("Curso agregado en cursos.")

    else:
        print("El alumno no tiene estructura de cursos ni calificaciones.")

def actualizar_calificacion():
    rut = input("RUT del alumno: ")
    asignatura = input("Nombre de la asignatura a modificar: ")
    nueva_nota = float(input("Nueva nota: "))

    resultado = alumnos.update_one(
        {"rut": rut, "calificaciones.asignatura": asignatura},
        {"$set": {"calificaciones.$.nota": nueva_nota}}
    )

    if resultado.modified_count > 0:
        print("Nota actualizada correctamente en calificaciones.")
    else:
        print("No se encontró la asignatura o no se modificó la nota.")

def eliminar_alumno():
    rut = input("RUT del alumno a eliminar: ")
    alumnos.delete_one({"rut": rut})
    print("Alumno eliminado.")


menu()