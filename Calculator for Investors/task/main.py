from menu_stack import MenuItem, MenuStack
from database import get_session
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
        MenuItem("ND/EBITDA", list_by_ebitda, "List by ND/EBITDA"),
        MenuItem("ROE", list_by_roe, "List by ROE"),
        MenuItem("ROA", list_by_roa, "List by ROA")
    ]

    menu_stack.push_menu(top_ten_items, "TOP TEN", )

def search_company():
    session = get_session()

    search_term = input("Enter company name:\n")

    results = session.query(Companies).filter(
        Companies.name.ilike(f'%{search_term}%')
    ).order_by(Companies.name).all()

    if results:
        for i, company in enumerate(results):
            print(f"{i} {company.name}")

        selection = int(input("Enter company number:\n"))
        return results[selection]
    else:
        print("Company not found!")
        return None

def create_company():
    session = get_session()

    ticker = input("Enter ticker (in the format 'MOON'):\n")
    name = input("Enter company (in the format 'Moon Corp'):\n")
    sector = input("Enter industries (in the format 'Technology'):\n")

    new_company = Companies(ticker=ticker, name=name, sector=sector)
    session.add(new_company)

    ebitda = float(input("Enter ebitda (in the format '987654321'):\n"))
    sales = float(input("Enter sales (in the format '987654321'):\n"))
    net_profit = float(input("Enter net profit (in the format '987654321'):\n"))
    market_price = float(input("Enter market price (in the format '987654321'):\n"))
    net_debt = float(input("Enter net_debt (in the format '987654321'):\n"))
    assets = float(input("Enter assets (in the format '987654321'):\n"))
    equity = float(input("Enter equity (in the format '987654321'):\n"))
    cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'):\n"))
    liabilities = float(input("Enter liabilities (in the format '987654321'):\n"))

    new_financial = Financial(ebitda=ebitda, sales=sales, net_profit=net_profit, market_price=market_price,
                              net_debt=net_debt, assets=assets, equity=equity, cash_equivalents=cash_equivalents,
                              liabilities=liabilities)
    session.add(new_financial)
    session.commit()

    print("Company created successfully!")

    menu_stack.pop_menu()

def read_company():
    fin_data = search_company()

    if fin_data:
        print(f"P/E = {fin_data.market_price / fin_data.net_profit}")
        print(f"P/S = {fin_data.market_price / fin_data.sales}")
        print(f"P/B = {fin_data.market_price / fin_data.assets}")
        print(f"ND/EBITDA = {fin_data.net_debt / fin_data.EBITDA}")
        print(f"ROE = {fin_data.net_profit / fin_data.equity}")
        print(f"ROA = {fin_data.net_profit / fin_data.assets}")
        print(f"L/A = {fin_data.liabilities / fin_data.assets}")

    menu_stack.pop_menu()

def update_company():
    fin_data = search_company()

    if fin_data:
        session = get_session()
        fin_data.ebitda = float(input("Enter ebitda (in the format '987654321'):\n"))
        fin_data.sales = float(input("Enter sales (in the format '987654321'):\n"))
        fin_data.net_profit = float(input("Enter net profit (in the format '987654321'):\n"))
        fin_data.market_price = float(input("Enter market price (in the format '987654321'):\n"))
        fin_data.net_debt = float(input("Enter net_debt (in the format '987654321'):\n"))
        fin_data.assets = float(input("Enter assets (in the format '987654321'):\n"))
        fin_data.equity = float(input("Enter equity (in the format '987654321'):\n"))
        fin_data.cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'):\n"))
        fin_data.liabilities = float(input("Enter liabilities (in the format '987654321'):\n"))

        session.commit()
        print("Company updated successfully!")

    menu_stack.pop_menu()

def delete_company():
    fin_data = search_company()

    if fin_data:
        session = get_session()
        comp_data = session.get(Companies, fin_data.ticker)
        session.delete(fin_data)
        session.delete(comp_data)
        session.commit()

        print("Company deleted successfully!")

    menu_stack.pop_menu()

def list_all_companies():
    session = get_session()
    companies = session.query(Companies).order_by(Companies.ticker).all()

    if companies:
        print("COMPANY LIST")

        for company in companies:
            print(f"{company.ticker} {company.name}")

    else:
        print("No companies in the database")

    menu_stack.pop_menu()

def list_by_ebitda():
    print("Not implemented!")
    menu_stack.pop_menu()

def list_by_roe():
    print("Not implemented!")
    menu_stack.pop_menu()

def list_by_roa():
    print("Not implemented!")
    menu_stack.pop_menu()


def main():
    main_items = [
        MenuItem("CRUD", show_crud_menu, "CRUD operations"),
        MenuItem("TOP TEN", show_top_ten_menu, "Show top ten companies by criteria")
    ]

    menu_stack.push_menu(main_items, "MAIN")
    menu_stack.run()


if __name__ == "__main__":
    menu_stack = MenuStack()
    main()





