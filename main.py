from tkinter import *
from tkinter import ttk
from connextion import *

#Variables para la interfaz
ventana = Tk()
ventana.title("Crud mysql ")
ventana.geometry("600x500")

# Crear una instacio de la clase conection
db = DataBase()
modificar = False
dni = StringVar()
sexo = StringVar()
nombre = StringVar()
apellido = StringVar()


def estudianteClick(event):
    id = tvEstudiante.selection()[0]
    if int(id) > 0:
        dni.set(tvEstudiante.item(id, "values")[1])
        sexo.set(tvEstudiante.item(id, "values")[2])
        nombre.set(tvEstudiante.item(id, "values")[3])
        apellido.set(tvEstudiante.item(id, "values")[4])

#Interfaz
marco = LabelFrame(ventana, text="Formulario de gestion de estudiantes ")
marco.place(x=50, y=50, width=500, height=400)
# Label y Entrys
labelDni = Label(marco, text="DNI").grid(column=0, row=0, padx=5, pady=5)
txtDni = Entry(marco, textvariable=dni)
txtDni.grid(column=1, row=0)

labelSexo = Label(marco, text="Sexo").grid(column=0, row=1, padx=5, pady=5)
txtSexo = ttk.Combobox(marco, values=["M", "F"], textvariable=sexo)
txtSexo.grid(column=1, row=1)
txtSexo.current(0)

labelNombre = Label(marco, text="Nombre").grid(column=2, row=0, padx=5, pady=5)
txtNombre = Entry(marco, textvariable=nombre)
txtNombre.grid(column=3, row=0)

labelApellido = Label(marco, text="Apellido").grid(column=2, row=1, padx=5, pady=5)
txtApellido = Entry(marco, textvariable=apellido)
txtApellido.grid(column=3, row=1)

lblMensaje = Label(marco, text="Aqui van los mensaje", fg="green")
lblMensaje.grid(column=0, row=2, columnspan=4)
# Tabla de lista de estuiante
tvEstudiante = ttk.Treeview(marco, selectmode=NONE)
tvEstudiante.grid(column=0, row=3, columnspan=4, padx=5)
tvEstudiante["columns"] = ("ID", "DNI", "SEXO", "NOMBRE", "APELLIDO")
tvEstudiante.column("#0", width=0, stretch=NO)
tvEstudiante.column("ID", width=50, anchor=CENTER)
tvEstudiante.column("DNI", width=50, anchor=CENTER)
tvEstudiante.column("SEXO", width=50, anchor=CENTER)
tvEstudiante.column("NOMBRE", width=100, anchor=CENTER)
tvEstudiante.column("APELLIDO", width=100, anchor=CENTER)

tvEstudiante.heading("#0", text="")
tvEstudiante.heading("ID", text="ID", anchor=CENTER)
tvEstudiante.heading("DNI", text="DNI", anchor=CENTER)
tvEstudiante.heading("SEXO", text="SEXO", anchor=CENTER)
tvEstudiante.heading("NOMBRE", text="NOMBRE", anchor=CENTER)
tvEstudiante.heading("APELLIDO", text="APELLIDO", anchor=CENTER)
tvEstudiante.bind("<<TreeviewSelect>>", estudianteClick)

# BOTONES
btnEliminar = Button(marco, text="Eliminar", command=lambda: eliminar())
btnEliminar.grid(column=1, row=4)

btnNuevo = Button(marco, text="Guardar", command=lambda: nuevo())
btnNuevo.grid(column=2, row=4)

btnActualizar = Button(marco, text="Seleccionar", command=lambda: actualizar())
btnActualizar.grid(column=3, row=4)


##Funciones de la inteccion del sistema
def validar():
    return len(dni.get()) and len(nombre.get()) and len(apellido.get())


def limpiar():
    dni.set("")
    sexo.set("")
    nombre.set("")
    apellido.set("")


def vaciar_tabla():
    filas = tvEstudiante.get_children()
    for fila in filas:
        tvEstudiante.delete(fila)


def llenar_tabla():
    vaciar_tabla()
    sql = "SELECT * FROM `estudiantes` "
    db.cursor.execute(sql)
    filas = db.cursor.fetchall()
    for fila in filas:
        id = fila[0]
        tvEstudiante.insert("", END, id, text=id, values=fila)


def modificarFlase():
    global modificar
    modificar = False
    tvEstudiante.config(selectmode=NONE)
    btnNuevo.config(text="Guardar")
    btnActualizar.config(text="Seleccionar")
    btnEliminar.config(state=DISABLED)


def modificarTrue():
    global modificar
    modificar = True
    tvEstudiante.config(selectmode=BROWSE)
    btnNuevo.config(text="Nuevo")
    btnActualizar.config(text="Actualizar")
    btnEliminar.config(state=NORMAL)


# Funcion para CRUD, Insertar, actualizar y eliminar
def eliminar():
    id = tvEstudiante.selection()[0]
    # Ferificion de ID
    if int(id) > 0:
        sql = "DELETE FROM `estudiantes` where id=" + id
        db.cursor.execute(sql)
        db.conexion.commit()
        tvEstudiante.delete(id)
        lblMensaje.config(text="se a eliminado el registro, Correctamente")
        limpiar()
    else:
        lblMensaje.config(text="Seleciones un registro para eliminar ")


def nuevo():
    if modificar == False:
        if validar():
            val = (dni.get(), sexo.get(), nombre.get(), apellido.get())
            slq = "INSERT INTO `estudiantes`(dni, sexo, nombre, apellido) VALUES (%s,%s,%s,%s)"
            db.cursor.execute(slq, val)
            db.conexion.commit()
            lblMensaje.config(text="Se a guardado un registro correctamente", fg="green")
            llenar_tabla()
            limpiar()
        else:
            lblMensaje.config(text="Los compos no deben estar basios", fg="red")
    else:
        modificarFlase()


def actualizar():
    if modificar == True:
        if validar():
            id = tvEstudiante.selection()[0]
            val = (dni.get(), sexo.get(), nombre.get(), apellido.get())
            slq = "UPDATE `estudiantes` SET dni=%s, sexo=%s, nombre=%s, apellido=%s WHERE id=" + id
            db.cursor.execute(slq, val)
            db.conexion.commit()
            lblMensaje.config(text="Se actualizo correctamente ", fg="green")
            llenar_tabla()
            limpiar()
        else:
            lblMensaje.config(text="Los compos no deben estar basios", fg="red")
    else:
        modificarTrue()


llenar_tabla()
ventana.mainloop()
