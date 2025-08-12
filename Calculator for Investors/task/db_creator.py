import csv
from sqlalchemy import Column, Float, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


def main():
    Base = declarative_base()

    class Companies(Base):
        __tablename__ = 'companies'

        ticker = Column(String(10), primary_key=True)
        name = Column(String(60))
        sector = Column(String(60))

    class Financial(Base):
        __tablename__ =  'financial'

        ticker = Column(String(10), primary_key=True)
        ebitda = Column(Float)
        sales = Column(Float)
        net_profit = Column(Float)
        market_price = Column(Float)
        net_debt = Column(Float)
        assets = Column(Float)
        equity = Column(Float)
        cash_equivalents = Column(Float)
        liabilities = Column(Float)


    engine = create_engine("sqlite:///investor.db", echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    comp_columns = ['ticker', 'name', 'sector']
    fin_columns = ['ticker', 'ebitda', 'sales', 'net_profit', 'market_price', 'net_debt', 'assets', 'equity',
                   'cash_equivalents', 'liabilities']

    with (
        open('companies.csv') as c,
        open('financial.csv') as f
    ):
        comp_reader = csv.DictReader(c, delimiter=",")
        fin_reader = csv.DictReader(f, delimiter=",")

        for line in comp_reader:
            for col in comp_columns:
                if not line[col]:
                    line[col] = None

            comp_dict = {col: line[col] for col in comp_columns}
            comp_obj = Companies(**comp_dict)
            session.add(comp_obj)

        for line in fin_reader:
            for col in fin_columns:
                if not line[col]:
                    line[col] = None

            fin_dict = {col: line[col] for col in fin_columns}
            fin_obj = Financial(**fin_dict)
            session.add(fin_obj)

        session.commit()

    print("Database created successfully!")

if __name__ == '__main__':
    main()





