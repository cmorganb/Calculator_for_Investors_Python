from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Companies(Base):
    __tablename__ = 'companies'

    ticker = Column(String(10), primary_key=True)
    name = Column(String(60))
    sector = Column(String(60))

    financial = relationship("Financial", back_populates="company", uselist=False)

class Financial(Base):
    __tablename__ = 'financial'

    ticker = Column(String(10), ForeignKey('companies.ticker'), primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)

    company = relationship('Companies', back_populates='financial')