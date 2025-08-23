from sqlalchemy import Column, Float, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

comp_columns = ['ticker', 'name', 'sector']
fin_columns = ['ticker', 'ebitda', 'sales', 'net_profit', 'market_price', 'net_debt', 'assets', 'equity',
               'cash_equivalents', 'liabilities']

Base = declarative_base()

class Companies(Base):
    __tablename__ = 'companies'

    ticker = Column(String(10), primary_key=True)
    name = Column(String(60))
    sector = Column(String(60))


class Financial(Base):
    __tablename__ = 'financial'

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
Base.metadata.create_all(engine, checkfirst=True)

Session = sessionmaker(bind=engine)
session = Session()


def create_company(ticker, name, sector):
    session.add(Companies(ticker=ticker, name=name, sector=sector))
    session.commit()

def read_company(ticker):
    company_data = session.query(Companies).filter(Companies.ticker == ticker).first()
    financial_data = session.query(Financial).filter(Financial.ticker == ticker).first()



def update_company(ticker, ebitda, sales, net_profit, market_price, net_debt, assets, equity,
               cash_equivalents, liabilities):
    query = session.query(Financial)
    company_to_update = query.filter(Financial.ticker == ticker)

    company_to_update.update({'ebitda': ebitda, 'sales': sales, 'net_profit': net_profit,
                              'market_price': market_price, 'net_debt': net_debt, 'assets': assets,
                              'equity': equity, 'cash_equivalents': cash_equivalents, 'liabilities': liabilities})
    session.commit()


def delete_company(ticker):
    query = session.query(Financial)
    company_to_delete = query.filter(Financial.ticker == ticker).delete()
    session.commit()

    
