class MenuItem:
    def __init__(self, title, action, description):
        self.title = title
        self.action = action
        self.description = description

class MenuStack:
    def __init__(self):
        self.stack = []
        self.running = True

    def push_menu(self, menu_items, title):
        """Go into a submenu"""
        self.stack.append({"title": title, "items": menu_items})

    def pop_menu(self):
        """Go back to the previous menu"""
        if len(self.stack) > 1:
            self.stack.pop()
        else:
            self.running = False

    def display_current(self):
        if not self.stack:
            return

        current = self.stack[-1]
        print(f"\n{current['title'].upper()} MENU")
        print("0 Back" if len(self.stack) > 1 else "0 Exit")
        for i, item in enumerate(current['items'], 1):
            print(f"{i} {item.description}")

    def handle_input(self):
        try:
            choice = int(input("Enter an option:\n"))
            if choice == 0:
                self.pop_menu()

            else:
                current = self.stack[-1]
                if 1 <= choice <= len(current['items']):
                    current['items'][choice-1].action()
                else:
                    raise IndexError
        except (ValueError, IndexError):
            print("Invalid option!")

    def run(self):
        while self.running and self.stack:
            self.display_current()
            self.handle_input()

        print("Have a nice day!")  # exit message