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

    print(company_data.name)
    print(f"P/E = {financial_data.market_price / financial_data.net_profit}")
    print(f"P/S = {financial_data.market_price / financial_data.sales}")
    print(f"P/B = {financial_data.market_price / financial_data.assets}")
    print(f"ND/EBITDA = {financial_data.net_debt / financial_data.ebitda}")
    print(f"ROE = {financial_data.net_profit / financial_data.equity}")
    print(f"ROA = {financial_data.net_profit / financial_data.assets}")
    print(f"L/A = {financial_data.liabilities / financial_data.assets}")



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

    
