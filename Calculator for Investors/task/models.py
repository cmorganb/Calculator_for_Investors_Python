from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
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

    def p_e(self):
        if self.market_price and self.net_profit and self.net_profit != 0:
            return round(self.market_price / self.net_profit, 2)
        return None

    def p_s(self):
        if self.market_price and self.sales and self.sales != 0:
            return round(self.market_price / self.sales, 2)
        return None

    def p_b(self):
        if self.market_price and self.assets and self.assets != 0:
            return round(self.market_price / self.assets, 2)
        return None

    @hybrid_property
    def nd_ebitda(self):
        if self.ebitda and self.net_debt and self.ebitda != 0:
            return round(self.net_debt / self.ebitda, 2)
        return None

    @hybrid_property
    def roe(self):
        if self.equity and self.net_profit and self.equity != 0:
            return round(self.net_profit / self.equity, 2)
        return None

    @hybrid_property
    def roa(self):
        if self.assets and self.net_profit and self.assets != 0:
            return round(self.net_profit / self.assets, 2)
        return None

    def l_a(self):
        if self.assets and self.liabilities and self.assets != 0:
            return round(self.liabilities / self.assets, 2)
        return None


