##############################################################################
# Authors: Sandhya Saisubramanian, Sainyam Galhotra
# Description: Function related to pattern mining for interpretable clustering.
#############################################################################

import numpy as np
import pyfpgrowth
import networkx as nx


def frequent_pattern_mining(members,Features):
    # find patterns that occur at least min_support times.
    min_support = 0.2*len(members)
    patterns = pyfpgrowth.find_frequent_patterns(members, min_support)
    print("# Patterns:",len(patterns))
    display_patterns= []
    for p in patterns:
        p_index =  int(p[0])-1
        display_patterns.append(Features[p_index])
    print("Patterns:",display_patterns)

    #counting the feature occurence in each cluster
def calculate_composition(G,k,aff_array,domain):
    attr = nx.get_node_attributes(G,'attributes')
    if domain == "sanitation":
        pit_latrines_percentage  = ['<25','25-50','50-75','>75']
        for cluster in range(k):
            members = [] #collects attributes of each cluster's members.
            total_nodes_incluster = 0
            districts_pit_latrine = np.zeros((len(pit_latrines_percentage)))
            for node in G.nodes():
                aff = aff_array[node]
                if aff == cluster:
                    attributes = attr[node]
                    temp_attributes = '0'
                    total_nodes_incluster += 1
                    if(float(attributes[4]) < 25):
                        districts_pit_latrine[0] += 1
                        temp_attributes = "1"
                    if(float(attributes[4]) >= 25 and float(attributes[4]) < 50):
                        districts_pit_latrine[1] += 1
                        temp_attributes = "2"
                    if(float(attributes[4]) >= 50 and float(attributes[4]) <= 75):
                        districts_pit_latrine[2] += 1
                        temp_attributes = "3"
                    if(float(attributes[4]) > 75):
                        districts_pit_latrine[3] += 1
                        temp_attributes = "4"
                    members.append(temp_attributes)
            print("**********************")
            print("Number of nodes (districts) with %pit latrines:",(districts_pit_latrine/total_nodes_incluster))
            frequent_pattern_mining(members,pit_latrines_percentage)

    elif domain == "adult":
         age_pay = ['age <= 40 and pay <= 50K', 'age <= 40 and pay >50K','age >40 and pay <=50K', 'age >40 and pay >50K']
         gender_hours = ['Male and <=40','Male and >40','Female and <=40','Female and >40']
         for cluster in range(k):
            total_nodes_incluster = 0
            members = [] #collects attributes of each cluster's members.
            age_pay_count =  np.zeros((len(age_pay)))
            gender_hours_count = np.zeros((len(gender_hours)))
            for node in G.nodes():
                aff  = aff_array[node]
                if(aff == cluster):
                    total_nodes_incluster += 1
                    attributes = attr[node]
                    if(float(attributes[0]) <= 40 and float(attributes[14]) == 50):
                        age_pay_count[0] +=1
                        members.append('1')
                    elif (float(attributes[0]) <= 40 and float(attributes[14]) == 100):
                        age_pay_count[1] +=1
                        members.append('2')
                    elif (float(attributes[0]) >40 and float(attributes[14]) == 50):
                        age_pay_count[2] +=1
                        members.append('3')
                    elif (float(attributes[0]) >40 and float(attributes[14]) == 100):
                        age_pay_count[3] +=1
                        members.append('4')
            print("*********************************************")
            print("age pay distribution in cluster = ", (age_pay_count/total_nodes_incluster))
            frequent_pattern_mining(members,age_pay)
    elif domain == "crime":
        ViolentCrimesPerPop = ['<0.25','0.25-0.5','0.5-0.75','0.75-1']
        for cluster in range(k):
            total_nodes_incluster = 0
            members = []
            community_crime = np.zeros((len(ViolentCrimesPerPop)))
            for node in G.nodes():
                aff = aff_array[node]
                if aff == cluster:
                    attributes = attr[node]
                    attribute_id = len(attributes)-1
                    total_nodes_incluster += 1
                    if(float(attributes[len(attributes)-1]) <= 0.25):
                        community_crime[0] += 1
                        members.append('1')
                    elif(float(attributes[len(attributes)-1]) > 0.25 and float(attributes[len(attributes)-1]) <= 0.5):
                        community_crime[1] += 1
                        members.append('2')
                    elif(float(attributes[len(attributes)-1]) > 0.5 and float(attributes[len(attributes)-1]) <= 0.75):
                        community_crime[2] += 1
                        members.append('3')
                    else:
                        community_crime[3] += 1
                        members.append('4')
            print("**********************")
            print("ViolentCrimesPerPopulation:",ViolentCrimesPerPop)
            print("Number of nodes (districts) with avg crime rate:",(community_crime/total_nodes_incluster))
            frequent_pattern_mining(members,ViolentCrimesPerPop)

    # elif domain == "crime":
    #     # percent_under_poverty = ['<25','25-50','50-75','>75']
    #     # ViolentCrimesPerPop = ['<0.25','0.25-0.5','0.5-0.75','0.75-1']
    #     # PercentPersonDenseHousing = ['<0.25','0.25-0.5','0.5-0.75','0.75-1']
    #     MedianIncome = ['<0.25','0.25-0.5','0.5-0.75','0.75-1']
    #     for cluster in range(k):
    #         total_nodes_incluster = 0
    #         members = []
    #         income_count  = np.zeros((len(MedianIncome)))
    #     #     community_crime = np.zeros((len(ViolentCrimesPerPop)))
    #     #     dense_housing = np.zeros((len(PercentPersonDenseHousing)))
    #         for node in G.nodes():
    #             aff = aff_array[node]
    #             if aff == cluster:
    #                 attributes = attr[node]
    #                 total_nodes_incluster += 1
    #                 if(float(attributes[16]) <= .25):
    #                     income_count[0] += 1
    #                     members.append('1')
    #                 elif (float(attributes[16]) > .25 and float(attributes[16]) <= .50):
    #                     income_count[1] += 1
    #                     members.append('2')
    #                 elif (float(attributes[16]) > .50 and float(attributes[16]) <=.75):
    #                     income_count[2] += 1
    #                     members.append('3')
    #                 else:
    #                     income_count[3] += 1
    #                     members.append('4')
    #     #                 community_crime[0] += 1
    #     #             if(float(attributes[len(attributes)-1]) >= 0.25 and float(attributes[len(attributes)-1]) < 0.5):
    #     #                 community_crime[1] += 1
    #     #             if(float(attributes[len(attributes)-1]) >= 0.5 and float(attributes[len(attributes)-1]) <= 0.75):
    #     #                 community_crime[2] += 1
    #     #             if(float(attributes[len(attributes)-1]) > 0.75):
    #     #                 community_crime[3] += 1

    #     #             if(float(attributes[len(attributes)-1]) <0.25):
    #     #                 community_crime[0] += 1
    #     #             if(float(attributes[len(attributes)-1]) >= 0.25 and float(attributes[len(attributes)-1]) < 0.5):
    #     #                 community_crime[1] += 1
    #     #             if(float(attributes[len(attributes)-1]) >= 0.5 and float(attributes[len(attributes)-1]) <= 0.75):
    #     #                 community_crime[2] += 1
    #     #             if(float(attributes[len(attributes)-1]) > 0.75):
    #     #                 community_crime[3] += 1
    #     #             #   Percent population in dense housing. (many ppl in small house)
    #     #
    #     #             if(float(attributes[74]) <0.25):
    #     #                 dense_housing[0] += 1
    #     #             if(float(attributes[74]) >= 0.25 and float(attributes[74]) < 0.5):
    #     #                 dense_housing[1] += 1
    #     #             if(float(attributes[74]) >= 0.5 and float(attributes[74]) <= 0.75):
    #     #                 dense_housing[2] += 1
    #     #             if(float(attributes[74]) > 0.75):
    #     #                 dense_housing[3] += 1
    #         print("**********************")
    #     #     print("ViolentCrimesPerPopulation:",ViolentCrimesPerPop)
    #     #     print("Number of nodes (districts) with avg crime rate:",(community_crime/total_nodes_incluster))
    #     #     print("dense_housing percentage:",(dense_housing/total_nodes_incluster))
    #         print("MedianIncome", MedianIncome)
    #         print("Median family income distribution cluster = ", (income_count/total_nodes_incluster))
    #         frequent_pattern_mining(members,MedianIncome)

    elif domain == "accident":
        Accident_type = ['Pedestrian hit','Vehicle collision','Death','Others']
        for cluster in range(k):
            total_nodes_incluster = 0
            members = []
            accident_count  = np.zeros((len(Accident_type)))
            for node in G.nodes():
                aff = aff_array[node]
                if aff == cluster:
                    attributes = attr[node]
                    total_nodes_incluster += 1
                    if('pedestrian' in attributes[10].lower() or "pedestrians" in attributes[10].lower()\
                       or "cyclist" in attributes[10].lower() or "fell from" in attributes[10].lower()):
                        accident_count[0] += 1
                        members.append('1')
                    elif ('collided' in attributes[10].lower() or 'collision' in attributes[10].lower() \
                                  or "rammed" in attributes[10].lower() or "crash" in attributes[10].lower() \
                          or "knocked" in attributes[10].lower() or "hit from the rear" in attributes[10].lower()\
                          or "ramming" in attributes[10].lower()):
                        accident_count[1] += 1
                        members.append('2')
                    elif ('body' in attributes[10].lower() or 'bodies' in attributes[10].lower()\
                          or "killed" in attributes[10].lower()):
                        accident_count[2] += 1
                        members.append('3')
                    else:
                        accident_count[3] += 1
                        members.append('4')

            print("**********************")
            print("Accident_type", Accident_type)
            print("Accident type distribution in cluster = ", (accident_count/total_nodes_incluster))
            frequent_pattern_mining(members,Accident_type)



    # person_room  = ['0-1','1-1.5','1.5-2','>2']
    # for cluster in range(k):
    #     total_nodes_incluster = 0
    #     districts_person_room = np.zeros((len(person_room)))
    #     for node in G.nodes():
    #         aff = kc.getAffiliation(node)
    #         if aff == cluster:
    #             attributes = attr[node]
    #             total_nodes_incluster += 1
    #             if(float(attributes[6]) < 1):
    #                 districts_person_room[0] += 1
    #             if(float(attributes[6]) >= 1 and float(attributes[6]) < 1.5):
    #                 districts_person_room[1] += 1
    #             if(float(attributes[6]) >= 1.5 and float(attributes[6]) <= 2):
    #                 districts_person_room[2] += 1
    #             if(float(attributes[6]) > 2):
    #                 districts_person_room[3] += 1
    #     print("**********************")
    #     print("Average person per room:",person_room)
    #     print("Number of nodes (districts) with avg person per room:",(districts_person_room/total_nodes_incluster))
