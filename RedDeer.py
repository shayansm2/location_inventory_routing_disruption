#%%
import numpy as np
import pandas as pd
from TestProblem import TestProblem
from pmx_crossover import pmx_crossover
from rrc_crossover import rrc_crossover

#%%
class RedDeer:
    

    @classmethod
    def set_problem(cls, test_prblem): 
        cls.problem = test_prblem


    def __init__(self, representation = None): 

        if np.array_equal(representation,None) :
            self.random_generation()
        else :
            self.set_representation(representation)
        
        self.objective_function_calculator()
        self.fitness_function_calculator()


    def __str__(self):
        
        output =  "selected locations :\n" + str(self.representation[0]) + " \n"
        output += "customers visit order :\n" + str(self.facility_order()) + " \n"
        output += "objective function : " + str(self.objective_function) + " \n"
        output += "facility construction costs : " + str(self.facility_cost()) + "\n"
        output += "transportation and penalty costs : " + str(self.transportation_cost()) + "\n"
        output += "holding, ordering and inventory costs : " + str(self.ordering_inventory_cost()) + "\n"

        if self.penalty_function() > 0:
            output += "SOLUTION IS NOT FEASIBLE\n"

            if self.check_capacities() > 0:
                output += "violating capacity constraint!\n"
            if self.check_demand_threshold() > 0:
                output += "violating demand threshold constraint\n"
            if self.check_service_level() > 0:
                output += "violating service level constraint\n"

        else:
            output += "SOLUTION IS FEASIBLE\n"

        output += "fitness : " + str(self.fitness) + "\n"
        return output


    def __repr__(self):
        
        is_feasible = "is feasible"
        if self.penalty_function() > 0 :
            is_feasible = "is NOT feasible"
        return "a RD with " + str(self.objective_function) +  " as objective function which " + is_feasible


    def set_representation(self, representation):

        representation_location = list(representation[0])
        if representation_location == [0] * self.problem.dim_facilities:
            while (representation_location == [0] * self.problem.dim_facilities):
                representation_location = list(np.random.randint(2,size = self.problem.dim_facilities))
            representation[0] = np.array(representation_location)
        self.representation = representation


    def facility_order(self): 

        z = self.representation[0]
        indexes = np.array([range(self.problem.dim_facilities)])
        customers = np.concatenate((indexes, self.representation[1:]))
        delete_columnns = np.where(z == 0)
        customer_facility_order = np.delete(customers, delete_columnns, axis = 1)
        facility_order = []
        for i in range(self.problem.dim_customers):
            customer_id = i + 1
            facility_order.append(
                list(customer_facility_order [ :, customer_facility_order[customer_id].argsort()][0])
            )
        return np.array(facility_order)


    def order_quantity(self): 

        q = self.problem.disruption_probability
        facility_order = self.facility_order()
        visit_probability = np.zeros((self.problem.dim_customers,self.problem.dim_facilities))
        
        for customer_id in range(len(facility_order)):
            customer_order = facility_order[customer_id]

            p = np.concatenate((np.array([1]), q[customer_order][:-1].cumprod()))
            visit_probability[customer_id, customer_order] = p
        
        self.facilities_demand = np.dot(self.problem.expected_value_demand, (1-q) * visit_probability)
        self.ordering_quantity = np.sqrt((2 * self.problem.ordering_cost / self.problem.inventory_cost) * self.facilities_demand)


    def facility_cost(self):  
        z = self.representation[0]
        return np.dot(z,self.problem.opening_cost)


    def transportation_cost(self): 
        
        q = self.problem.disruption_probability
        ttl_transport_cost = 0
        facility_order = self.facility_order()

        for customer_id in range(len(facility_order)):
            customer_order = facility_order[customer_id]

            p = np.concatenate((np.array([1]), q[customer_order].cumprod()))

            c = np.concatenate((
                np.array([self.problem.transportation_customer2facility[customer_id,customer_order[0]]]),
                self.problem.transportation_facility2facility[customer_order[:-1],customer_order[1:]],
                np.array([self.problem.penalty_cost])
            ))

            ttl_transport_cost += ( np.dot(c,p) * self.problem.expected_value_demand[customer_id])

        for customer_id in range(len(facility_order)):
            customer_order = facility_order[customer_id]
            
            p1 = np.concatenate((np.array([1]), q[customer_order].cumprod()))
            p2 = np.concatenate((1 - q[customer_order], np.array([1])))
            p = p1 * p2

            c = np.concatenate((
                self.problem.transportation_customer2facility[customer_id][customer_order],
                np.array([self.problem.transportation_customer2facility[customer_id][customer_order][-1]])
            ))

            ttl_transport_cost += (np.dot(c,p) * self.problem.expected_value_demand[customer_id])

        return ttl_transport_cost



    def ordering_inventory_cost(self): 

        self.order_quantity()
        return np.sum(np.sqrt(2 * self.problem.ordering_cost * self.problem.inventory_cost * self.facilities_demand))


    def random_generation(self): 

        random_location = list(np.random.randint(2,size = self.problem.dim_facilities))
        random_routing = [list(np.random.permutation(self.problem.dim_facilities)) for i in range(self.problem.dim_customers)]
        random_representation = np.array( [random_location] + random_routing )
        self.set_representation(random_representation)


    def objective_function_calculator(self):  
        
        self.objective_function = self.ordering_inventory_cost() + self.transportation_cost() + self.facility_cost()


    def check_service_level(self):
        
        q = self.problem.disruption_probability
        ttl_service_level_deviation = 0
        facility_order = self.facility_order()

        for customer_id in range(len(facility_order)):
            customer_order = facility_order[customer_id]

            p = np.concatenate((np.array([1]), q[customer_order].cumprod()))

            c = np.concatenate((
                np.array([self.problem.transportation_customer2facility[customer_id,customer_order[0]]]),
                self.problem.transportation_facility2facility[customer_order[:-1],customer_order[1:]],
                np.array([self.problem.penalty_cost])
            ))

            service_level = np.dot(c,p)
            if service_level > self.problem.service_level:
                ttl_service_level_deviation += service_level

        return ttl_service_level_deviation

    def check_capacities(self):
        
        capacity_deviation = self.problem.capacities - self.facilities_demand
        capacity_deviation_index = np.where(capacity_deviation < 0)
        return -sum(capacity_deviation[capacity_deviation_index])


    def check_demand_threshold(self):

        z = self.representation[0]
        demand_threshold_deviation = self.facilities_demand - (self.problem.demand_threshold * z)
        demand_threshold_deviation_index = np.where(demand_threshold_deviation < 0)
        return -sum(demand_threshold_deviation[demand_threshold_deviation_index])


    def penalty_function(self):

        service_level_deviation_penalty = np.exp(self.check_service_level()) - 1
        capacity_deviation_penalty = np.exp(self.check_capacities()) - 1
        demand_threshold_deviation_penalty = np.exp(self.check_demand_threshold()) - 1
        return service_level_deviation_penalty + capacity_deviation_penalty + demand_threshold_deviation_penalty


    def fitness_function_calculator(self, penalty = 5):  
        
        self.fitness = self.objective_function + (penalty * self.penalty_function())
    

    def roaring(self):
        
        best_fitness = self.fitness.copy()
        best_representation = self.representation.copy()
        main_representation = self.representation.copy()


        for customer_id in range(self.problem.dim_customers):
            for facility_id in range(self.problem.dim_facilities - 1):

                new_representation = main_representation.copy()
                new_representation[customer_id + 1,facility_id] , new_representation[customer_id + 1,facility_id + 1] = new_representation[customer_id + 1,facility_id + 1] , new_representation[customer_id + 1,facility_id]

                new_rd = RedDeer(new_representation)
                if(new_rd.fitness < best_fitness):
                    best_fitness = new_rd.fitness
                    best_representation = new_rd.representation
        
        self.set_representation(best_representation)
        self.objective_function_calculator()
        self.fitness_function_calculator()


    def fighting(self, other):
        
        best_fitness = self.fitness.copy()
        best_representation = self.representation.copy()

        parent1 = self.representation
        parent2 = other.representation

        parent_facility_1 = parent1[0]
        parent_facility_2 = parent2[0]
        (child_facility_1, child_facility_2) = rrc_crossover(parent_facility_1, parent_facility_2)

        child1 = np.vstack((child_facility_1, parent1[1:]))  
        child2 = np.vstack((child_facility_1, parent2[1:]))
        child3 = np.vstack((child_facility_2, parent1[1:]))
        child4 = np.vstack((child_facility_2, parent2[1:]))

        childs = [child1, child2, child3, child4]
        for child in childs:
            rd = RedDeer(child)
            if rd.fitness < best_fitness:
                best_fitness = rd.fitness
                best_representation = child
        if other.fitness < best_fitness:
            best_fitness = other.fitness.copy()
            best_representation = other.representation.copy()
        
        self.set_representation(best_representation)
        self.objective_function_calculator()
        self.fitness_function_calculator()



    def mating(self, other):
        
        parent1 = self.representation
        parent2 = other.representation

        parent_facility_1 = parent1[0]
        parent_facility_2 = parent2[0]
        (child, _) = rrc_crossover(parent_facility_1, parent_facility_2)

        for customer_id in range(self.problem.dim_customers):

            parent_customer_1 = parent1[customer_id + 1]
            parent_customer_2 = parent2[customer_id + 1]
            child_customer = pmx_crossover(parent_customer_1, parent_customer_2)

            child = np.vstack((child, child_customer))
        
        rd_child = RedDeer(child)
        return rd_child


    def distance(self, other):
        
        self_representation = self.representation
        other_representation = other.representation

        self_facilities = self_representation[0]
        other_facilities = other_representation[0]
        self_customers = self_representation[1:]
        other_customers = other_representation[1:]

        facilities_distance = sum(np.abs(self_facilities - other_facilities))
        customers_distance = sum(sum(np.abs(self_customers - other_customers)))

        return (facilities_distance + 1) * np.log(customers_distance + np.e)


# %%
