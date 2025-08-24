from menu_stack import MenuItem, MenuStack
from database import get_session_context, create_tables, initialize_db_from_files
from models import Companies, Financial

def show_crud_menu():
    crud_items = [
        MenuItem("Create", create_company, "Create a company"),
        MenuItem("Read", read_company, "Read a company"),
        MenuItem("Update", update_company, "Update a company"),
        MenuItem("Delete", delete_company, "Delete a company"),
        MenuItem("List", list_all_companies, "List all companies")
    ]

    menu_stack.push_menu(crud_items, "CRUD")

def show_top_ten_menu():
    top_ten_items = [
        MenuItem("ND/EBITDA", list_by_nd_ebitda, "List by ND/EBITDA"),
        MenuItem("ROE", list_by_roe, "List by ROE"),
        MenuItem("ROA", list_by_roa, "List by ROA")
    ]

    menu_stack.push_menu(top_ten_items, "TOP TEN", )

def search_company():
    with get_session_context() as session:
        search_term = input("Enter company name:\n")

        results = session.query(Companies).filter(
            Companies.name.ilike(f'%{search_term}%')
        ).all()

        if results:
            for i, company in enumerate(results):
                print(f"{i} {company.name}")

            selection = int(input("Enter company number:\n"))
            return results[selection].ticker
        else:
            print("Company not found!")
            return None

def create_company():
    with get_session_context() as session:
        ticker = input("Enter ticker (in the format 'MOON'):\n")
        name = input("Enter company (in the format 'Moon Corp'):\n")
        sector = input("Enter industries (in the format 'Technology'):\n")

        new_company = Companies(ticker=ticker, name=name, sector=sector)
        session.add(new_company)

        ebitda = float(input("Enter ebitda (in the format '987654321'):\n"))
        sales = float(input("Enter sales (in the format '987654321'):\n"))
        net_profit = float(input("Enter net profit (in the format '987654321'):\n"))
        market_price = float(input("Enter market price (in the format '987654321'):\n"))
        net_debt = float(input("Enter net debt (in the format '987654321'):\n"))
        assets = float(input("Enter assets (in the format '987654321'):\n"))
        equity = float(input("Enter equity (in the format '987654321'):\n"))
        cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'):\n"))
        liabilities = float(input("Enter liabilities (in the format '987654321'):\n"))

        new_financial = Financial(ticker=ticker, ebitda=ebitda, sales=sales, net_profit=net_profit, market_price=market_price,
                                  net_debt=net_debt, assets=assets, equity=equity, cash_equivalents=cash_equivalents,
                                  liabilities=liabilities)
        session.add(new_financial)

    print("Company created successfully!")

    menu_stack.pop_menu()

def read_company():
    ticker = search_company()

    if ticker:
        with get_session_context() as session:
            fin_data = session.get(Financial, ticker)
            comp_data = session.get(Companies, ticker)

            if fin_data:
                print(f"{comp_data.ticker} {comp_data.name}")
                print(f"P/E = {display_indicator(fin_data.p_e())}")
                print(f"P/S = {display_indicator(fin_data.p_s())}")
                print(f"P/B = {display_indicator(fin_data.p_b())}")
                print(f"ND/EBITDA = {display_indicator(fin_data.nd_ebitda)}")
                print(f"ROE = {display_indicator(fin_data.roe)}")
                print(f"ROA = {display_indicator(fin_data.roa)}")
                print(f"L/A = {display_indicator(fin_data.l_a())}")

    menu_stack.pop_menu()

def update_company():
    ticker = search_company()

    if ticker:
        with get_session_context() as session:
            fin_data = session.get(Financial, ticker)  # re-attaching the object to the session

            if fin_data:
                fin_data.ebitda = float(input("Enter ebitda (in the format '987654321'):\n"))
                fin_data.sales = float(input("Enter sales (in the format '987654321'):\n"))
                fin_data.net_profit = float(input("Enter net profit (in the format '987654321'):\n"))
                fin_data.market_price = float(input("Enter market price (in the format '987654321'):\n"))
                fin_data.net_debt = float(input("Enter net debt (in the format '987654321'):\n"))
                fin_data.assets = float(input("Enter assets (in the format '987654321'):\n"))
                fin_data.equity = float(input("Enter equity (in the format '987654321'):\n"))
                fin_data.cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'):\n"))
                fin_data.liabilities = float(input("Enter liabilities (in the format '987654321'):\n"))

                print("Company updated successfully!")

    menu_stack.pop_menu()

def delete_company():
    ticker = search_company()

    if ticker:
        with get_session_context() as session:
            fin_data = session.get(Financial, ticker)  # re-attaching the object to the session
            comp_data = session.get(Companies, fin_data.ticker)

            session.delete(fin_data)
            session.delete(comp_data)

        print("Company deleted successfully!")

    menu_stack.pop_menu()

def list_all_companies():
    with get_session_context() as session:
        companies = session.query(Companies).order_by(Companies.ticker).all()

        if companies:
            print("COMPANY LIST")

            for company in companies:
                print(f"{company.ticker} {company.name} {company.sector}")

        else:
            print("No companies in the database")

    menu_stack.pop_menu()

def list_by_nd_ebitda():
    with get_session_context() as session:
        top_nd_ebitda = (session.query(Financial)
                         .filter(Financial.equity != 0)
                         .order_by(Financial.nd_ebitda.desc())
                         .limit(10)
                         .all())

        for company in top_nd_ebitda:
            print(f"{company.ticker} {display_indicator(company.nd_ebitda)}")

    menu_stack.pop_menu()

def list_by_roe():
    with get_session_context() as session:
        top_roe = (session.query(Financial)
                         .filter(Financial.equity != 0)
                         .order_by(Financial.roe.desc())
                         .limit(10)
                         .all())

        for company in top_roe:
            print(f"{company.ticker} {display_indicator(company.roe)}")

    menu_stack.pop_menu()

def list_by_roa():
    with get_session_context() as session:
        top_roa = (session.query(Financial)
                         .filter(Financial.equity != 0)
                         .order_by(Financial.roa.desc())
                         .limit(10)
                         .all())

        for company in top_roa:
            print(f"{company.ticker} {display_indicator(company.roa)}")

    menu_stack.pop_menu()

def display_indicator(indicator):
    if indicator:
        return(indicator, 2)

    return None

def main():
    create_tables()
    initialize_db_from_files()

    main_items = [
        MenuItem("CRUD", show_crud_menu, "CRUD operations"),
        MenuItem("TOP TEN", show_top_ten_menu, "Show top ten companies by criteria")
    ]

    print("Welcome to the Investor Program!")
    menu_stack.push_menu(main_items, "MAIN")
    menu_stack.run()


if __name__ == "__main__":
    menu_stack = MenuStack()
    main()





