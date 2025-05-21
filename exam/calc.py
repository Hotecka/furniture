import sqlite3

def calculate_material_for_product(material_id, product_id, product_quantity, db_path='bd2'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT quantity FROM product_materials
        WHERE material_id = ? AND product_id = ?
    """, (material_id, product_id))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0] * product_quantity
    else:
        return 0  # Материал не используется в этом продукте например металл
