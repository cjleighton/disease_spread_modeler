import numpy as np
import random
import matplotlib.pyplot as plt

# we're going to have to iterate through citizens in each city during infection
# for each city, maintain a list of indices in citizens[] from that city
citizens=np.array([])

class citizen():
    def __init__(self,infected,hometown,contacts):
        self.infected=infected # are they infected?
        self.infected_days=0 # how long has someone been infected
        self.infected_in_past=False # if someone's already been infected, they can't contract the disease again
        self.hometown=hometown # what's their hometown as a string?
        self.curr_city=hometown # set everyone in their hometown initially
        self.days_away=0 # if citizen leaves hometown, count how long they're away so we can send them back
        self.contacts=contacts # in hometown, what indices in citizens[] from their hometown do they see each day?

class city():
    def __init__(self,name,population,contact_size,adj_cities):
        print("Generating",name+"...")
        global citizens # access to citizens[]
        self.name=name # city name
        self.adj_cities=adj_cities
        self.population=np.array([]) # indices in citizens[] indicating people from current city
        self.citizens_begin=len(citizens) # marks where in citizens[] people for city begins
        self.citizens_end=len(citizens)+population-1
        for i in range(0,population):
            # establish contact list. pick from citizens from current city
            # only from citizens from hometown
            # when we create the city, mark current len(citizens)
            # and what the length will be after city is created
            # use this to get random indices
            contacts=np.array([])
            while len(contacts)<contact_size:
                r=random.randint(self.citizens_begin,self.citizens_end)
                if (r not in contacts) and (r!=i):
                    contacts=np.append(contacts,r)
            # create citizen
            new_citizen = citizen(False,name,contacts)
            citizens=np.append(citizens,new_citizen)
            self.population=np.append(self.population,len(citizens)-1)
################################################################################
# when we create a city, we want:
#   -there to be an existing list of citizens
#   -call to class to create new citizens and add to existing global list
contact_size = 6 # how many people encounter each day in their hometown
random_interact = 8 # how many people someone randomly interacts with no matter what city they're in
days_away_max = 5 # how many days someone can be in a non-hometown before returning to hometown
infected_days_max = 14 # if someone's been infected for this many days, they recover
people_in_transit = 0 # number of people from each city who travel to a neighboring city
infect_prob = 0.1 # probability of an infection for each encounter
partial_immunity_factor = 1 # after someone's been infected

Denver=city("Denver",3000,contact_size,["Salt Lake City","Albuquerque","Cheyenne"])
Salt_Lake=city("Salt Lake City",1000,contact_size,["Denver","Cheyenne","Phoenix"])
Albuquerque=city("Albuquerque",2500,contact_size,["Denver","Phonix"])
Phoenix=city("Phoenix",5000,contact_size,["Salt Lake City","Albuquerque"])
Cheyenne=city("Cheyenne",300,contact_size,["Denver","Salt Lake City"])
cities=[Denver,Salt_Lake,Albuquerque,Phoenix,Cheyenne] # leave this as non-numpy array
citizens[0].infected=True # someone in denver gets infected first

infected_people_den=np.array([])
infected_people_SL=np.array([])
infected_people_ph=np.array([])
infected_people_al=np.array([])
infected_people_ch=np.array([])
day_arr=np.array([])

for day in range(0,250): # time iterator
    for city_index in range(0,len(cities)): # consider all cities
        for i in range(cities[city_index].citizens_begin,cities[city_index].citizens_end): # consider all citizens in each city
            if citizens[i].infected==True: # citizen is infected

                # infect people on citizen i's contact list
                if citizens[i].curr_city==citizens[i].hometown: # ...if they're in hometown
                    for j in range(0,len(citizens[i].contacts)): # iterate through their contacts
                        # check whether contact j is already infected
                        curr_contact=int(citizens[i].contacts[j])
                        #print("contact:",curr_contact,"infected:",citizens[curr_contact].infected)
                        if (citizens[curr_contact].infected==False) and (citizens[curr_contact].curr_city==citizens[i].curr_city): # can be infected
                            '''if citizens[curr_contact].infected_in_past==False:
                                infect_prob_factor = 1
                            else:
                                infect_prob_factor = partial_immunity_factor'''
                            infect_prob_factor = 1
                            if (random.randrange(100)<infect_prob_factor*infect_prob*100)==True:
                                citizens[curr_contact].infected=True # infect the contact

                # infect some random people in the city they're currently in
                for k in range(0,len(cities)): # we need start and end indices in citizens[] for current city
                    if cities[k].name==citizens[i].curr_city:
                        curr_city_citizens_begin = cities[k].citizens_begin
                        curr_city_citizens_end = cities[k].citizens_end
                for k in range(0,random_interact): # now iterate through some random people in curr_city and infect
                    rand_person = random.randint(curr_city_citizens_begin,curr_city_citizens_end)
                    if (citizens[rand_person].infected==False) and (citizens[rand_person].curr_city==citizens[i].curr_city): # can be infected
                        '''if citizens[curr_contact].infected_in_past==False:
                            infect_prob_factor = 1
                        else:
                            infect_prob_factor = partial_immunity_factor'''
                        infect_prob_factor = 1
                        if (random.randrange(100)<infect_prob_factor*infect_prob*100)==True:
                            citizens[rand_person].infected=True

            # we want to check if the citizen is away from their hometown and how long they've been away
            # if they've been away for n days (3?), send them back to their hometown
            if citizens[i].curr_city != citizens[i].hometown:
                citizens[i].days_away=citizens[i].days_away+1
                if citizens[i].days_away >= days_away_max:
                    citizens[i].curr_city = citizens[i].hometown
                    citizens[i].days_away = 0 # reset counter

            # if a citizen is infected, iterate their infection counter. if they've been infected for m days, they recover
            if citizens[i].infected==True:
                citizens[i].infected_days=citizens[i].infected_days+1
                if citizens[i].infected_days>=infected_days_max:
                    #if (random.randrange(100)<10)==True: # 10% chance of recovering after 14 days
                    citizens[i].infected=False
                    citizens[i].infected_in_past=True

        # now that we've iterated through citizens[] and done the day's infections, send n people in current city to random connecting city
        transit_indices_curr_city = np.random.randint(cities[city_index].citizens_begin,cities[city_index].citizens_end,people_in_transit)
        rand_adj_city_index = random.randint(0,len(cities[city_index].adj_cities)-1) # pick random index from cities[city_index].adj_cities
        for i in range(0,people_in_transit):
            #print("CURR_CITY:",citizens[transit_indices_curr_city[i]].curr_city,"NEW_CITY:",cities[city_index].adj_cities[rand_adj_city_index])
            citizens[transit_indices_curr_city[i]].curr_city=cities[city_index].adj_cities[rand_adj_city_index]


    # infection counter, replace
    infected_sum_den = 0
    infected_sum_SL = 0
    infected_sum_ph = 0
    infected_sum_al = 0
    infected_sum_ch = 0
    for i in range(0,len(citizens)):
        if (citizens[i].curr_city=="Denver") and (citizens[i].infected==True):
            infected_sum_den=infected_sum_den+1
        if (citizens[i].curr_city=="Salt Lake City") and (citizens[i].infected==True):
            infected_sum_SL=infected_sum_SL+1
        if (citizens[i].curr_city=="Phoenix") and (citizens[i].infected==True):
            infected_sum_ph=infected_sum_ph+1
        if (citizens[i].curr_city=="Albuquerque") and (citizens[i].infected==True):
            infected_sum_al=infected_sum_al+1
        if (citizens[i].curr_city=="Cheyenne") and (citizens[i].infected==True):
            infected_sum_ch=infected_sum_ch+1
    print("Day:",str(day)+", Infected:",infected_sum_den)
    infected_people_den=np.append(infected_people_den,infected_sum_den)
    infected_people_SL=np.append(infected_people_SL,infected_sum_SL)
    infected_people_ph=np.append(infected_people_ph,infected_sum_ph)
    infected_people_al=np.append(infected_people_al,infected_sum_al)
    infected_people_ch=np.append(infected_people_ch,infected_sum_ch)
    day_arr=np.append(day_arr,day)
plt.plot(day_arr,infected_people_den,label="Denver")
plt.plot(day_arr,infected_people_SL,label="Salt Lake")
plt.plot(day_arr,infected_people_ph,label="Phoenix")
plt.plot(day_arr,infected_people_al,label="Albuquerque")
plt.plot(day_arr,infected_people_ch,label="Cheyenne")
plt.legend(loc="upper left")
plt.show()
#for i in range(0,len(citizens)):
