import csv
from backend.db_client import get_db

def import_buyers(csv_path="backend/data/buyers.csv"):
    conn = get_db()
    cur = conn.cursor()

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            sql = """
                INSERT INTO buyers (
                    name,
                    phone_whatsapp,
                    budget_min,
                    budget_max,
                    location_pref,
                    strategy,
                    notes
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                row["name"].strip(),
                row["whatsapp_number"].strip(),  # CSV column name
                int(row["budget_min"]) if row["budget_min"] else None,
                int(row["budget_max"]) if row["budget_max"] else None,
                row["location_pref"].strip(),
                row["strategy"].strip(),
                row.get("notes", "").strip(),
            )

            cur.execute(sql, values)

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Imported buyers from {csv_path}")


if __name__ == "__main__":
    import_buyers()
