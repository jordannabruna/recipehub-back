# seed.py
from app.database import SessionLocal
from app.roles.role_model import Role

db = SessionLocal()

# Verifica se já existem roles, se não, cria
if not db.query(Role).filter_by(name="admin").first():
    admin_role = Role(id=1, name="admin")
    db.add(admin_role)
    print("Role 'admin' criada.")

if not db.query(Role).filter_by(name="user").first():
    user_role = Role(id=2, name="user")
    db.add(user_role)
    print("Role 'user' criada.")

db.commit()
db.close()