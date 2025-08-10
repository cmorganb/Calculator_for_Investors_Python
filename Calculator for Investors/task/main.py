from menu_stack import MenuItem, MenuStack

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
    print("Not implemented!")
    menu_stack.pop_menu()

def read_company():
    print("Not implemented!")
    menu_stack.pop_menu()

def update_company():
    print("Not implemented!")
    menu_stack.pop_menu()

def delete_company():
    print("Not implemented!")
    menu_stack.pop_menu()

def list_all_companies():
    print("Not implemented!")
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


menu_stack = MenuStack()
main_items = [
    MenuItem("CRUD", show_crud_menu, "CRUD operations"),
    MenuItem("TOP TEN", show_top_ten_menu, "Show top ten companies by criteria")
]

menu_stack.push_menu(main_items, "MAIN")
menu_stack.run()





