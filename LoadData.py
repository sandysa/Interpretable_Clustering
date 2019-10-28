##############################################################################
# Authors: Sandhya Saisubramanian, Sainyam Galhotra
# Description: Reads datasets and returns a graph.
#############################################################################
import numpy as np
import networkx as nx

class LoadData:
    def __init__(self, domain):
        self.domain = domain

    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False


    def loadPokecData(self):
        filename = "../Dataset/Pokec/processed-pokec-profiles10K.txt"
        G = nx.Graph()
        attributes = {}
        index = -1
        with open(filename,encoding="utf8") as myfile:
            for line in myfile:
                temp = line.split("\t")
                index += 1
                u_features = []
                #Attributes considered: age, location, last_login (datetime), registration (datetime), age
                for i in range(3, 8):
                    u_features.append(temp[i])
                if(index < 10000):
                    G.add_node(index)
                    attributes[index] = u_features
        nx.set_node_attributes(G, attributes, 'attributes')
        myfile.close()

        print("processing edge:")
        edge_file = "../Dataset/Pokec/processed-pokec-relationships10K.txt"
        with open(edge_file,encoding="utf8") as myfile:
            for line in myfile:
                temp = line.split("\t")
                # Because the user id starts at 1.
                u = int(temp[0])-1
                v = int(temp[1])-1
                distance = 0
                if(u <10000 and v <10000):
                    for i in range(len(attributes[u])):
                        if(attributes[u][i] == attributes[v][i]):
                            distance += 1
                    distance = distance/(len(attributes))
                    G.add_edge(u,v, weight=(1-distance))
        myfile.close()
        return G,attributes

    def loaddblpData(self):
        filename = "../Dataset/dblp/CORE.csv"
        G = nx.Graph()
        attributes = {}
        index = -1
        with open(filename) as myfile:
            for line in myfile:
                meta_val = line.split("\n")
                temp = meta_val[0].split(",")
                if(len(temp[6]) == 0):
                    continue
                index += 1
                u_features = []
                for x in range(0, 7):
                    u_features.append(temp[x].strip())
                if (index < 10000):
                    G.add_node(index)
                    attributes[index] = u_features
        nx.set_node_attributes(G, attributes, 'attributes')
        myfile.close()
        for u in G.nodes:
            for v in G.nodes:
                if(u != v):
                    distance = 0
                    for i in range(len(attributes)):
                        if(attributes[u] == attributes[v]):
                            distance += 1
                    distance = distance/(len(attributes))
                    G.add_edge(u,v,weight=1-distance)
        print("number of nodes = ", G.number_of_nodes())
        print("number of edges = ", G.number_of_edges())
        return G

    def loadAdultIncomeData(self):
        filename = "../Dataset/adultIncome/adult_data.txt"
        workclass =['Private','Self-emp-not-inc','Self-emp-inc','Federal-gov','Local-gov','State-gov','Without-pay','Never-worked']
        education = ['Bachelors','Some-college','11th','HS-grad','Prof-school','Assoc-acdm','Assoc-voc','9th','7th-8th','12th',
                     'Masters', '1st-4th', '10th', 'Doctorate', '5th-6th','Preschool']
        marital_status =['Married-civ-spouse','Divorced','Never-married', 'Separated','Widowed','Married-spouse-absent','Married-AF-spouse']
        occupation=['Tech-support','Craft-repair', 'Other-service','Sales','Exec-managerial','Prof-specialty','Handlers-cleaners',
                    'Machine-op-inspct','Adm-clerical', 'Farming-fishing','Transport-moving', 'Priv-house-serv', 'Protective-serv','Armed-Forces']
        relationship = ['Wife', 'Own-child','Husband','Not-in-family', 'Other-relative', 'Unmarried']
        race=['White','Asian-Pac-Islander','Amer-Indian-Eskimo','Other','Black']
        sex=['Female','Male']
        country = ['United-States', 'Cambodia', 'England','Puerto-Rico','Canada','Germany','Outlying-US(Guam-USVI-etc)',
                   'India', 'Japan', 'Greece', 'South', 'China', 'Cuba', 'Iran', 'Honduras', 'Philippines', 'Italy',
                   'Poland','Jamaica', 'Vietnam', 'Mexico', 'Portugal', 'Ireland','France', 'Dominican-Republic', 'Laos',
                   'Ecuador', 'Taiwan', 'Haiti', 'Columbia', 'Hungary', 'Guatemala', 'Nicaragua', 'Scotland', 'Thailand',
                   'Yugoslavia', 'El-Salvador', 'Trinadad&Tobago','Peru', 'Hong', 'Holand-Netherlands']
        G = nx.Graph()
        attributes = {}
        index = -1
        with open(filename) as myfile:
            for line in myfile:
                if any(s in line for s in "?"):
                    continue
                index += 1
                if(index > 1200):
                    break
                # change pay: <=50k -> 50 and >50k ->100
                line = line.replace("<=50K","50")
                line = line.replace(">50K","100")
                meta_val = line.split("\n")
                temp = meta_val[0].split(",")
                u_features = []
                u_features.append(float(temp[0].strip()))
                u_features.append(workclass.index(temp[1].strip()))
                u_features.append(float(temp[2].strip()))
                u_features.append(education.index(temp[3].strip()))
                u_features.append(float(temp[4].strip()))
                u_features.append(marital_status.index(temp[5].strip()))
                u_features.append(occupation.index(temp[6].strip()))
                u_features.append(relationship.index(temp[7].strip()))
                u_features.append(race.index(temp[8].strip()))
                u_features.append(sex.index((temp[9].strip())))
                u_features.append(float(temp[10].strip()))
                u_features.append(float(temp[11].strip()))
                u_features.append(float(temp[12].strip()))
                u_features.append(country.index(temp[13].strip()))
                u_features.append(float(temp[14].strip()))

                # for x in range(0, len(temp)):
                #     u_features.append(temp[x].strip())
                if (index < 10000):
                    G.add_node(index)
                    attributes[index] = u_features
        nx.set_node_attributes(G, attributes, 'attributes')
        myfile.close()
        print("number of nodes = ", G.number_of_nodes())
        return G

    def loadAccidentData(self):
        filename = "../Dataset/Kenya/2011_Traffic_Incidences_From_Desinventar.csv"
        G = nx.Graph()
        attributes = {}
        index = -1
        with open(filename) as myfile:
            for line in myfile:
                # Skipping header
                if("Serial" in line):
                    continue
                if("matatu" in line.lower() or "buchenge" in line.lower()):
                    continue
                temp = line.split(",")
                # If no accident description, continue
                if(temp[10] == ""):
                    continue
                index += 1
                u_features = []
                for x in range(0, len(temp)):
                    val = temp[x].strip()
                    if("%" in val):
                        val = val.replace("%","")
                    u_features.append(val)
                G.add_node(index)
                attributes[index] = u_features
        nx.set_node_attributes(G, attributes, 'attributes')
        myfile.close()
        print("number of nodes = ", G.number_of_nodes())
        return G



    def loadSanitationData(self):
        filename = "../Dataset/Kenya/Sanitation_by_District.csv"
        G = nx.Graph()
        attributes = {}
        index = -1
        with open(filename) as myfile:
            for line in myfile:
                # Skipping header
                if("District" in line):
                    continue
                if any(s in line for s in "?"):
                    continue
                line = line.replace("Environment, Water and Sanitation","Environment")
                line = line.replace("%","")
                temp = line.split(",")
                if(temp[2] == ""):
                    continue
                index += 1
                u_features = []
                # Ignore district name (temp[0]) since lat long values provide better distance metric.
                # Ignore last col (object id)
                # Ignore random table references - 21,22,23
                for x in range(0, len(temp)-1):
                    if(x in [21,22,23]):
                        continue
                    val = temp[x].strip()
                    if(self.is_number(val)):
                        u_features.append(float(temp[x].strip()))
                G.add_node(index)
                attributes[index] = u_features
        nx.set_node_attributes(G, attributes, 'attributes')
        myfile.close()
        print("number of nodes = ", G.number_of_nodes())
        return G

    def loadHouseholdData(self):
        filename = "../Dataset/Kenya/Households_by_Number_of_Dwelling_Units_and_County_2009.csv"
        G = nx.Graph()
        attributes = {}
        index = -1
        with open(filename) as myfile:
            for line in myfile:
                # Skipping header
                if("County" in line):
                    continue
                if any(s in line for s in "?"):
                    continue
                if(index > 1000):
                    break
                temp = line.split(",")
                index += 1
                u_features = []
                # Ignore district name and Urban/Rural, location
                for x in range(2, len(temp)-3):
                    u_features.append(float(temp[x]))
                G.add_node(index)
                attributes[index] = u_features
        nx.set_node_attributes(G, attributes, 'attributes')
        myfile.close()
        print("number of nodes = ", G.number_of_nodes())
        return G

    def loadCrimeData(self):
        filename = "../Dataset/Crime/communities_data.txt"
        G = nx.Graph()
        attributes = {}
        index = -1
        with open(filename) as myfile:
            for line in myfile:
                line =  line.replace("?","0")
                temp = line.split(",")
                # Crime value missing
                if(temp[len(temp)-1] == "?"):
                    continue
                index += 1
                u_features = []
                # Ignore string data
                for x in range(0, len(temp)):
                    val = temp[x].strip()
                    if(self.is_number(val)):
                        u_features.append(float(temp[x].strip()))
                G.add_node(index)
                attributes[index] = u_features
        nx.set_node_attributes(G, attributes, 'attributes')
        myfile.close()
        print("number of nodes = ", G.number_of_nodes())
        return G


    def readFile(self):
        if(self.domain == "pokec"):
            return  self.loadPokecData()
        elif self.domain == "dblp":
            return  self.loaddblpData()
        elif self.domain == "adult":
            return  self.loadAdultIncomeData()
        elif self.domain == "sanitation":
           return  self.loadSanitationData()
        elif self.domain == "household":
            return self.loadHouseholdData()
        elif self.domain == "crime":
            return self.loadCrimeData()
        elif self.domain == "accident":
            return self.loadAccidentData()





