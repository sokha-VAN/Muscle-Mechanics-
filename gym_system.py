import os
from datetime import datetime
from member import Member, SubcriptionPlan

class GymSystem:
    def __init__(self):
        self.__members = []
        self.__plans = {}
        # add file  handlig 
        self.__plan_file = "plans.txt"
        self.__member_file = "members.txt"

        self.load_plans()
        self.load_members()

    # add magic method
    def __len__(self):
        return len(self.__members)
    
    # add magic method
    def __contains__(self, phone):
        for member in self.__members:
            if member.get_phone() == phone:
                return True
        return False
    


    # ---------------- FILE HANDLING ----------------

    def save_plans(self):
        try:
            with open(self.__plan_file, "w") as file:
                for plan_id, plan in self.__plans.items():
                    file.write(f"{plan_id}|{plan.plan_name}|{plan.duration}|{plan.plan_price}\n")
        except Exception as e:
            print("Error saving plans:", e)

    def load_plans(self):
        if not os.path.exists(self.__plan_file):
            return

        try:
            with open(self.__plan_file, "r") as file:
                for line in file:
                    data = line.strip().split("|")
                    if len(data) == 4:
                        plan_id = data[0]
                        name = data[1]
                        duration = int(data[2])
                        price = float(data[3])
                        self.__plans[plan_id] = SubcriptionPlan(name, duration, price)
        except Exception as e:
            print("Error loading plans:", e)

    def save_members(self):
        try:
            with open(self.__member_file, "w") as file:
                for member in self.__members:
                    file.write(
                        f"{member.get_member_id()}|"
                        f"{member.get_name()}|"
                        f"{member.get_sex()}|"
                        f"{member.get_phone()}|"
                        f"{member.get_plan().plan_name}|"
                        f"{member.get_join_date().strftime('%d-%m-%Y')}\n"
                    )
        except Exception as e:
            print("Error saving members:", e)

    def load_members(self):
        if not os.path.exists(self.__member_file):
            return

        max_id = 0  

        try:
            with open(self.__member_file, "r") as file:
                for line in file:
                    data = line.strip().split("|")
                    if len(data) == 6:
                        mid = data[0]
                        name = data[1]
                        sex = data[2]
                        phone = data[3]
                        plan_name = data[4]
                        join_date = datetime.strptime(data[5], "%d-%m-%Y")

                        found_plan = None
                        for plan in self.__plans.values():
                            if plan.plan_name == plan_name:
                                found_plan = plan
                                break

                        if found_plan is not None:
                            # CHANGED: pass member_id at the end
                            member = Member(name, sex, phone, found_plan, join_date, mid)
                            self.__members.append(member)

                            # NEW: update counter from file
                            if mid.startswith("M"):
                                num = int(mid[1:])
                                if num > max_id:
                                    max_id = num

            Member.id_counter = max_id + 1   # NEW
        except Exception as e:
            print("Error loading members:", e)


    # ---------------- PLAN METHODS ----------------

    def add_subcription_plan(self):
        print("\n--- Create New Subscription Plan ---")
        name = input("Enter Subcription Plan Name: ").strip()

        try:
            duration = int(input("Enter Duration (days): "))
            price = float(input("Enter Price: $"))

            if duration <= 0 or price < 0:
                print("Duration must be positive and price cannot be negative.")
                return

            plan_id = str(len(self.__plans) + 1)
            self.__plans[plan_id] = SubcriptionPlan(name, duration, price)
            self.save_plans()
            print(f"Plan '{name}' added successfully!")

        except ValueError:
            print("Invalid input! Duration must be integer and price must be number.")

    def view_plans(self):
        print("\n--- Subscription Plans ---")
        if not self.__plans:
            print("No plans found!")
            return
        else:
            for k, v in self.__plans.items():
                print(f"{k}. {v}")


    # ---------------- MEMBER METHODS ----------------

    def add_member(self):
        if not self.__plans:
            print("ERROR: Create a plan first (Option 1).")
            return

        print("\n--- Add Member ---")
        name = input("Enter Name: ").strip()
    #check for valid input of sex
        while True:    
            sex = input("Enter Sex (M/F): ").lower().strip()
            if sex in [ "m", "f", "female", "male"]:
                if sex in ["m", "male"]:
                    sex = "M"
                else:
                    sex="F"
                break
            else:
                print("Invalid input! Please enter M, F, Male, or Female.")
                
        while True:
            phone = input("Enter Phone: (e.g. 012345678)").strip()
            if len(phone) <=8 or len(phone) >10:
                print("ERROR: phone number should be more than 8 and less than 10!")
                continue

            duplicate = False
            for x in self.__members:
                if x.get_phone() == phone:
                    print(f" ERROR: Phone already registered!")
                    duplicate = True
                    break
            if duplicate:
                continue
            break
        
        print("\nSelect Plan:")
        while True:

            self.view_plans()
            choice = input("Choice: ").strip()
            if choice not in self.__plans:
                print("please select the existing plan!")
                continue
            break
        while True:
            date_in = input("Enter Join Date (DD-MM-YYYY): ").strip()

            try:
                join_date = datetime.strptime(date_in, "%d-%m-%Y")
                break
            except ValueError:
                print("Invalid date format! Please use DD-MM-YYYY.")
        # CHANGED: no manual member id
        new_member = Member(name, sex, phone, self.__plans[choice], join_date)
        self.__members.append(new_member)
        self.save_members()
        print("Member registered!")
        print("Member ID:", new_member.get_member_id()) 
                

    def view_member(self):
        print("\n--- Current Members ---")
        if not self.__members:
            print("No  record founded!")
            return
        for m in self.__members:
            print(m)

    def search_member(self):
        print("\n--- Search Member ---")
        phone = input("Enter Phone Number:").strip()
        for x in self.__members:
            if x.get_phone() == phone:
                print(f"Found: {x}")    
                return
        print("No member found!")    

    # update_member
    def update_member(self):
        print("\n--- Update Member ---")
        phone = input("Enter Phone Number to update: ").strip() #search for member to update
        found_mem = None 
        for member in self.__members:
            if member.get_phone() == phone:
                found_mem = member
                break
        if not found_mem:
            print("Member not found")
            return
        
        print("Updating Member....")
        
        #insert new phone number
        new_phone = input("Enter new phone: ").strip()
        found_num = False
        for x in self.__members:
            if x.get_phone() == new_phone and x != found_mem:
                found_num = True
                break

        if len(new_phone) <= 8 or len(new_phone) > 10:
            print("Invalid length! Phone not updated.")

        elif found_num:
            print("ERROR: This phone number is already registered to another member!")
        else:
            found_mem.set_phone(new_phone)
            print("Phone updated successfully!")

        print("\nAvailable Plans:")
        self.view_plans()
        choice = input("Enter new plan choice: ").strip()

        if choice in self.__plans:
            found_mem.set_plan(self.__plans[choice])
            self.save_members()
            print("Member updated successfully!")
        else:
            print("Invalid plan choice!")
            return

        print("No member found!")

    def delete_member(self):
        print("\n--- Delete Member ---")
        phone = input("Enter Phone to delete:").strip()
        found = None
        for x in self.__members:
            if x.get_phone() == phone:
                found = x
                break
        if found:
            self.__members.remove(found)
            self.save_members()  
            print(f"Member with phone {phone} has been deleted.")
        else:
            print("No member found with that phone number!")
