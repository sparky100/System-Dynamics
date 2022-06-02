import pandas as pd
import matplotlib.pyplot as plt

class stock:
    def __init__(self, name, start): # used when creating a new instance
        self.name = name
        self.value = [start]

    def next_val(self,  step, stocks, rates, timestep):
            #rate 0 calculation
            # Get rate0 - constant growth
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
             #       print(delta1)
            
           
            #rate 2  calculation        
            rate2= rates[(rates["Target"]==self.name) & (rates["RateType"]==2)]
            if rate1.empty == False:
                for index, row in rate2.iterrows():
                    delta2+= stocks[row.Source].value[step-1] * row.Value * self.value[step-1] 
            
            new_value=self.value[step-1]+delta0+(delta1+delta2)*timestep
            #print(self.name, new_value)
            self.value.append(new_value)

class model:
    def __init__(self, name, duration, start_time, timestep): # used when creating a new instance
        self.name = name
        self.duration = duration
        self.timestep=timestep
        self.steps=int(duration/timestep)
        self.simtime= start_time
        self.start_time=start_time
        print(self)
        
    def increment_time_step(self, step, stocks, rates):
        for key in stocks:
            stocks[key].next_val(step, stocks, rates, self.timestep)
         
    def run(self, stocks, rates):
        # simulate the model for the calculated number of steps
        for step in range(1,self.steps):
            self.simtime+=self.timestep
            self.increment_time_step(step, stocks, rates)              

    def save_results(self, file_name):
        
        data=pd.DataFrame({"Time":range(0, self.steps)})
        
        #Add each stock to the data frame
        for key in stocks:
            data[key]=stocks[key].value 

        data["Time"]=self.start_time+(data["Time"]*self.timestep)
        #data["Year"]=round(data['Time'],0)
        
        data.to_excel(file_name)
        return data            

    def plot_graphs(self, results, title,ylabel, stack_bar, line_graph):
        
        

        #Filter data so it is just  integer times
        import math
        plot_results=results[results.index.isin(range(0,self.steps+1,int(1/self.timestep)))]
        
        #Line chart

        if line_graph:
            # plot_results.plot(x="Time", title=title, ylabel=ylabel)
#            plot_results.plot(x="Time", title=title, ylabel=ylabel,xticks=range(self.start_time,self.start_time+self.duration,1))
            results.plot(x="Time", title=title, ylabel=ylabel,xticks=range(self.start_time,self.start_time+self.duration,1))

 #           plt.xticks = range(self.start_time,self.duration,1)

        #Vertical Stack
        if stack_bar:
#            ax = plot_results.plot.bar(x="Time", title=title, stacked=True, xticks=range(self.start_time,self.start_time+self.duration,1))
            stack_results=plot_results.copy()
            stack_results['Time']=plot_results['Time'].astype(int)
            
            ax = stack_results.plot.bar(x="Time", ylabel=ylabel, stacked=True,title=title)
            plt.legend(bbox_to_anchor=(1.02, 0.1), loc='right', borderaxespad=0)
            
        #Phase plane plot, xticks=range(self.start_time,1)
        #results.plot(x="Children", y="Adults", title="Phase Plot",xlabel="Children", ylabel="Adults", legend=False)
        
        plt.show()


def import_model(stock_file, rate_file):
    
    stocks={}

# Rates are as a dictionary of lists - which are then converted to a dataframe

    import pandas as pd

    #load Stock data
    # stocks_df=pd.read_csv("Stocks.csv")
    stocks_df=pd.read_csv(stock_file)
    
    for index, row in stocks_df.iterrows():
        print(row.Stock)
        stocks[row.Stock]=stock(row.Stock, row.Value)

    #Load rate data
    
    # rates=pd.read_csv("Rates.csv")
    rates=pd.read_csv(rate_file)

    print ("Stock Data")
    print(stocks_df)
    print("")
    print("Rates")
    print(rates)
    print("")

    return rates, stocks
        
##############################################################################################################
# Main Code

from rich import print

print("Starting Simulation")

#Initialise Model
model_name="Population"
model_duration=6
model_start_time=0
model_timestep=.083333

simulation=model(model_name,model_duration,model_start_time, model_timestep)

rates,stocks = import_model("StockHouses.csv","RatesHouses.csv")

#Execute the model
simulation.run(stocks, rates)

#Save the output data
output_file="test.xlsx"
results=simulation.save_results(output_file)

#Plot graphs
line_graph=True
stack_bar=True
title="Houses Built Over time"
ylabel="Number"

simulation.plot_graphs(results, title,ylabel, stack_bar, line_graph)
