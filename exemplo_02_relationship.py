from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    todos: list['Todo'] = Relationship()

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    status: str = 'todo'

    # nome do banco minusculo.id para relacionamento entre tabelas
    person_id: int = Field(foreign_key='person.id')


# Conexão com o banco
engine = create_engine('sqlite:///db.db')

# Tudo feito com herança do SQLModel vai ser crido nesse metadata.create_all
SQLModel.metadata.create_all(engine)


# Dentro da sessão(utilizando a engine) para fazer operações no banco, usa-se
# session.refresh é utilizado para usar os valores de dentro do banco, não da variavel em código
with Session(engine) as session:
    query = (
        select(Person).where(Person.id == 2)
    )

    result = session.exec(query).first()
    
    print(result)
    print(result.todos)