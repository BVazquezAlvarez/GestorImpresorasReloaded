__author__ = 'Borja'

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import sqlite3 as dbapi
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table

class DialogTinta(Gtk.Dialog):
    """
    Ventana emergente la cual te salta cuando haya una excepcion
    """
    def __init__(self, parent, rest):
        Gtk.Dialog.__init__(self, "Tinta restante", parent, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label(rest)

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class DialogInsert(Gtk.Dialog):
    """
    Te avisa cuando se haya insertado correctamente
    """
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Insertado", parent, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Insertado correctamente")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class DialogBorrado(Gtk.Dialog):
    """
    Te avisa cuando se haya borrado correctamente
    """
    def __init__(self, parent, i):
        Gtk.Dialog.__init__(self, "Impresora borrada", parent, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("La impresora con id " + i + " ha sido borrada")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class Interfaz:
    """
    Interfaz principal
    """
    def __init__(self):
        fichero="Interfaz.glade"
        builder=Gtk.Builder()
        builder.add_from_file(fichero)
        self.window=builder.get_object("window1")
        self.window.show_all()
        self.window.set_resizable(False)

        signais= {"mostrartodas": self.mclick,
                  "buscarImpresora": self.bclick,
                  "insertarNueva": self.insertarNueva,
                  "borrar": self.borrar,
                  "comprar":self.comprar,
                  "unatinta":self.unatinta,
                  "generarpdf":self.imprimirpdf,
                  "delete-event": Gtk.main_quit,
                  "borrarimpresora":self.borrar,
                  "checkpass":self.checkpass,
                  "adminsalir":self.saliradmin}

        self.entry=builder.get_object("entrynombre")
        self.lista=builder.get_object("lista")
        self.addcodigo=builder.get_object("addcodigo")
        self.addnombre=builder.get_object("addnombre")
        self.addcolor=builder.get_object("addcolor")
        self.addcantidad=builder.get_object("addcantidad")
        self.addimpresora=builder.get_object("addimpresora")
        self.modimpresora=builder.get_object("modimpresora")
        self.addtinta=builder.get_object("addtinta")
        self.borrarimpresora=builder.get_object("borrarimpresora")
        self.codigocomprar=builder.get_object("codigocomprar")
        self.adminpass=builder.get_object("adminpass")
        self.imprimirpdf=builder.get_object("imprimirpdf")
        self.adminsalir=builder.get_object("adminsalir")




        builder.connect_signals(signais)

    def mclick(self,control):
            """
            Muestra todo lo que haya en la base de datos
            """

            #Conectamos con la base de datos
            bd = dbapi.connect("basetinta.dat")
            print(bd)
            cursor = bd.cursor()
            bd.commit()
            print("Funciona")
            #Buscamos todas las tintas
            cursor.execute("""select * from impresora""")
            impresoras = ""
            #Las metemos en un string
            for resultado in cursor:
                impresoras = impresoras + (
                "Codigo: " + str(resultado[0]) + ", Impresora: " + str(resultado[1]) + ", Tinta: " + str(
                    resultado[2]) + ", Cantidad: " + str(resultado[3]) + "\n")
            bd.close()
            self.textbuffer = self.lista.get_buffer()
            self.textbuffer.set_text
            self.textbuffer.set_text(impresoras)

    def bclick(self,control):
            """
             Muestra unicamente lo que hayamos buscado
            """
            #Cogemos la marca que ha introducido el ususario, que ha sido pasada el parametro de entrada
            id = self.entry.get_text()
            bd = dbapi.connect("basetinta.dat")
            print(bd)
            cursor = bd.cursor()
            bd.commit()

            #Buscamos las tintas que se usan en dicha marca
            cursor.execute("select * from impresora where Impresora='" + str(id) + "'")
            impresoras = ""
            for resultado in cursor:
                impresoras = impresoras + (
                "Codigo: " + str(resultado[0]) + ", Impresora: " + str(resultado[1]) + ", Tinta: " + str(
                    resultado[2]) + ", Cantidad: " + str(resultado[3]) + "\n")
            bd.close()
            self.textbuffer = self.lista.get_buffer()
            self.textbuffer.set_text
            self.textbuffer.set_text(impresoras)


    def insertarNueva(self, control):
        """
        Inserta una nueva tinta
        """
        bd = dbapi.connect("basetinta.dat")
        print(bd)
        cursor = bd.cursor()
        if (self.addcolor.get_text() or self.addnombre.get_text()or self.addcantidad.get_text() or self.addcodigo.get_text())=="":
            dialog = DialogTinta(None,"Complete todos los campos a insertar")
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                dialog.destroy()
        else:
            #Ejecutamos el sql para que inserte
            cursor.execute(
                " insert into impresora values('" + str(self.addcodigo.get_text()) + "','" + str(self.addnombre.get_text()) + "','" + str(
                    self.addcolor.get_text()) + "','" + str(self.addcantidad.get_text()) + "')")
            bd.commit()
            dialog = DialogInsert(None)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                dialog.destroy()
                self.addcantidad.set_text("")
                self.addcodigo.set_text("")
                self.addcolor.set_text("")
                self.addnombre.set_text("")

    def borrar(self,control):
        """
        Borra una tinta de la base
        """
        bd = dbapi.connect("basetinta.dat")
        print(bd)

        cursor = bd.cursor()
        cursor.execute("delete from impresora where Codigo='" + self.modimpresora.get_text() + "'")
        bd.commit()
        dialog = DialogBorrado(self, self.modimpresora.get_text())
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.destroy()

    def comprar(self,control):
        """
        Elimina una tinta de la base porque la han comprado
        """
        bd = dbapi.connect("basetinta.dat")
        print(bd)

        #Cogemos del Text Field el codigo de la impresora introducido
        cursor = bd.cursor()
        #Vemos con que impresora coincide el codigo
        cursor.execute("select Cantidad from impresora where Codigo='" +  self.codigocomprar.get_text() + "'")
        for resultado in cursor:
            nuevacant = (resultado[0])

        #Comprueba que hay stock para esa impresora. Si no hay lo muestra en el boton.
        if int(nuevacant)==0:
            dialog = DialogTinta(None,"No hay stock de "+str( self.codigocomprar.get_text()))
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                dialog.destroy()

        else:
            #restamos
            nuevacantint = int(nuevacant) - 1
            nuevacant = str(nuevacantint)

            # Actualizamos la la fila en la base de datos
            cursor.execute("Update impresora set Cantidad='{}' where Codigo='{}'".format(nuevacant,  self.codigocomprar.get_text()))
            bd.commit()

            #Pasamos a la ventana emergente los cartuchos restantes para que se le informe al usuario
            dialog = DialogTinta(None,"Quedan "+ str(nuevacant)+" cartuchos")
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                dialog.destroy()

    def unatinta(self, control):
        """
        Suma 1 de tinta porque la han devuelto o porque lo manda el admin
        """
        bd = dbapi.connect("basetinta.dat")
        print(bd)
        nuevacant=None
        cursor = bd.cursor()
        cursor.execute("select Cantidad from impresora where Codigo='" + self.modimpresora.get_text() + "'")
        for resultado in cursor:
            nuevacant = (resultado[0])

        if nuevacant==None:
            dialog = DialogTinta(None,"No existe esa impresora")
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                dialog.destroy()
        else:
            nuevacantint = int(nuevacant) + 1
            nuevacant = str(nuevacantint)

            cursor.execute("Update impresora set Cantidad='{}' where Codigo='{}'".format(nuevacant,self.modimpresora.get_text()))
            bd.commit()
            dialog = DialogTinta(None, "Ensertada tinta a la impresora "+self.modimpresora.get_text())
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                dialog.destroy()

    def imprimirpdf(self,control):
        """
        Imprime el pdf
        """
        pdf = "Impresoras.pdf"
        bd = dbapi.connect("basetinta.dat")
        cursor = bd.cursor()
        c = canvas.Canvas(pdf, pagesize=A4)
        impresoras = list(cursor.execute("select * from impresora"))
        title = [["CODIGO", "NOMBRE", "COLOR", "CANTIDAD"]]

        clientes = title+impresoras
        tabla = Table(clientes)
        tabla.wrapOn(c, 20, 30)
        tabla.drawOn(c, 20, 600)
        c.save()

    def checkpass(self,control):
        """
        Comprueba que es correcta la pass
        """
        if self.adminpass.get_text()=="root":
            self.addcodigo.set_sensitive(True)
            self.addcantidad.set_sensitive(True)
            self.addnombre.set_sensitive(True)
            self.addcolor.set_sensitive(True)
            self.modimpresora.set_sensitive(True)
            self.addimpresora.set_sensitive(True)
            self.imprimirpdf.set_sensitive(True)
            self.borrarimpresora.set_sensitive(True)
            self.addtinta.set_sensitive(True)
            self.adminpass.set_text("")
            self.adminsalir.set_sensitive(True)
            dialog = DialogTinta(None,"Pass Correcta")
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                 dialog.destroy()


        else:
           self.labelpass.set_text("Pass incorrecta")
           dialog = DialogTinta(None,"Pass incorrecta")
           response = dialog.run()
           if response == Gtk.ResponseType.OK:
                dialog.destroy()

    def saliradmin(self,control):
        """
        Sale del modo admintrador
        """
        self.addcodigo.set_sensitive(False)
        self.addcantidad.set_sensitive(False)
        self.addnombre.set_sensitive(False)
        self.addcolor.set_sensitive(False)
        self.modimpresora.set_sensitive(False)
        self.addimpresora.set_sensitive(False)
        self.imprimirpdf.set_sensitive(False)
        self.borrarimpresora.set_sensitive(False)
        self.addtinta.set_sensitive(False)
        self.adminsalir.set_sensitive(False)


if __name__ == "__main__":
    Interfaz()
    Gtk.main()

