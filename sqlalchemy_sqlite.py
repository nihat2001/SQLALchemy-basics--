from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()
engine = create_engine(
        "sqlite:///chatbot.db", echo = True
)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key = True, autoincrement = True)
    role = Column(String, nullable = False)
    content = Column(String, nullable = False)

    def __repr__(self):
        return f"Message(id = {self.id}, role = {self.role}, content = {self.content})"

print(f"[SYSTEM] - DataBase and table are creating... ")   
Base.metadata.create_all(engine)
print(f"[SYSTEM] - DataBase and table are created!")   

print(f"Messages are creating...")
with Session(engine) as session:
    try:
        existing = session.query(Message).count()
        if existing == 0:
            msg_1 = Message(role = "user", content = "Hi! Been curious, as a shortly what's actually Python?")
            msg_2 = Message(role = "assistant", content = "Greetings! As a shortly Python is a programming language.")
            msg_3 = Message(role = "user", content = "Got it! Appreciates for your effort!")

            session.add_all([msg_1, msg_2, msg_3])
            session.commit()
            print(f"Messages are successfully created!")
        else:
            print(f"Already has {existing} messages, skipping.")
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Some problem happened:{e}")

print(f"Reading session opening...")
with Session(engine) as session:
    try:
        msg_list = [session.get(Message, msg_id) for msg_id in [1, 2, 3]]

        for msg in msg_list:
            if msg:
                print(f"{msg.role.upper()}: {msg.content}")
            else:
                print(f"Messages could't found...")
    except Exception as e:
        print(f"Reading session failed:{e}")

print(f"[SYSTEM] - Execution finished!")