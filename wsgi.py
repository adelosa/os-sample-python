import os
from sqlalchemy import String, Integer, Column, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask

Base = declarative_base()


class HelloTable(Base):
    __tablename__ = 'hello_table'

    id = Column(Integer, primary_key=True)
    greeting = Column(String, primary_key=True)


app = Flask(__name__)
db_url = 'postgresql://{user}:{pwd}@{host}/{db}'.format(host=os.environ['POSTGRESQL_SERVICE_HOST'], user=os.environ['DB_USER'], pwd=os.environ['DB_PASS'], db='hellodb')
app.engine = create_engine(db_url, echo=True)
Base.metadata.create_all(bind=app.engine)

app.db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=app.engine))
Base.query = app.db_session.query_property()


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
