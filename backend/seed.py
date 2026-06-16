from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import Category, SlaPolicy, Department, TicketPriority

def seed_database():
    db: Session = SessionLocal()
    try:
        print("🌱 Starting database seeding process...")

        # 1. SEED CATEGORIES
        default_categories = ["Network", "Printer/Hardware", "Software/ERP", "Radiology Systems", "Finance Systems"]
        print(f"Checking categories...")
        for cat_name in default_categories:
            # Prevent duplication if script is run multiple times
            existing = db.query(Category).filter_by(name=cat_name).first()
            if not existing:
                category = Category(name=cat_name)
                db.add(category)
                print(f"   [+] Added Category: {cat_name}")

        # 2. SEED SLA POLICIES
        # Maps TicketPriority enums to your specific response/resolution time targets
        sla_targets = [
            {"priority": TicketPriority.low, "response": 24, "resolution": 72},
            {"priority": TicketPriority.medium, "response": 8, "resolution": 24},
            {"priority": TicketPriority.high, "response": 2, "resolution": 8},
            {"priority": TicketPriority.critical, "response": 1, "resolution": 2},
        ]
        print(f"Checking SLA policies...")
        for target in sla_targets:
            existing = db.query(SlaPolicy).filter_by(priority=target["priority"]).first()
            if not existing:
                policy = SlaPolicy(
                    priority=target["priority"],
                    response_time_hours=target["response"],
                    resolution_time_hours=target["resolution"]
                )
                db.add(policy)
                print(f"   [+] Added SLA Policy for priority: {target['priority'].value}")

        # 3. SEED DEPARTMENTS
        # (Using 'bcrypt_placeholder_hash' for now until you implement authentication hashing)
        sample_departments = [
            {"name": "Finance Department", "code": "FIN", "phone": "+254711223344"},
            {"name": "Radiology Department", "code": "RAD", "phone": "+254722334455"},
            {"name": "Insurance/Billing", "code": "INS", "phone": "+254733445566"},
        ]
        print(f"Checking departments...")
        for dept in sample_departments:
            existing = db.query(Department).filter_by(dept_code=dept["code"]).first()
            if not existing:
                department = Department(
                    name=dept["name"],
                    dept_code=dept["code"],
                    password_hash="bcrypt_placeholder_hash",  # Replace later with real hash
                    phone_number=dept["phone"],
                    is_active=True
                )
                db.add(department)
                print(f"   [+] Added Department: {dept['name']} ({dept['code']})")

        # Commit everything cleanly to Postgres
        db.commit()
        print("✅ Database seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed! Transaction rolled back.")
        print(f"Error details: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
