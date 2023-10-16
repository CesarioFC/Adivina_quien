import tkinter as tk
from tkinter import messagebox
import pickle

class AnimalGuessingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Juego de Adivinar Animales")
        self.tree_filename = "animal_tree.pkl"

        # Intenta cargar el árbol desde el archivo, o crea un nuevo árbol si no se puede cargar
        self.current_node = self.load_tree() if self.load_tree() else self.create_default_tree()

        self.initialize_game()

    def initialize_game(self):
        self.label = tk.Label(self.master, text="Piensa en un animal y yo trataré de adivinarlo.")
        self.label.pack(pady=10)

        self.play_button = tk.Button(self.master, text="Empezar a jugar", command=self.play_game)
        self.play_button.pack(pady=10)

        self.play_again_button = tk.Button(self.master, text="Jugar de nuevo", command=self.play_again)
        self.play_again_button.pack(pady=10)
        self.play_again_button.config(state=tk.DISABLED)

        self.new_animal_windows = []

    def play_game(self):
        self.label.config(text="")
        self.play_button.config(state=tk.DISABLED)
        self.adivinar_animal(self.current_node)

    def play_again(self):
        self.label.config(text="")
        self.adivinar_animal(self.current_node)

    def adivinar_animal(self, nodo):
        if nodo.izquierda:
            respuesta = messagebox.askyesno(nodo.valor, icon='question')
            if respuesta:
                self.adivinar_animal(nodo.izquierda)
            else:
                self.adivinar_animal(nodo.derecha)
        else:
            respuesta_final = messagebox.askyesno("¿Es un " + nodo.valor + "?", icon='question')
            if respuesta_final:
                self.animal_adivinado(nodo.valor)
            else:
                self.pensar_nuevo_animal()

    def animal_adivinado(self, animal_adivinado):
        respuesta = messagebox.askyesno("¡Adiviné!", "El animal que pensaste es un " + animal_adivinado + ".\n¿Es correcto?")
        if respuesta:
            messagebox.showinfo("Genial", "¡Gracias por jugar!")
            self.play_again_button.config(state=tk.NORMAL)
        else:
            self.pensar_nuevo_animal()

    def pensar_nuevo_animal(self):
        new_animal_window = tk.Toplevel(self.master)
        new_animal_window.title("No adivinado - Ingresa un nuevo animal y una pregunta")

        tk.Label(new_animal_window, text="No he adivinado. Ingresa un nuevo animal y una pregunta para distinguirlo de los demás.").pack(pady=10)

        nuevo_animal_label = tk.Label(new_animal_window, text="Animal:")
        nuevo_animal_label.pack()
        new_animal_entry = tk.Entry(new_animal_window)
        new_animal_entry.pack()

        nueva_pregunta_label = tk.Label(new_animal_window, text="Pregunta para distinguir:")
        nueva_pregunta_label.pack()
        new_question_entry = tk.Entry(new_animal_window)
        new_question_entry.pack()

        aceptar_button = tk.Button(new_animal_window, text="Aceptar", command=lambda: self.agregar_nuevo_animal(new_animal_entry.get(), new_question_entry.get()))
        aceptar_button.pack(pady=10)

        self.new_animal_windows.append(new_animal_window)

    def agregar_nuevo_animal(self, nuevo_animal, nueva_pregunta):
        if nuevo_animal and nueva_pregunta:
            # Guarda la información del nodo actual
            nodo_actual = self.current_node
            nodo_nueva_pregunta = Nodo(nueva_pregunta)
            nodo_nuevo_animal = Nodo(nuevo_animal)

            # Crea nuevos nodos para el animal pensado y el animal ingresado
            nodo_actual.valor = nueva_pregunta
            nodo_actual.izquierda = nodo_nueva_pregunta
            nodo_actual.derecha = nodo_nuevo_animal

            messagebox.showinfo("¡Gracias por enseñarme!", "Vamos a jugar de nuevo.")

            for window in self.new_animal_windows:
                window.destroy()

            self.play_again_button.config(state=tk.NORMAL)
            self.save_tree()  # Guarda el árbol después de agregar nueva información

    def save_tree(self):
        try:
            with open(self.tree_filename, 'wb') as file:
                pickle.dump(self.current_node, file)
        except Exception as e:
            messagebox.showerror("Error", "No se pudo guardar el árbol: " + str(e))

    def load_tree(self):
        try:
            with open(self.tree_filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return None
        except Exception as e:
            messagebox.showerror("Error", "No se pudo cargar el árbol: " + str(e))
            return None

    def create_default_tree(self):
        root_node = Nodo("¿Es mamífero?")
        root_node.izquierda = Nodo("Perro")
        root_node.derecha = Nodo("Pájaro")
        return root_node


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalGuessingGame(root)
    root.mainloop()
