import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import matplotlib
import geopandas as gpd

from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.widgets import Slider, Button


matplotlib.use('webagg')

# load data
eqDf = pd.read_csv('earthquakes_2010to2016.csv')
fDf = pd.read_csv('subsetFracking.csv')
fDf['long'] = fDf['Longitude']
fDf['lat'] = fDf['Latitude']
eqDf['long'] = eqDf['longitude']
eqDf['lat'] = eqDf['latitude']

# change bounds of data geographically
x1 = -130
x2 = -60
y1 = 24
y2 = 50



fDf = fDf[(fDf['long'] > x1) & (fDf['long'] < x2) & 
           (fDf['lat'] > y1) & (fDf['lat'] < y2)]
fDf = fDf.reset_index()
eqDf = eqDf[(eqDf['long'] > x1) & (eqDf['long'] < x2) & 
           (eqDf['lat'] > y1) & (eqDf['lat'] < y2)]
eqDf = eqDf.reset_index()

# extract time
years = np.zeros(len(eqDf['long']))
for row, val in eqDf.iterrows():
    date = datetime.datetime.strptime(val.time,
		 "%Y-%m-%dT%H:%M:%S.%fZ")
    years[row] = date.year
	
eqDf['year']=years

years = np.zeros(len(fDf['long']))
for row, val in fDf.iterrows():
    date = datetime.datetime.strptime(val.JobStartDate,
		 "%m/%d/%Y %H:%M:%S %p")
    years[row] = date.year
fDf['year']=years



# set up figures
fig, ax1 = plt.subplots()
ax1.set(xlim=(x1,x2),ylim=(y1,y2), autoscale_on=False)
figsldr, axsldr = plt.subplots()
figzoom, axzoom = plt.subplots()
figplot, axplot = plt.subplots()
axplot.set(title='Earthquake and Fracking from 1950-2016')
axplot2 = axplot.twinx()
axzoom.set(xlim=(x1,x2),ylim=(y1,y2), autoscale_on=False,
	title='Click main figure to zoom!')

# plot world graph and get length of ax1
world = gpd.read_file('us_map.json')
world.plot(ax = ax1, legend=True, color='black',
 edgecolor='black', linewidth=1, alpha=1)
world.plot(ax = axzoom, legend=True, color='black',
 edgecolor='black', linewidth=1, alpha=1)
length = len(ax1.get_children())
lengthzoom = len(axzoom.get_children())

custom_lines = [Line2D([0], [0], color='blue', lw=4),
                Line2D([0], [0], color='orange', lw=4)]
ax1.legend(custom_lines, ['Earthquakes', 'Fracking'])
axzoom.legend(custom_lines, ['Earthquakes', 'Fracking'])
axplot.legend(custom_lines, ['Earthquakes', 'Fracking'])



# first drawing

# earthquake data
sample_size = 1000

def decr_data(data, init, sample_size):
	data_temp = data[data['year'] == init]
	if (len(data_temp) >= sample_size):
		data_temp = data_temp.sample(n=sample_size)
	return data_temp
	
eqDf_temp = decr_data(eqDf, 2011, sample_size)
fDf_temp = decr_data(fDf, 2011, sample_size)

#earthquake
fig1_eq = sns.kdeplot(x=eqDf_temp['long'], y=eqDf_temp['lat'],
	 shade = True, ax = ax1,color = 'blue', alpha = 0.8)
	 
figzoom_eq = sns.kdeplot(x=eqDf_temp['long'], y=eqDf_temp['lat'],
	 shade = True, ax = axzoom,color = 'blue', alpha = 0.8)
#fracking
fig1_f = sns.kdeplot(x=fDf_temp['long'], y=fDf_temp['lat'],
	 shade = True, ax = ax1,color = 'orange', alpha = 0.5)
	 
figzoom_f = sns.kdeplot(x=fDf_temp['long'], y=fDf_temp['lat'],
	 shade = True, ax = axzoom,color = 'orange', alpha = 0.5)

# slider
time_slider = Slider(
    ax=axsldr,
    label="Time (years)",
    valmin=2010,
    valmax=2016,
    valinit=2011,
    valfmt = "%i"
)

class updater:
	def __init__(self,a,a1,length,fig,ax1,eqDf,fDf,sample_size):
		self.a = a
		self.a1=a1
		self.length = length
		self.fig = fig
		self.ax1 = ax1
		self.eqDf = eqDf
		self.fDf = fDf
		self.sample_size = sample_size
			
	def update(self,val):
		# remove old drawings
		def remove_stuff(list, length, a):
			list = a.get_children()
			list = list[1:(len(list) - length)]
			for c in list:
				c.remove()
			
		# modify data for year		
		def new_data(data, val, sample_size, ax1, c, alpha):
			val = round(val,0)
			data_temp = data[data['year'] == val]
			if (len(data_temp) >= sample_size):
				data_temp = data_temp.sample(n=sample_size)
			a = sns.kdeplot(x=data_temp['long'], y=data_temp['lat'],
				 shade = True, ax = ax1,color=c, alpha = alpha)

			
		list1 = self.a.get_children()
		remove_stuff(list1, self.length, self.a)
		new_data(self.eqDf, val, self.sample_size, self.ax1, 'blue', 0.8)
		new_data(self.fDf, val, self.sample_size, self.ax1, 'orange', 0.5)
				
		self.fig.canvas.draw()

# initialize class and call slider update
myClass_fig1 = updater(fig1_eq,fig1_f,length,fig,ax1,eqDf,fDf,sample_size)

time_slider.on_changed(myClass_fig1.update)

print(time_slider.val)


class zoomfig:
	def __init__(self, eqDf, fDf, axzoom, figzoom, length, sample_size,
					a, a1, time, earthquake, figplot, axplot, axplot2):
		self.eqDf = eqDf
		self.fDf = fDf
		self.axzoom = axzoom
		self.figzoom = figzoom
		self.length = length
		self.sample_size = sample_size
		self.a = a
		self.a1 = a1
		self.time = time
		self.earthquake = earthquake
		self.figplot = figplot
		self.axplot = axplot
		self.axplot2 = axplot2
		
	def on_press(self, event):
		# change axis limits
		if event.button != 1:
			return
		x, y = event.xdata, event.ydata
		delta = 5
		self.axzoom.set_xlim(x - delta, x + delta)
		self.axzoom.set_ylim(y - delta, y + delta)
		## graph data
		# set bounds
		def set_bounds(data, x, y, delta):
			x1 = x - delta
			x2 = x + delta
			y1 = y - delta
			y2 = y + delta
			data_new = data[(data['long'] > x1) & (data['long'] < x2) & 
           		(data['lat'] > y1) & (data['lat'] < y2)]
				
			
			return data_new.reset_index()
			
		eqDf_temp = set_bounds(self.eqDf, x, y, delta)
		fDf_temp = set_bounds(self.fDf, x, y, delta)
		
		# graph data
		
		def remove_stuff(list, length, a):
			list = a.get_children()
			list = list[1:(len(list) - length)]
			for c in list:
				c.remove()
				
		# graph data based on year and bounds set
		def new_data(data, val, sample_size, ax1, c, alpha):
			val = round(val,0)
			data_temp = data[data['year'] == val]
			if (len(data_temp) >= sample_size):
				data_temp = data_temp.sample(n=sample_size)
			a = sns.kdeplot(x=data_temp['long'], y=data_temp['lat'],
				 shade = True, ax = ax1,color=c, alpha = alpha)
				 
				 
		list1 = self.a.get_children()
		remove_stuff(list1,self.length,self.a)
		
		new_data(eqDf_temp, self.time, self.sample_size,
				 self.axzoom, 'blue', 0.8)
		new_data(fDf_temp, self.time, self.sample_size,
				 self.axzoom, 'orange', 0.5)
				
		
		self.figzoom.canvas.draw()
		
		# make stuff on new figure
		self.axplot.cla()
		self.axplot2.cla()
		eq_new = set_bounds(self.earthquake, x , y, delta)
		eq_new = eq_new.groupby(['Year'])["mag"].count()
		
		eq_new = pd.DataFrame(eq_new)
		
			
		eq_new['Years']= eq_new.index
		
		a = self.axplot.plot(eq_new["Years"], eq_new["mag"] ,'b-o')
		self.axplot.set(title='Number of Earthquakes (2.5+ mag) per Year')
		self.axplot.set_xlabel("Year")
		self.axplot.set_ylabel("Number of Earthquakes")
		
		
		
		fDf_new = set_bounds(self.fDf, x, y, delta)
		if (len(fDf_new) == 0):
			
			
			self.axplot2.set_ylabel("Total Base Water Volume Fracked (gal)")
			self.axplot2.plot([0], [0],
							color='orange', marker='o', linestyle='solid')
			
			
			custom_lines = [Line2D([0], [0], color='blue', lw=4),
	                Line2D([0], [0], color='orange', lw=4)]
			self.axplot.legend(custom_lines, ['Earthquakes', 'Fracking'])
		
		else:	
			fDf_new = fDf_new.groupby(['year'])["TotalBaseWaterVolume"].sum()
			fDf_new = pd.DataFrame(fDf_new)
			fDf_new['Years'] = fDf_new.index
			self.axplot2.set_ylabel("Total Base Water Volume Fracked (gal)")
			self.axplot2.plot(fDf_new['Years'], fDf_new['TotalBaseWaterVolume'],
									color='orange', marker='o', linestyle='solid')
			
			
			custom_lines = [Line2D([0], [0], color='blue', lw=4),
	                Line2D([0], [0], color='orange', lw=4)]
			self.axplot.legend(custom_lines, ['Earthquakes', 'Fracking'])
							  
		self.figplot.canvas.draw()

		
		



## add linear plot
# add historic earthquakes
# bound by long/lat
# do summation

#eq1947 = pd.read_csv('earthquake1937-1947.csv')
eq1970 = pd.read_csv('earthquake1948to1970.csv')
eq1980 = pd.read_csv('earthquake1971to1980.csv')
ed1985 = pd.read_csv('earthquake1980to1985.csv')
ed1990 = pd.read_csv('earthquake1986to1990.csv')
ed1991 = pd.read_csv('earthquake1991to1995.csv')
ed2000 = pd.read_csv('earthquake1996to2000.csv')
ed2009 = pd.read_csv('earthquakes_2000to2009.csv')
ed2016 = pd.read_csv('earthquakes_2010to2016.csv')

earthquake = pd.concat([eq1970, eq1980,
				ed1985, ed1990, ed1991, ed2000, ed2009, ed2016])
earthquake['long'] = earthquake['longitude']
earthquake['lat'] = earthquake['latitude']
earthquake["time"] = pd.to_datetime(earthquake["time"])
earthquake['Year'] = pd.DatetimeIndex(earthquake['time']).year


zoomfig1 = zoomfig(eqDf, fDf, axzoom, figzoom, lengthzoom, sample_size,
					figzoom_eq, figzoom_f, time_slider.val, earthquake,
					figplot, axplot, axplot2)
					
fig.canvas.mpl_connect('button_press_event', zoomfig1.on_press)

print(earthquake)

plt.show()