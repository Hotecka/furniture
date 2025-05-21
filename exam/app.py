import tkinter as tk
from tkinter import messagebox, simpledialog
from material_utils import get_all_materials, add_material, edit_material, get_products_using_material
from calc import calculate_material_for_product


class MaterialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Склад материалов")

        self.materials_listbox = tk.Listbox(root, width=50)
        self.materials_listbox.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Обновить", command=self.load_materials).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Добавить", command=self.add_material).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_selected_material).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Продукция", command=self.show_products_for_selected_material).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Расчет", command=self.calculate_material).grid(row=0, column=4, padx=5)

        self.load_materials()

    def load_materials(self):
        self.materials_listbox.delete(0, tk.END)
        self.materials = get_all_materials()
        for mat in self.materials:
            self.materials_listbox.insert(tk.END, f"{mat[0]}. {mat[1]} — {mat[2]} {mat[3]}")

    def get_selected_material(self):
        selection = self.materials_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите материал")
            return None
        return self.materials[selection[0]]

    def add_material(self):
        name = simpledialog.askstring("Название", "Введите название материала:")
        if not name:
            return
        quantity = simpledialog.askfloat("Количество", "Введите количество:")
        unit = simpledialog.askstring("Ед. изм.", "Введите единицу измерения:")
        if quantity is not None and unit:
            add_material(name, quantity, unit)
            self.load_materials()

    def edit_selected_material(self):
        mat = self.get_selected_material()
        if not mat:
            return
        name = simpledialog.askstring("Новое название", "Введите название:", initialvalue=mat[1])
        quantity = simpledialog.askfloat("Новое количество", "Введите количество:", initialvalue=mat[2])
        unit = simpledialog.askstring("Новая ед. изм.", "Введите единицу:", initialvalue=mat[3])
        if name and quantity is not None and unit:
            edit_material(mat[0], name, quantity, unit)
            self.load_materials()

    def show_products_for_selected_material(self):
        mat = self.get_selected_material()
        if not mat:
            return
        products = get_products_using_material(mat[0])
        if products:
            prod_list = "\n".join([f"{p[0]}: {p[1]}" for p in products])
            messagebox.showinfo("Продукция", f"Материал используется в:\n{prod_list}")
        else:
            messagebox.showinfo("Продукция", "Материал не используется в продукции.")

    def calculate_material(self):
        mat = self.get_selected_material()
        if not mat:
            return  # Если ничего не выбрано — не продолжаем

        # Получаем список продукции, где используется материал
        products = get_products_using_material(mat[0])
        if not products:
            messagebox.showinfo("Нет данных", "Материал не используется ни в одной продукции.")
            return

        # Отображаем список продукции с номерами
        product_names = [f"{p[0]}: {p[1]}" for p in products]
        product_str = "\n".join([f"{i + 1}. {name}" for i, name in enumerate(product_names)])
        choice = simpledialog.askinteger("Выбор продукции", f"Выберите номер продукции:\n{product_str}")

        if not choice or choice < 1 or choice > len(products):
            messagebox.showwarning("Ошибка", "Неверный выбор.")
            return

        product_id, product_name = products[choice - 1]
        qty = simpledialog.askinteger("Количество изделий", f"Сколько '{product_name}' нужно произвести?")
        if qty is None:
            return

        from calc import calculate_material_for_product
        total = calculate_material_for_product(mat[0], product_id, qty)
        messagebox.showinfo("Расчет", f"Для {qty} шт. продукции '{product_name}' требуется:\n{total} {mat[3]}")



if __name__ == "__main__":
    root = tk.Tk()
    app = MaterialApp(root)
    root.mainloop()
