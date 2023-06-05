from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

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
    p = Person(name='João')
    session.add(p)
    session.commit()
    # Trás as informações do banco para o código
    # Linha 34. será reconhecido as informações que estão na base para pegar o p.id
    session.refresh(p)
    print(p)

    t = Todo(title='Estudar', status='Doing', person_id=p.id)
    session.add(t)
    session.commit()
    print(t)

    # Query
    """
    Metodos do exec
    - all: pega todo
    - one: pega um
    - first: pega o primeiro
    - partition: particiona a saida
    """
    query = select(Todo)
    exec_retorno = session.exec(query).all()
    print(exec_retorno)

    query_2 = select(Todo).where(Todo.id > 50)
    exec_retorno = session.exec(query_2).all()
    print(exec_retorno)
  
    """
    Métodos 'query'
    - where: Condição de busca
    - offset:
    - order_by: Ordenação dos resultados
    - limit: limita retorno em numero definido
    """

    query_3 = (
        select(Todo) # Tabela/Objecto: Todo
        .limit(6) # Limitando resultado em 6
        #.order_by(Todo.id.desc(), Todo.id) # Ordenando resultados
        .offset(0) # Paginação, começa a partir do x
    )

    result = session.query(query_3).all()
    print(result)

    query_4 = (
        select(Todo) # Tabela/Objecto: Todo
        .limit(20) # Limitando resultado em 6
        .order_by(Todo.title) # Ordenando resultados
        .offset(12) # Paginação, começa a partir da dow x
        .where(Todo.status == 'done')
    )

    result = session.query(query_4).all()
    print(result)

    query_5 = (
        select(Todo) # Tabela/Objecto: Todo
        .join(Person)
        .limit(20) # Limitando resultado em 6
        .order_by(Todo.title) # Ordenando resultados
        .offset(12) # Paginação, começa a partir da dow x
        .where(Todo.status == 'done', Person.id == 2)
    )

    result = session.query(query_5).all()
    print(result)