import random
import numpy as np
import pandas as pd
import math


data = {
  "married_household / house 2+ people": 0.45,
  "family household": 0.38,
  "household with chd": 0.106,
  "household with 65+": 0.082,
  "household with 65+ with 1 person": 0.481,
  "1 people per household": 0.526,
  "2 people per household": 0.817,
  "3 people per household": 0.88,
  "4 people per household": 0.962,
  "5 people per household": 1,
  "1 childs": 0.476,
  "2 childs": 0.819,
  "3 childs": 1,
  "employed percent": 0.786,
  "travel to work by car": 0.4,
  "travel to work by public trans": 0.592,
  "travel to work by 2 wheeled vehicle": 0.679,
  "travel to work by bicycle": 0.705,
  "travel to work by foot": 0.959,
  "travel to work by other": 1,
  "iterations": 800,
  "result": [],
}


def make_data():
    for i in range(data["iterations"]):
        def get_people_num():
            if i <= 421:
                return 1
            elif 421 < i <= 654:
                return 2
            elif 654 < i <= 704:
                return 3
            elif 704 < i <= 770:
                return 4
            else:
                return 5

            # get random num for calculate is married related to the data dict
        def get_is_married_rand(people_per_household):
            if people_per_household >= 2:
                rand_married = np.random.random_sample()
            else:
                rand_married = 0.999
            return rand_married

        # output if married = 1 // if not = 0
        def get_is_married_bin(is_married):
            if is_married < data["married_household / house 2+ people"]:
                return 1
            else:
                return 0

        def get_rand_child(people_per_household):
            chd_rand = np.random.random_sample()
            if people_per_household > 2 and chd_rand < data["household with chd"]:
                return chd_rand
            else:
                return 100

        def get_childs_num(childs_rand, people_per_household):
            if childs_rand <= data["1 childs"]:
                return 1
            elif data["1 childs"] < childs_rand <= data["2 childs"] and people_per_household > 2:
                return 2
            elif data["2 childs"] < childs_rand <= data["3 childs"] and people_per_household > 3:
                return 3
            elif 4 <= people_per_household <= 5:
                return random.randint(0, 3)
            else:
                return 0

        def get_adults_num(childs_num, people_per_household):
            pph = people_per_household
            cn = childs_num
            return pph - cn

        def get_rand_employed():
            rand_emp = np.random.random_sample()
            return rand_emp

        def get_employed_num(adults_num, rand_emp_value):
            if rand_emp_value > data["household with 65+"]:
                adt = adults_num * data["employed percent"]
                return math.ceil(adt)
            else:
                return random.randint(0, adults_num)

        def get_household_by_1(adults_num, childs_num, employed_num):
            household = {
                "total pep": [1] * people_per_household,
                "adt_list": [1] * adults_num,
                "chd_list": [1] * childs_num,
                "emp_list": [1] * employed_num
            }
            return household

        def get_work_travels(household_by_1):
            emp_list = household_by_1["emp_list"]
            work_travel_res = {
                "work by car": [],
                "work by public trans": [],
                "work by 2 wheeled vehicle": [],
                "work by bicycle": [],
                "work by foot": [],
                "work by other": []
            }
            for j in emp_list:
                rand_work_travel = np.random.random_sample()
                if rand_work_travel < data["travel to work by car"]:
                    work_travel_res["work by car"].append(1)
                elif data["travel to work by car"] < rand_work_travel < data["travel to work by public trans"]:
                    work_travel_res["work by public trans"].append(1)
                elif data["travel to work by public trans"] < rand_work_travel < data["travel to work by 2 wheeled vehicle"]:
                    work_travel_res["work by 2 wheeled vehicle"].append(1)
                elif data["travel to work by 2 wheeled vehicle"] < rand_work_travel < data["travel to work by bicycle"]:
                    work_travel_res["work by bicycle"].append(1)
                elif data["travel to work by bicycle"] < rand_work_travel < data["travel to work by foot"]:
                    work_travel_res["work by foot"].append(1)
                else:
                    work_travel_res["work by other"].append(1)
            return work_travel_res

        def get_leisure_travels(household_by_1):
            pep_list = household_by_1["total pep"]
            leisure_travel_res = {
                "leisure by car": [],
                "leisure by public trans": [],
                "leisure by 2 wheeled vehicle": [],
                "leisure by bicycle": [],
                "leisure by foot": [],
                "leisure by other": []
            }
            for j in pep_list:
                rand_leisure_travel = np.random.random_sample()
                if rand_leisure_travel < data["travel to work by car"]:
                    leisure_travel_res["leisure by car"].append(1)
                elif data["travel to work by car"] < rand_leisure_travel < data["travel to work by public trans"]:
                    leisure_travel_res["leisure by public trans"].append(1)
                elif data["travel to work by public trans"] < rand_leisure_travel < data["travel to work by 2 wheeled vehicle"]:
                    leisure_travel_res["leisure by 2 wheeled vehicle"].append(1)
                elif data["travel to work by 2 wheeled vehicle"] < rand_leisure_travel < data["travel to work by bicycle"]:
                    leisure_travel_res["leisure by bicycle"].append(1)
                elif data["travel to work by bicycle"] < rand_leisure_travel < data["travel to work by foot"]:
                    leisure_travel_res["leisure by foot"].append(1)
                else:
                    leisure_travel_res["leisure by other"].append(1)
            return leisure_travel_res


        res = {}
        id_num = str(i) + "Ganei_Sharona"
        people_per_household = get_people_num()
        is_married = get_is_married_rand(people_per_household)
        bin_marries = get_is_married_bin(is_married)
        childs_rand = get_rand_child(people_per_household)
        childs_num = get_childs_num(childs_rand, people_per_household)
        adults_num = get_adults_num(childs_num, people_per_household)
        rand_emp_value = get_rand_employed()
        employed_num = get_employed_num(adults_num, rand_emp_value)
        household_by_1 = get_household_by_1(adults_num, childs_num, employed_num)
        work_travel_data = get_work_travels(household_by_1)
        leisure_travel_data = get_leisure_travels(household_by_1)
        res["Id"] = id_num
        res["pep per house"] = people_per_household
        res["rand chd"] = childs_rand
        res["chd num"] = childs_num
        res["married rand"] = is_married
        res["married"] = bin_marries
        res["adults_num"] = adults_num
        res["emp_rand"] = rand_emp_value
        res["employed"] = employed_num
        res["bin house"] = household_by_1
        res["work by car list"] = work_travel_data["work by public trans"]
        res["work by car"] = len(work_travel_data["work by public trans"]) * 2
        res["work by public trans list"] = work_travel_data["work by car"]
        res["work by public trans"] = len(work_travel_data["work by car"]) *2
        res["work by 2 wheeled vehicle list"] = work_travel_data["work by 2 wheeled vehicle"]
        res["work by 2 wheeled vehicle"] = len(work_travel_data["work by 2 wheeled vehicle"]) * 2
        res["work by bicycle list"] = work_travel_data["work by bicycle"]
        res["work by bicycle"] = len(work_travel_data["work by bicycle"]) * 2
        res["work by foot list"] = work_travel_data["work by foot"]
        res["work by foot"] = len(work_travel_data["work by foot"]) * 2
        res["work by other list"] = work_travel_data["work by other"]
        res["work by other"] = len(work_travel_data["work by other"]) * 2
        res["total work travel"] = (res["work by car"] + res["work by public trans"] + res["work by 2 wheeled vehicle"]
                                    + res["work by bicycle"] + res["work by foot"] + res["work by other"])
        res["leisure by car"] = len(leisure_travel_data["leisure by public trans"]) * 2
        res["leisure by public trans list"] = leisure_travel_data["leisure by car"]
        res["leisure by public trans"] = len(leisure_travel_data["leisure by car"]) *2
        res["leisure by 2 wheeled vehicle list"] = leisure_travel_data["leisure by 2 wheeled vehicle"]
        res["leisure by 2 wheeled vehicle"] = len(leisure_travel_data["leisure by 2 wheeled vehicle"]) *2
        res["leisure by bicycle list"] = leisure_travel_data["leisure by bicycle"]
        res["leisure by bicycle"] = len(leisure_travel_data["leisure by bicycle"]) *2
        res["leisure by foot list"] = leisure_travel_data["leisure by foot"]
        res["leisure by foot"] = len(leisure_travel_data["leisure by foot"]) *2
        res["leisure by other list"] = leisure_travel_data["leisure by other"]
        res["leisure by other"] = len(leisure_travel_data["leisure by other"]) *2
        res["total leisure travel"] = (res["leisure by car"] + res["leisure by public trans"]
                                       + res["leisure by 2 wheeled vehicle"] + res["leisure by bicycle"]
                                       + res["leisure by foot"] + res["leisure by other"])
        res["total travels"] = res["total leisure travel"] + res["total work travel"]
        data["result"].append(res)


def statistic(df1):
    married_count = df1['married'].value_counts() / data["iterations"] * 100
    people_per_house_count = df1['pep per house'].value_counts() / data["iterations"] * 100
    child_count = df1['chd num'].value_counts() / data["iterations"] * 100
    total_childs = df1['chd num'].value_counts()
    adult_count = df1['adults_num'].value_counts() / data["iterations"] * 100
    emp_count = df1['employed'].value_counts() / data["iterations"] * 100
    total_worker = df1['employed'].value_counts()
    total_pop = sum(df1['pep per house'])
    print("married:   ",married_count)
    print("people_per_house:    ", people_per_house_count)
    print("total chd:    ", total_childs)
    print("child:    ", child_count)
    print("adt num:   ", adult_count)
    print("emp:   ", emp_count)
    print("total emp:   ", total_worker)
    print("total pop:", total_pop)


def main():
    make_data()
    df1 = pd.DataFrame(data["result"])
    statistic(df1)
    print(df1)
    df1.to_excel('output.xlsx')


if __name__ == "__main__":
    main()










