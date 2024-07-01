import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import shutil

def organizar_archivos(carpeta_origen, incluir_subcarpetas, extensiones_personalizadas, mover_no_reconocidos, prefijo):
    try:
        registros = []
        carpeta_otros = os.path.join(carpeta_origen, "otros")

        # Función para organizar archivos en una carpeta dada
        def organizar_en_carpeta(carpeta):
            for filename in os.listdir(carpeta):
                ruta_completa = os.path.join(carpeta, filename)
                if os.path.isfile(ruta_completa):
                    _, ext = os.path.splitext(filename)
                    ext = ext.lower()

                    # Organizar según las extensiones personalizadas o por tipo
                    if extensiones_personalizadas and ext[1:] in extensiones_personalizadas:
                        carpeta_destino = os.path.join(carpeta, ext[1:] + '_files')
                    elif ext[1:]:
                        carpeta_destino = os.path.join(carpeta, ext[1:] + '_files')
                    else:
                        carpeta_destino = carpeta_otros

                    # Crear la carpeta destino si no existe
                    os.makedirs(carpeta_destino, exist_ok=True)

                    # Construir el nuevo nombre del archivo con el prefijo
                    nuevo_nombre = prefijo + filename
                    ruta_nuevo_nombre = os.path.join(carpeta_destino, nuevo_nombre)

                    # Verificar si el archivo ya existe en la carpeta destino
                    if not os.path.exists(ruta_nuevo_nombre):
                        # Mover y renombrar el archivo
                        shutil.move(ruta_completa, ruta_nuevo_nombre)
                        # Registrar el movimiento en el historial
                        registros.append(f"{filename} --> {ruta_nuevo_nombre}")
                    else:
                        if messagebox.askyesno("Archivo Existente", f"El archivo '{filename}' ya existe en '{carpeta_destino}'. ¿Deseas sobrescribirlo?"):
                            shutil.move(ruta_completa, ruta_nuevo_nombre)
                            registros.append(f"{filename} --> {ruta_nuevo_nombre} (sobrescrito)")
                        else:
                            registros.append(f"No se movió '{filename}'")

                elif os.path.isdir(ruta_completa) and incluir_subcarpetas:
                    organizar_en_carpeta(ruta_completa)

        organizar_en_carpeta(carpeta_origen)

        # Mostrar historial de registros
        if registros:
            historial.config(state=tk.NORMAL)
            for registro in registros:
                historial.insert(tk.END, registro + "\n")
            historial.config(state=tk.DISABLED)

        messagebox.showinfo("Éxito", "Archivos organizados y renombrados correctamente.")
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"No se encontró el archivo o carpeta: {str(e)}")
    except PermissionError as e:
        messagebox.showerror("Error", f"Permiso denegado para acceder al archivo: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

def seleccionar_carpeta():
    carpeta_origen = filedialog.askdirectory()
    if carpeta_origen:
        label_carpeta.config(text=f"Carpeta seleccionada: {carpeta_origen}")
        btn_organizar.config(state=tk.NORMAL)  # Habilitar el botón de organizar

def limpiar_historial():
    historial.config(state=tk.NORMAL)
    historial.delete('1.0', tk.END)
    historial.config(state=tk.DISABLED)

def abrir_carpeta_origen():
    carpeta_origen = label_carpeta.cget('text').split(': ')[1]
    if os.path.exists(carpeta_origen):
        os.startfile(carpeta_origen)

# Crear la ventana principal
root = tk.Tk()
root.title("Organizador y Renombrador de Archivos")

# Función para centrar la ventana en la pantalla
def centrar_ventana():
    ancho = 800
    alto = 500
    x = (root.winfo_screenwidth() // 2) - (ancho // 2)
    y = (root.winfo_screenheight() // 2) - (alto // 2)
    root.geometry(f'{ancho}x{alto}+{x}+{y}')

centrar_ventana()

# Crear marco para la configuración
frame_configuracion = tk.LabelFrame(root, text="Configuración de Organización", padx=10, pady=10)

# Widgets para la configuración
label_carpeta = tk.Label(frame_configuracion, text="Selecciona la carpeta a organizar:")
btn_seleccionar = tk.Button(frame_configuracion, text="Seleccionar carpeta", command=seleccionar_carpeta)
label_subcarpetas = tk.Label(frame_configuracion, text="Incluir subcarpetas:")
check_subcarpetas_var = tk.BooleanVar()
check_subcarpetas = tk.Checkbutton(frame_configuracion, variable=check_subcarpetas_var)
label_extensiones = tk.Label(frame_configuracion, text="Extensiones personalizadas (separadas por coma):")
extensiones_personalizadas_entry = tk.Entry(frame_configuracion, width=50)
label_mover_no_reconocidos = tk.Label(frame_configuracion, text="Mover archivos no reconocidos a 'otros':")
check_mover_no_reconocidos_var = tk.BooleanVar()
check_mover_no_reconocidos = tk.Checkbutton(frame_configuracion, variable=check_mover_no_reconocidos_var)
label_prefijo = tk.Label(frame_configuracion, text="Prefijo para los archivos renombrados:")
prefijo_entry = tk.Entry(frame_configuracion, width=50)

# Posicionar widgets en el marco de configuración
label_carpeta.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)
btn_seleccionar.grid(row=0, column=2, padx=10, pady=5)
label_subcarpetas.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
check_subcarpetas.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
label_extensiones.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
extensiones_personalizadas_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)
label_mover_no_reconocidos.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
check_mover_no_reconocidos.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
label_prefijo.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
prefijo_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)

# Crear marco para el historial
frame_historial = tk.LabelFrame(root, text="Historial de Organización", padx=10, pady=10)

# Área de texto desplazable para mostrar historial
historial = scrolledtext.ScrolledText(frame_historial, width=100, height=15, wrap=tk.WORD, state=tk.DISABLED)

# Posicionar historial en su marco
historial.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Función para organizar y renombrar archivos
def organizar_y_renombrar():
    carpeta_seleccionada = label_carpeta.cget('text').split(': ')[1]
    extensiones = extensiones_personalizadas_entry.get().split(',')
    prefijo = prefijo_entry.get()
    organizar_archivos(carpeta_seleccionada, check_subcarpetas_var.get(), extensiones, check_mover_no_reconocidos_var.get(), prefijo)

# Botón para organizar y renombrar archivos
btn_organizar = tk.Button(root, text="Organizar y Renombrar", command=organizar_y_renombrar, state=tk.DISABLED)

# Función para abrir la carpeta seleccionada en el explorador de archivos
btn_abrir_carpeta = tk.Button(root, text="Abrir Carpeta", command=abrir_carpeta_origen)

# Función para limpiar el historial
btn_limpiar_historial = tk.Button(root, text="Limpiar Historial", command=limpiar_historial)

# Posicionar marcos en la ventana principal
frame_configuracion.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)
frame_historial.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)
btn_organizar.pack(pady=10)
btn_abrir_carpeta.pack(pady=5)
btn_limpiar_historial.pack(pady=5)

# Ejecutar la interfaz
root.mainloop()
