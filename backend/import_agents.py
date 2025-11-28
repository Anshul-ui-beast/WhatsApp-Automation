import csv
from backend.db_client import get_db

def import_agents(csv_path="backend/data/agents.csv"):
    """
    Imports agents from CSV into the agents table.
    CSV must contain columns:
        name, phone, agency, city
    These will be mapped to DB columns:
        name → name
        agency → agency_name
        phone → phone_whatsapp
        city → source   (temporary use)
    """

    conn = get_db()
    cur = conn.cursor()

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            sql = """
            INSERT INTO agents (name, agency_name, phone_whatsapp, email, source)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                row["name"],
                row["agency_name"],
                row["phone_whatsapp"],
                None,       # email column not provided → default None
                row["source"] # temporary use of "source"
            )

            cur.execute(sql, values)

    conn.commit()
    cur.close()
    conn.close()
    print("✔ CSV imported successfully!")
    

# Run directly
if __name__ == "__main__":
    import_agents()
