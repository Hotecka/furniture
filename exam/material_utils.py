import sqlite3

DB_PATH = 'bd2'

def get_all_materials():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, quantity, unit FROM materials")
    materials = cursor.fetchall()
    conn.close()
    return materials

def add_material(name, quantity, unit):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO materials (name, quantity, unit) VALUES (?, ?, ?)", (name, quantity, unit))
    conn.commit()
    conn.close()

def edit_material(material_id, name, quantity, unit):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE materials SET name = ?, quantity = ?, unit = ? WHERE id = ?", (name, quantity, unit, material_id))
    conn.commit()
    conn.close()

def get_products_using_material(material_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.name
        FROM products p
        JOIN product_materials pm ON p.id = pm.product_id
        WHERE pm.material_id = ?
    """, (material_id,))
    products = cursor.fetchall()
    conn.close()
    return products
