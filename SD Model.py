from click import style
from matplotlib.style import available
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
        
    def increment_time_step(self, step, stocks, rates):
        for key in stocks:
            stocks[key].next_val(step, stocks, rates, self.timestep)
         
    def run(self, stocks, rates):
        # simulate the model for the calculated number of steps
        from rich.progress import track

    
        for step in track(range(1,self.steps)):
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

    
    def plot_graphs(self, results, title,ylabel, phase_plot, stack_bar, line_graph):
        
        

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
        
        if phase_plot:
            results.plot(x=results.columns[1], y=results.columns[2], title="Phase Plot",xlabel=results.columns[1], ylabel=results.columns[2], legend=False)
        
        plt.show()


def import_model(stock_file, rate_file):
    
    stocks={}

# Rates are as a dictionary of lists - which are then converted to a dataframe

    import pandas as pd

    #load Stock data
    # stocks_df=pd.read_csv("Stocks.csv")
    stocks_df=pd.read_csv(stock_file)
    
    for index, row in stocks_df.iterrows():
        #print(row.Stock)
        stocks[row.Stock]=stock(row.Stock, row.Value)

    #Load rate data
    
    # rates=pd.read_csv("Rates.csv")
    rates=pd.read_csv(rate_file)

    console.print ("\nStock Data", style="underline")
    print("\n",stocks_df)
    console.print("\nRates", style="underline")
    print("\n",rates,"\n")

    print("Model Created\n")
   

    return rates, stocks
        
##############################################################################################################
# Main Code

from rich import print
from rich.console import Console
console = Console()


console.print ("Available_models\n", style="underline")
available_models=pd.read_csv("Models.csv")
print (available_models)

print()
user_input=input("Select model number ")

console.print("\nInitialising Model\n", style="underline")
model_params=available_models.iloc[[user_input]]['Definition'].values[0]

model_data=pd.read_csv(model_params, header=None, index_col=0).to_dict()
print(f"\nName  {model_data[1]['model_name']:>14}")
print(f"Duration  {int(model_data[1]['duration']):>10}")
print(f"Start  {int(model_data[1]['start_time']):>13}")
print(f"Step {float(model_data[1]['timestep']):>15}")

# validate input?

simulation=model(model_data[1]['model_name'],int(model_data[1]['duration']),int(model_data[1]['start_time']),float(model_data[1]['timestep']))

rates,stocks = import_model(model_data[1]['stock_file'],model_data[1]['rates_file'])

#Execute the model
print("\nStarting Simulation")

from rich.progress import track


simulation.run(stocks, rates)

#Save the output data
output_file=model_data[1]['model_name']+".xlsx"
results=simulation.save_results(output_file)


#Plot 
def str2bool(v):
  return v.lower() in ("yes")

line_graph=bool(str2bool(model_data[1]['line_graph']))
stack_bar=bool(str2bool(model_data[1]['stack_bar']))
phase_plot=bool(str2bool(model_data[1]['phase_plot']))

title=model_data[1]['title']
ylabel=model_data[1]['y_label']

print("\nSimulation Ended")

simulation.plot_graphs(results, title,ylabel, phase_plot, stack_bar, line_graph)
