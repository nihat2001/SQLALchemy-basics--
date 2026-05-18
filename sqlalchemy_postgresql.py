import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, Session

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

Base = declarative_base()
engine = create_engine(
        f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/postgres",
        echo = True
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)   
    name = Column(String(100))               
    email = Column(String(200), unique = True) 

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"

print(f"[SYSTEM] - DataBase and table are creating... ")  
Base.metadata.create_all(engine)
print(f"[SYSTEM] - DataBase and table are created!")

with Session(engine) as session:
    try:
        existing = session.query(User).count()
        if existing == 0:
            user_1 = User(name = "Nick", email = "n.brown@email.com")
            user_2 = User(name = "Mike", email = "m.nelson@email.com")
            
            session.add_all([user_1, user_2])
            session.commit()
        else:
            print(f"Already has {existing} user, skipping.")
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Some problem happened:{e}")

print(f"Reading session opening...")
with Session(engine) as session:
    try:
        user_list = [session.get(User, user_id) for user_id in [1, 2]]

        for usr in user_list:
            if usr:
                print(f"{usr.name}: {usr.email}")
            else:
                print(f"User couldn't found...")
    except Exception as e:
        print(f"Reading session failed:{e}")

print(f"[SYSTEM] - Execution finished!")