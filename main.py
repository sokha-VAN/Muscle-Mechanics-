from gym_system import GymSystem

# ---------------- MENU ----------------
def  menu(system):
    
    while True:
        print("\n--- Gym Membership System ---")
        print("1. Add Plan")
        print("2. View Plans")
        print("3. Add Member")
        print("4. View All Members")
        print("5. Search Member")
        print("6. Update Member")
        print("7. Delete Member")
        print("8. Exit")

        c = input("Option: ").strip()

        if c == "1":
            system.add_subcription_plan()
        elif c == "2":
            system.view_plans()
        elif c == "3":
            system.add_member()
        elif c == "4":
            system.view_member()
        elif c == "5":
            system.search_member()
        elif c == "6":
            system.update_member()
        elif c == "7":
            system.delete_member()
        elif c == "8":
            print("Thank you for using Gym Membership System.")
            break
        else:
            print("Invalid option! Please try again.")

if __name__ == "__main__":
    gym = GymSystem()
    menu(gym)
    
