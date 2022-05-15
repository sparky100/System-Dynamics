import pandas as pd
import matplotlib.pyplot as plt

class stock:
    def __init__(self, name, start): # used when creating a new instance
        self.name = name
        self.value = [start]

    def next_val(self,  step, stocks, rates, timestep):
            #rate 0 calculation
            # Get rate0
            delta0=0
            delta1=0
            delta2=0
            rate0= rates[(rates["Target"]==self.name) & (rates["RateType"]==0)]
            if rate0.empty == False:
                delta0 = rate0.Value # need chainging
             
            #rate 1 calculation
            rate1= rates[(rates["Target"]==self.name) & (rates["RateType"]==1)]
            if rate1.empty == False:
                for index, row in rate1.iterrows():
                    delta1+= stocks[row.Source].value[step-1] * row.Value 
            
           
            #rate 2  calculation        
            rate2= rates[(rates["Target"]==self.name) & (rates["RateType"]==2)]
            if rate1.empty == False:
                for index, row in rate2.iterrows():
                    delta2+= stocks[row.Source].value[step-1] * row.Value * self.value[step-1] 
            
            new_value=self.value[step-1]+delta0+(delta1+delta2)*timestep
            
            self.value.append(new_value)

class model:
    def __init__(self, name, duration, timestep): # used when creating a new instance
        self.name = name
        self.duration = duration
        self.timestep=timestep
        self.steps=int(duration/timestep)
        self.simtime= 0
        print(self)
        
    def increment_time_step(self, step, stocks, rates):
        for key in stocks:
            stocks[key].next_val(step, stocks, rates, self.timestep)
         
    def run(self):
        # simulate the model for the calculated number of steps
        for step in range(1,self.steps):
            self.simtime+=self.timestep
            self.increment_time_step(step, stocks, rates)              

    def save_results(self, file_name):
        
        data=pd.DataFrame({"Time":range(0, self.steps)})

        #Add each stock to the data frame
        for key in stocks:
            data[key]=stocks[key].value 

        data["Time"]=data["Time"]*modelrun.timestep
        data.to_excel(file_name)
        return data            

    def plot_graphs(self, results):
        
        results.plot(x="Time", title="Population Against Time", ylabel="Population")

        #Phase plane plot
        results.plot(x="Rabbit", y="Fox", title="Phase Plot",xlabel="Rabbits", ylabel="Foxes", legend=False)

        plt.show()


        
##############################################################################################################
# Main Code

# Define stocks and initial values

Rabbit = stock("Rabbit", 20)
Fox = stock("Fox",20)

# Create Dictionary for Stocks

stocks={}
stocks={"Rabbit":Rabbit,"Fox":Fox}

# Rates are as a dictionary of lists - which are then converted to a dataframe

import pandas as pd

ratedata={"Target":["Rabbit","Rabbit","Fox","Fox"],
          "Source":["Rabbit","Fox","Fox","Rabbit"],
          "RateType":[1,2,1,2],
          "Description":["Birth rate","Predation Rate","Death Rate", "Predator Growth"], 
          "Value":[1,-0.01,-1.0,0.01]}

rates=pd.DataFrame(ratedata)

#Initialise Model
model_name="Predator"
model_duration=15
model_starttime=0
Model_timestep=0.01

modelrun=model(model_name,model_duration,Model_timestep)

#Execute the model
modelrun.run()

#Save the output data
output_file="test.xlsx"
results=modelrun.save_results(output_file)

#Plot graphs
modelrun.plot_graphs(results)

