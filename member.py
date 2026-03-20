from datetime import datetime, timedelta

class SubcriptionPlan:
    def __init__(self, plan_name, duration, plan_price):
        self.plan_name = plan_name
        self.duration = duration
        self.plan_price = plan_price

    def __str__(self):
        return f"{self.plan_name} - Duration: {self.duration}days - Price: {self.plan_price}"
    
    # add magic method 
    def __repr__(self):
        return f"SubcriptionPlan('{self.plan_name}', {self.duration}, {self.plan_price})"

    
class Member:
    # add for auto id 
    id_counter = 1   

    #  member_id moved to the end and default is None
    def __init__(self, name, sex, phone, plan, join_date, member_id=None):
        #auto id generation        
        if member_id is None:
            self.__member_id = Member.id_counter
            Member.id_counter += 1
        else:
            self.__member_id = member_id

        self.__name = name
        self.__sex = sex
        self.__phone = phone
        self.__plan = plan
        self.__join_date = join_date
        self.__expiry_date = self.__calculate_expiry()

    def __calculate_expiry(self):
        return self.__join_date + timedelta(days= self.__plan.duration)
    
    def get_member_id(self):
        return self.__member_id

    def get_name(self):
        return self.__name

    def get_phone(self):
        return self.__phone

    def get_sex(self):
        return self.__sex

    def get_plan(self):
        return self.__plan

    def get_join_date(self):
        return self.__join_date

    def set_phone(self, new_phone):
        if len(new_phone) >8 or len(new_phone) <=10:
            self.__phone = new_phone
            return True
        else:
            return False
        
    def set_plan(self, new_plan):
        self.__plan = new_plan
        self.__expiry_date = self.__calculate_expiry()

    def get_status(self):
        if datetime.now() <= self.__expiry_date:
            return "Active"
        else:
            return "Expired"
        
    def __str__(self):
        return (f"ID: M{self.get_member_id()} | Name: {self.get_name()} | {self.__sex} | "
                f"Phone: {self.get_phone()} | Plan: {self.__plan.plan_name} | "
                f"Exp: {self.__expiry_date.date()} | {self.get_status()}")
    
    # add magic method
    def __repr__(self):
        return f"Member('{self.__member_id}', '{self.__name}', '{self.__sex}', '{self.__phone}')"
