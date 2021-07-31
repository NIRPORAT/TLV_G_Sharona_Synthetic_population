import random
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages


data = {
  "married_household / house 2+ people": 0.47,
  "family household": 0.38,  # not use
  "household with chd": 0.106,
  "household with 65+": 0.082,
  "household with 65+ with 1 person": 0.481,  # not use
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
  "2014_work_travels": [40, 19.2, 8.7, 2.6, 25.4, 4.1],
  "iterations": 880,
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

        def get_rand_child(bin_married, people_per_household):
            chd_rand1 = np.random.random_sample()
            if people_per_household > 2 and bin_married == 1:
                return chd_rand1
            else:
                return 100

        def get_childs_num(childs_rand, people_per_household):
            if childs_rand <= data["1 childs"] and people_per_household >= 2:
                return 1
            elif data["1 childs"] < childs_rand <= data["2 childs"] and people_per_household >= 3:
                return 2
            elif data["2 childs"] < childs_rand <= data["3 childs"] and people_per_household >= 4:
                return 3
            else:
                return None

        def get_adults_num(childs_num, people_per_household):
            pph = people_per_household
            cn = childs_num
            if childs_num is not None:
                return pph - cn
            else:
                return pph


        def get_rand_employed():
            rand_emp = np.random.random_sample()
            return rand_emp

        def get_employed_num(adults_num, rand_emp_value):
            if rand_emp_value > data["household with 65+"]:
                adt_emp = adults_num * data["employed percent"]
                return round(adt_emp)
            else:
                adt_emp = np.random.normal(0.5, 4)
                adt_emp_round = round(adt_emp)
                if 0 <= adt_emp_round <= adults_num:
                    return adt_emp_round
                else:
                    return 0

        def get_household_by_1(adults_num, childs_num, employed_num):
            if childs_num is not None:
                household = {
                    "total pep": [1] * people_per_household,
                    "adt_list": [1] * adults_num,
                    "chd_list": [1] * childs_num,
                    "emp_list": [1] * employed_num
                }
            else:
                household = {
                    "total pep": [1] * people_per_household,
                    "adt_list": [1] * adults_num,
                    "emp_list": [1] * employed_num
                }
            return household

        def get_car_num(adults_num):
            cars_n = np.random.normal(1.8, 1.2)
            car_round = round(cars_n)
            if car_round < 0 or car_round > adults_num:
                return get_car_num(adults_num)
            else:
                return car_round

        def get_work_travels(household_by_1, cars_num):
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
                if rand_work_travel <= data["travel to work by car"] and cars_num != 0:
                    work_travel_res["work by car"].append(1)
                elif data["travel to work by car"] < rand_work_travel <= data["travel to work by public trans"]:
                    work_travel_res["work by public trans"].append(1)
                elif data["travel to work by public trans"] < rand_work_travel <= data["travel to work by 2 wheeled vehicle"]:
                    work_travel_res["work by 2 wheeled vehicle"].append(1)
                elif data["travel to work by 2 wheeled vehicle"] < rand_work_travel <= data["travel to work by bicycle"]:
                    work_travel_res["work by bicycle"].append(1)
                elif data["travel to work by bicycle"] < rand_work_travel <= data["travel to work by foot"]:
                    work_travel_res["work by foot"].append(1)
                elif rand_work_travel >= data["travel to work by foot"]:
                    work_travel_res["work by other"].append(1)
                else:
                    if cars_num != 0:
                        work_travel_res["work by car"].append(1)
            return work_travel_res
        #
        # def get_leisure_travels(household_by_1):
        #     pep_list = household_by_1["total pep"]
        #     leisure_travel_res = {
        #         "leisure by car": [],
        #         "leisure by public trans": [],
        #         "leisure by 2 wheeled vehicle": [],
        #         "leisure by bicycle": [],
        #         "leisure by foot": [],
        #         "leisure by other": []
        #     }
        #     for j in pep_list:
        #         rand_leisure_travel = np.random.random_sample()
        #         if rand_leisure_travel < data["travel to work by car"]:
        #             leisure_travel_res["leisure by car"].append(1)
        #         elif data["travel to work by car"] < rand_leisure_travel < data["travel to work by public trans"]:
        #             leisure_travel_res["leisure by public trans"].append(1)
        #         elif data["travel to work by public trans"] < rand_leisure_travel < data["travel to work by 2 wheeled vehicle"]:
        #             leisure_travel_res["leisure by 2 wheeled vehicle"].append(1)
        #         elif data["travel to work by 2 wheeled vehicle"] < rand_leisure_travel < data["travel to work by bicycle"]:
        #             leisure_travel_res["leisure by bicycle"].append(1)
        #         elif data["travel to work by bicycle"] < rand_leisure_travel < data["travel to work by foot"]:
        #             leisure_travel_res["leisure by foot"].append(1)
        #         else:
        #             leisure_travel_res["leisure by other"].append(1)
        #     return leisure_travel_res



        def get_single_parents(childs_num, adults_num):
            if childs_num == 1 | 2 | 3 and adults_num == 1:
                return 1
            else:
                return 0

        def get_houses_without_adt(people_per_household, childs_num):
            if childs_num == 1 | 2 | 3:
                error = (people_per_household - childs_num <= 0)
                if error:
                    return error


        res = {}
        id_num = str(i) + "Ganei_Sharona 2021"
        people_per_household = get_people_num()
        is_married = get_is_married_rand(people_per_household)
        bin_married = get_is_married_bin(is_married)
        childs_rand = get_rand_child(bin_married, people_per_household)
        childs_num = get_childs_num(childs_rand, people_per_household)
        adults_num = get_adults_num(childs_num, people_per_household)
        rand_emp_value = get_rand_employed()
        employed_num = get_employed_num(adults_num, rand_emp_value)
        household_by_1 = get_household_by_1(adults_num, childs_num, employed_num)
        cars_num = get_car_num(adults_num)
        work_travel_data = get_work_travels(household_by_1, cars_num)
        # leisure_travel_data = get_leisure_travels(household_by_1)
        sing_par = get_single_parents(childs_num, adults_num)
        houses_without_adt = get_houses_without_adt(people_per_household, childs_num)
        res["Id"] = id_num
        res["pep per house"] = people_per_household
        res["rand chd"] = childs_rand
        res["chd num"] = childs_num
        res["married rand"] = is_married
        res["married"] = bin_married
        res["adults_num"] = adults_num
        res["emp_rand"] = rand_emp_value
        res["employed"] = employed_num
        res["cars#"] = cars_num
        res["bin house"] = household_by_1
        res["work by car list"] = work_travel_data["work by car"]
        res["work by car"] = len(work_travel_data["work by car"])
        res["work by public trans list"] = work_travel_data["work by public trans"]
        res["work by public trans"] = len(work_travel_data["work by public trans"])
        res["work by 2 wheeled vehicle list"] = work_travel_data["work by 2 wheeled vehicle"]
        res["work by 2 wheeled vehicle"] = len(work_travel_data["work by 2 wheeled vehicle"])
        res["work by bicycle list"] = work_travel_data["work by bicycle"]
        res["work by bicycle"] = len(work_travel_data["work by bicycle"])
        res["work by foot list"] = work_travel_data["work by foot"]
        res["work by foot"] = len(work_travel_data["work by foot"])
        res["work by other list"] = work_travel_data["work by other"]
        res["work by other"] = len(work_travel_data["work by other"])
        res["total work travel"] = (res["work by car"] + res["work by public trans"] + res["work by 2 wheeled vehicle"]
                                    + res["work by bicycle"] + res["work by foot"] + res["work by other"])
        # res["leisure by car"] = len(leisure_travel_data["leisure by public trans"]) * 2
        # res["leisure by public trans list"] = leisure_travel_data["leisure by car"]
        # res["leisure by public trans"] = len(leisure_travel_data["leisure by car"]) *2
        # res["leisure by 2 wheeled vehicle list"] = leisure_travel_data["leisure by 2 wheeled vehicle"]
        # res["leisure by 2 wheeled vehicle"] = len(leisure_travel_data["leisure by 2 wheeled vehicle"]) *2
        # res["leisure by bicycle list"] = leisure_travel_data["leisure by bicycle"]
        # res["leisure by bicycle"] = len(leisure_travel_data["leisure by bicycle"]) *2
        # res["leisure by foot list"] = leisure_travel_data["leisure by foot"]
        # res["leisure by foot"] = len(leisure_travel_data["leisure by foot"]) *2
        # res["leisure by other list"] = leisure_travel_data["leisure by other"]
        # res["leisure by other"] = len(leisure_travel_data["leisure by other"]) *2
        # res["total leisure travel"] = (res["leisure by car"] + res["leisure by public trans"]
        #                                + res["leisure by 2 wheeled vehicle"] + res["leisure by bicycle"]
        #                                + res["leisure by foot"] + res["leisure by other"])
        # res["total travels"] = res["total leisure travel"] + res["total work travel"]
        res["single parents"] = sing_par
        res["house_without_adt"] = houses_without_adt
        data["result"].append(res)


def statistic(df1):
    def chd_stat():
        chd_no_zero = {
            '1 chd: ': (df1['chd num'] == 1).sum(),
            '2 chd: ': (df1['chd num'] == 2).sum(),
            '3 chd: ': (df1['chd num'] == 3).sum(),
            'None chd: ': df1['chd num'].isnull().sum()
        }
        df_chd = pd.DataFrame(chd_no_zero, index=[0])

        print(df_chd)

    chd_stat()
    with PdfPages('G_Sharona_visual.pdf') as pdf:
        fig = plt.figure(figsize=(10, 10))
        plt.rcParams.update({'font.size': 10})
        gs = fig.add_gridspec(2, 1)
        married_count = round((df1['married'].value_counts().sort_index() / data["iterations"] * 100), 2)
        married_df = pd.DataFrame({'2014': [53, 47], '2021': married_count})
        ax1 = fig.add_subplot(gs[0])
        married_bar = married_df.plot(kind='bar', rot=0, ax=ax1, title='Married % (1=Married)',)
        for p in married_bar.patches:
            married_bar.annotate(str(p.get_height()), (p.get_x() * 1.01, p.get_height() * 1.01))

        people_per_house = round((df1["pep per house"].value_counts().sort_index() / data["iterations"] * 100), 2)
        pph_df = pd.DataFrame({'2014': [52.6, 29.1, 6.3, 8.2, 3.8], '2021': people_per_house})
        ax2 = fig.add_subplot(gs[1])
        pph_bar = pph_df.plot(kind='bar', rot=0, ax=ax2, title='People per household')
        for p1 in pph_bar.patches:
            pph_bar.annotate(str(p1.get_height()), (p1.get_x() * 1.01, p1.get_height() * 1.01))

        pdf.savefig(fig)
        plt.close()

        fig = plt.figure(figsize=(10, 10))
        plt.rcParams.update({'font.size': 10})
        gs = fig.add_gridspec(2, 1)
        children_count = round(df1['chd num'].value_counts(normalize=True).sort_index() * 100, 2)
        chd_df = pd.DataFrame({'2014': [47.6, 34.3, 18.1], '2021': children_count}, index=[1, 2, 3])
        ax3 = fig.add_subplot(gs[0])
        chd_bar = chd_df.plot(kind='bar', rot=0, ax=ax3, title='Children per household (from households with children)')
        for p2 in chd_bar.patches:
            chd_bar.annotate(str(p2.get_height()), (p2.get_x() * 1.01, p2.get_height() * 1.01))
        print(chd_df)
        adult_count = (df1['adults_num'].value_counts() / data["iterations"] * 100)
        emp_count = round((df1['employed'].value_counts().sort_index() / data["iterations"] * 100), 2)
        ax4 = fig.add_subplot(gs[1])
        emp_bar = emp_count.plot(kind='bar', rot=0, ax=ax4, title='employed per households')
        for p3 in emp_bar.patches:
            emp_bar.annotate(str(p3.get_height()), (p3.get_x() * 1.01, p3.get_height() * 1.01))
        total_worker = df1['employed'].value_counts()
        total_pop = sum(df1['pep per house'])
        single_p = df1["single parents"].value_counts()

        pdf.savefig(fig)
        plt.close()

        fig = plt.figure(figsize=(10, 10))
        plt.rcParams.update({'font.size': 10})
        gs = fig.add_gridspec(2, 1)
        cars_mean = round((df1["cars#"].mean()), 2)
        cars_p = round((df1["cars#"].value_counts().sort_index() / data["iterations"] * 100), 2)
        ax5 = fig.add_subplot(gs[0])
        print('cars per house:', cars_p)
        car_bar = cars_p.plot(kind='bar', rot=0, ax=ax5, title=('cars per households (mean = ' + str(cars_mean) + ')'))
        for p4 in car_bar.patches:
            car_bar.annotate(str(p4.get_height()), (p4.get_x() * 1.01, p4.get_height() * 1.01))

        work_travel_list = {"Car": (df1["work by car"].sum() / df1["total work travel"].sum() * 100),
                            'Public trans': (df1["work by public trans"].sum() / df1["total work travel"].sum() * 100),
                            "2 wheeled vehicle": (df1["work by 2 wheeled vehicle"].sum() / df1["total work travel"].sum() * 100),
                            "Bicycle": (df1["work by bicycle"].sum() / df1["total work travel"].sum() * 100),
                            "Foot": (df1["work by foot"].sum() / df1["total work travel"].sum() * 100),
                            "Other": (df1["work by other"].sum() / df1["total work travel"].sum() * 100)}
        print('work_travel_list:', work_travel_list)
        work_travel_df = round((pd.DataFrame.from_dict(work_travel_list, orient='index', columns=['2021'])), 2)
        work_travel_df['2014'] = data["2014_work_travels"]
        print(work_travel_df)
        ax6 = fig.add_subplot(gs[1])
        work_travel_bar = work_travel_df.plot(kind='bar', rot=0, ax=ax6, title='Commuting to work')
        for p5 in work_travel_bar.patches:
            work_travel_bar.annotate(str(p5.get_height()), (p5.get_x() * 1.01, p5.get_height() * 1.01))


        plt.show()
        plt.draw()
        pdf.savefig(fig)
        plt.close()

    print("work travels method", work_travel_df)
    car_count = df1["cars#"].value_counts()
    print("married:   ", married_count)
    print("people_per_house:    ", people_per_house)
    print("children:", )
    print("adt num:   ", adult_count)
    print("emp:" , total_worker)
    print("emp by %:   ", emp_count)
    print("total emp:   ", df1['employed'].sum())
    print("total pop:", total_pop)
    print("single parents:   ", single_p)
    print('cars %: ', cars_p)
    print("car count: ", car_count)
    print('cars mean:  ', cars_mean)
    print('total_work_travel', df1["total work travel"].sum())




def main():
    make_data()
    df1 = pd.DataFrame(data["result"])
    statistic(df1)
    print(df1)
    df1.to_excel('G_Sharona 2021.xlsx')
    # plt.show()






if __name__ == "__main__":
    main()










