import uuid
from dataclasses import dataclass
from contextlib import contextmanager

from sqlalchemy import create_engine, Table, MetaData, Column, String, Float, select, insert, update, delete

# Créer le moteur et les métadonnées
engine = create_engine('sqlite:///data.db')
metadata = MetaData()

# Définir la table "entries" avec SQLAlchemy Core
entries = Table(
    'entries',
    metadata,
    Column('id', String, primary_key=True),
    Column('name', String, nullable=False),
    Column('amount', Float, nullable=False),
    Column('category', String, nullable=True)
)


@dataclass
class Entry:
    id: uuid.UUID
    name: str
    amount: float
    category: str | None

    @classmethod
    def from_db(cls, id: str, name: str, amount: float, category: str | None):
        return cls(
            uuid.UUID(id),
            name,
            amount,
            category,
        )
        
        

@contextmanager
def get_db():
    
    """Fournir une connexion à la base de données sous forme de contexte."""
    conn = engine.connect()
    trans = conn.begin()
    try:
        yield conn
        trans.commit()
    except Exception as e:
        trans.rollback()
        raise e
    finally:
        conn.close()
        
        

def init_db():
    
    """Initialiser la base de données en créant toutes les tables."""
    metadata.create_all(engine)
    
    

def create_entry(name: str, amount: float, category: str | None = None) -> None:
    
    """Créer une nouvelle entrée dans la base de données."""
    with get_db() as conn:
        stmt = insert(entries).values(
            id=uuid.uuid4().hex,
            name=name,
            amount=amount,
            category=category
        )
        conn.execute(stmt)
        
        

def get_entry(id: uuid.UUID) -> Entry:
    
    """Récupérer une entrée par son ID."""
    with get_db() as conn:
        stmt = select(entries).where(entries.c.id == id.hex)
        result = conn.execute(stmt).first()
        if result:
            return Entry.from_db(result.id, result.name, result.amount, result.category)
        else:
            raise Exception(f"Entrée {id} non trouvée")
        
        

def get_all_entries() -> list[Entry]:
    
    """Récupérer toutes les entrées de la base de données."""
    with get_db() as conn:
        stmt = select(entries)
        results = conn.execute(stmt).fetchall()
        return [Entry.from_db(r.id, r.name, r.amount, r.category) for r in results]
    
    

def update_entry(id: uuid.UUID, name: str, amount: float, category: str | None) -> None:
    
    """Mettre à jour une entrée existante."""
    with get_db() as conn:
        stmt = update(entries).where(entries.c.id == id.hex).values(
            name=name,
            amount=amount,
            category=category
        )
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise Exception("Aucune entrée mise à jour")
        
        

def delete_entry(id: uuid.UUID) -> None:
    
    """Supprimer une entrée de la base de données."""
    with get_db() as conn:
        stmt = delete(entries).where(entries.c.id == id.hex)
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise Exception("Aucune entrée supprimée")