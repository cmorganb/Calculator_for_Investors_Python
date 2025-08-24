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
    with get_session_context() as session:
        # Check if database already has data
        company_count = session.query(Companies).count()
        if company_count > 0:
            # print("Database already contains data.")
            return

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
                        ticker=line['ticker'] if line['ticker'] else None,
                        name=line['name'] if line['name'] else None,
                        sector=line['sector'] if line['sector'] else None
                    )
                    session.merge(company)

                # Process financial data
                for line in fin_reader:
                    financial = Financial(
                        ticker=line['ticker'] if line['ticker'] else None,
                        ebitda=float(line['ebitda']) if line['ebitda'] else None,
                        sales=float(line['sales']) if line['sales'] else None,
                        net_profit=float(line['net_profit']) if line['net_profit'] else None,
                        market_price=float(line['market_price']) if line['market_price'] else None,
                        net_debt=float(line['net_debt']) if line['net_debt'] else None,
                        assets=float(line['assets']) if line['assets'] else None,
                        equity=float(line['equity']) if line['equity'] else None,
                        cash_equivalents=float(line['cash_equivalents']) if line['cash_equivalents'] else None,
                        liabilities=float(line['liabilities']) if line['liabilities'] else None,
                    )
                    session.merge(financial)

                # print("Database initialized from CSV files successfully!")

        except FileNotFoundError as e:
            print(f"Error: Could not find CSV file - {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise