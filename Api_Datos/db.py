from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

USUARIO = "admin"
CLAVE = "123"
HOST = "localhost"
PUERTO = "5432"
NOMBRE_BD = "datos"

# PostgreSQL URL de conexión
DATABASE_URL = f"postgresql+psycopg2://{USUARIO}:{CLAVE}@{HOST}:{PUERTO}/{NOMBRE_BD}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


