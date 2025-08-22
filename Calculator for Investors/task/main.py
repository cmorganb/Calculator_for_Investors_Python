from menu_stack import MenuItem, MenuStack
from database import get_session, get_session_context
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

def create_company():
    session = get_session()

    ticker = input("Enter ticker (in the format 'MOON'):\n")
    name = input("Enter company (in the format 'Moon Corp'):\n")
    sector = input("Enter industries (in the format 'Technology'):\n")

    new_company = Companies(ticker=ticker, name=name, sector=sector)
    session.add(new_company)
    session.commit()

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
    search_term = input("Enter company name:\n")

    #call searching function
    #display search results menu


    menu_stack.pop_menu()

def update_company():
    search_term = input("Enter company name:\n")

    #call searching function
    #display search results menu

    ebitda = input("Enter ebitda (in the format '987654321'):\n")
    sales = input("Enter sales (in the format '987654321'):\n")
    net_profit = input("Enter net profit (in the format '987654321'):\n")
    market_price = input("Enter market price (in the format '987654321'):\n")
    net_debt = input("Enter net_debt (in the format '987654321'):\n")
    assets = input("Enter assets (in the format '987654321'):\n")
    equity = input("Enter equity (in the format '987654321'):\n")
    cash_equivalents = input("Enter cash equivalents (in the format '987654321'):\n")
    liabilities = input("Enter liabilities (in the format '987654321'):\n")

    #call function to update financial data

    print("Company updated successfully!")

    menu_stack.pop_menu()

def delete_company():
    search_term = input("Enter company name:\n")

    #call searching function
    #display search results menu

    #call fucntion to delete company

    print("Company deleted successfully!")

    menu_stack.pop_menu()

def list_all_companies():
    #call function to read all companies.

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





