from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Companies, Financial
from contextlib import contextmanager
import csv

engine = create_engine("sqlite:///investor.db", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_session_context():
    """Get a database session with context manager"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def initialize_db_from_files():
    """Initialize database from CSV files if database is empty"""
    with get_session_context as session:
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
                    company = Companies(
                        ticker=line['ticker'],
                        name=line['name'],
                        sector=line['sector']
                    )
                    session.merge(company)  # Use merge instead of add to handle duplicates

                # Process financial data
                for line in fin_reader:
                    financial = Financial(
                        ticker=line['ticker'],
                        ebitda=float(line['ebitda']),
                        sales=float(line['sales']),
                        net_profit=float(line['net_profit']),
                        market_price=float(line['market_price']),
                        net_debt=float(line['net_debt']),
                        assets=float(line['assets']),
                        equity=float(line['equity']),
                        cash_equivalents=float(line['cash_equivalents']),
                        liabilities=float(line['liabilities'])
                    )
                    session.merge(financial)

                session.commit()
                # print("Database created successfully!")

        except FileNotFoundError as e:
            print(f"Error: Could not find CSV file - {e}")
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()