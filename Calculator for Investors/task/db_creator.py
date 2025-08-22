import csv
from sqlalchemy import Column, Float, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError


def main():
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

    try:
        # Check if files exist
        with (
            open('companies.csv') as c,
            open('financial.csv') as f
        ):
            comp_reader = csv.DictReader(c, delimiter=",")
            fin_reader = csv.DictReader(f, delimiter=",")

            # Process companies
            for line in comp_reader:
                comp_dict = {}
                for col in comp_columns:
                    comp_dict[col] = line[col] if line[col].strip() else None

                comp_obj = Companies(**comp_dict)
                session.merge(comp_obj)  # Use merge instead of add to handle duplicates

            # Process financial data
            for line in fin_reader:
                fin_dict = {}
                for col in fin_columns:
                    if col == 'ticker':
                        fin_dict[col] = line[col] if line[col].strip() else None
                    else:
                        # Convert numeric columns, handle empty/invalid values
                        try:
                            fin_dict[col] = float(line[col]) if line[col].strip() else None
                        except (ValueError, TypeError):
                            fin_dict[col] = None

                fin_obj = Financial(**fin_dict)
                session.merge(fin_obj)  # Use merge instead of add to handle duplicates

            session.commit()
            print("Database created successfully!")

    except FileNotFoundError as e:
        print(f"Error: Could not find CSV file - {e}")
    except IntegrityError as e:
        session.rollback()
        print(f"Database integrity error: {e}")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


if __name__ == '__main__':
    main()