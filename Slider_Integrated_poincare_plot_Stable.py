# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 16:10:35 2019

@author: Sujith Tenali
"""

import pandas as pd

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row,column
#from bokeh import events
from bokeh.models import CustomJS, ColumnDataSource, CDSView, GroupFilter, BoxSelectTool, TapTool, HoverTool, PolySelectTool,MultiSelect,CheckboxGroup
from bokeh.models.callbacks import CustomJS
from bokeh.models.widgets import RadioButtonGroup,Button,Slider,TextInput,CheckboxButtonGroup,Div

# import datetime




# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
data = pd.read_csv("df_rhythmInfo_32748_1552798645150441.csv") 


RRSec = data["RRSec"] 

#RRSec_n_minus_1 = RRSec.shift(-1,axis =0)
RRSec_n_minus_1 = RRSec.shift(1,axis =0)
data["RRSec_n_minus_1"] = RRSec_n_minus_1
data['RRSec_n_minus_2'] = data.RRSec.shift(+2,axis=0)
#data['RRSec_n_plus_1'] = data.RRSec.shift(-1,axis=0)
data["RRSec_sum"] = data.RRSec_n_minus_1 + data.RRSec
data["RRSec_sum_check"] = data.RRSec_sum - data.RRSec_n_minus_2; 
data['beatCharN'] = data['beatChar']
data['beatCharN2'] = data['beatChar']
data['beatCharN3'] = data['beatChar'] 
data['SerialNo2'] = data['SerialNo']
data['SerialNo3'] = data['SerialNo']
data['noise'] = 'False'
#beatChar = data['beatChar']
data['localTime'] = pd.to_datetime(data['epochTime'], unit = 'us', utc = None).astype('datetime64[ns, Asia/Kolkata]')
data['change'] = 0
#print(data['beatChar'])

#print(data['SerialNo'])

# ---------------------------
s1 = ColumnDataSource(data=dict(x=data['RRSec_n_minus_1'], y=data['RRSec'], time=data['epochTime'], ann=data['beatChar'], localtime = data['localTime'],  change = data['change'], SerialNo = data['SerialNo'],SerialNo2 = data['SerialNo2'], SerialNo3 = data['SerialNo3'],noise = data['noise'],RRSec_n_minus_2 = data['RRSec_n_minus_2']))
data.set_index('beatChar', drop=True, append=False, inplace=True, verify_integrity=False)

#noise = ColumnDataSource(data=dict(RRSec=[],epochTime=[],beatChar=[],SerialNo=[],SerialNo2=[],SerialNo3=[]))
#print('passed1')

s2 = ColumnDataSource(data=dict(x=[], y=[], time=[], ann=[],noise=[]))
s3 = ColumnDataSource(data=dict(x=[], y=[], time=[], ann=[], change=[],noise=[]))
s4 = ColumnDataSource(data=dict(x=[], y=[], time=[], ann=[],noise=[]))
#S5 = ColumnDataSource(data=data)
#noise2 = ColumnDataSource(data=dict(x=[], y=[])) 		  
#print(S5.data) 

#print('passed2')


source = ColumnDataSource(data=dict(value=[]))

view_green_s1 = CDSView(source=s1, filters=[GroupFilter(column_name='ann', group='N')])
view_red_s1 = CDSView(source=s1, filters=[GroupFilter(column_name='ann', group='V')])
view_blue_s1 = CDSView(source=s1, filters=[GroupFilter(column_name='noise', group='True')])

view_green_s4 = CDSView(source=s4, filters=[GroupFilter(column_name='ann', group='N')])
view_red_s4 = CDSView(source=s4, filters=[GroupFilter(column_name='ann', group='V')])
view_blue_s4 = CDSView(source=s4, filters=[GroupFilter(column_name='noise', group='True')])


# output to static HTML file
output_file("Poincare.html")

data.to_csv(r'C:\Users\Sujith Tenali\Desktop\zero11.csv')


# ------------------------------------------ FIGURE 1 ----------------------------------------------------------
# # configure visual properties on a plot's figure attribute

p1 = figure(output_backend="webgl", plot_width=700, plot_height=700) 
p1.add_tools(BoxSelectTool()) 
p1.add_tools(PolySelectTool())
p1.toolbar.active_drag =BoxSelectTool()
p1.toolbar.active_scroll = None
p1.toolbar.active_tap = None
p1.toolbar.active_inspect = None

# p1.add_tools(TapTool())
p1.add_tools(HoverTool(
    tooltips=[
        	('index', '$index'),
	    	('(x,y)', '($x, $y)'),
    		('time', '@localtime{%c}'),
    ],

    formatters={
        	'localtime' : 'datetime', # use 'datetime' formatter for 'time' field
    },
))

font_name = "Gill Sans MT"

# p1.title.text = "Poincare Plot"
# p1.title.text_font_size = "50px"
# p1.title.text_color = "#22ACE2"
# p1.title.text_font = font_name

p1.xaxis.axis_label = "RRn-1 (seconds)"
p1.xaxis.axis_label_text_font_size = "25px"
# p1.xaxis.axis_label_text_color = "#22ACE2"
p1.xaxis.axis_label_text_font = font_name
p1.xaxis.major_label_text_font = font_name

p1.yaxis.axis_label = "RRn (seconds)"
p1.yaxis.axis_label_text_font_size = "25px"
# p1.yaxis.axis_label_text_color = "#22ACE2"
p1.yaxis.axis_label_text_font = font_name
p1.yaxis.major_label_text_font = font_name

# add a circle renderer with a size, color, and alpha
p1.circle(x='x', y='y', size=4, legend='N', color= 'green', alpha=0.5, source=s1, view=view_green_s1)  
p1.circle(x='x', y='y', size=4, legend='V', color= 'red', alpha=0.5, source=s1, view=view_red_s1) 
p1.circle(x='x', y='y', size=4, legend='Q', color= 'blue', alpha=0.5, source=s1, view=view_blue_s1)
#p1.circle(x = 'RRSec',y = 'RRSec_n_plus_1' ,source = noise, size=4, color="blue", alpha=0.5,legend="noise", muted_color="blue", muted_alpha=0.2) 
p1.legend.location = "top_right"
p1.legend.click_policy="hide"


callback = CustomJS(args=dict(S1=s1), code="""
    
    var n = cb_obj.value;
    
    var data1 = S1.data;
    
    for(var i = 0; i < data1.y.length; i++)
    {
          data1['noise'][i] = 'False';
       if(Math.abs(data1.x[i] + data1.y[i] - data1.RRSec_n_minus_2[i]) <= n)
       {
          data1['noise'][i] = 'True';
       }
    }
    S1.change.emit();
""")
slider = Slider(start=0.0, end=0.5,value=0.0, step=0.1, title="noise%",height=65)
slider.js_on_change('value', callback)
callback.args["slider"] = slider

# ------------------------------------------ FIGURE 1 ----------------------------------------------------------


# ------------------------------------------ FIGURE 2 ----------------------------------------------------------
p2 = figure(output_backend="webgl", plot_width=700, plot_height=700, x_range=p1.x_range, y_range=p1.y_range)

p2.xaxis.axis_label = "RRn-1 (seconds)"
p2.xaxis.axis_label_text_font_size = "25px"
# p2.xaxis.axis_label_text_color = "#22ACE2"
p2.xaxis.axis_label_text_font = font_name
p2.xaxis.major_label_text_font = font_name

p2.yaxis.axis_label = "RRn (seconds)"
p2.yaxis.axis_label_text_font_size = "25px"
# p2.yaxis.axis_label_text_color = "#22ACE2"
p2.yaxis.axis_label_text_font = font_name
p2.yaxis.major_label_text_font = font_name

# add a circle renderer with a size, color, and alpha
p2.circle(x='x', y='y', size=4, legend='N', color= 'green', alpha=0.5, source=s4, view=view_green_s4)
p2.circle(x='x', y='y', size=4, legend='V', color= 'red', alpha=0.5, source=s4, view=view_red_s4)
p2.circle(x='x', y='y', size=4, legend='Q', color= 'blue', alpha=0.5, source=s4, view=view_blue_s4)

p2.legend.location = "top_right"
p2.legend.click_policy="hide"

# ------------------------------------------ FIGURE 2 ----------------------------------------------------------











s1.selected.js_on_change('indices', CustomJS(args=dict(s1=s1, s2=s2), code="""
        var inds = cb_obj.indices;
        var d1 = s1.data;
		var d2 = s2.data;
        
        var len = inds.length;

		d2['x'] = []
        d2['y'] = []
		d2['time'] = []
		d2['ann'] = []
        d2['noise'] = []
        
        

        for (var i = 0; i < len; i++) {
            d2['x'].push(d1['x'][inds[i]])
            d2['y'].push(d1['y'][inds[i]])
	    d2['time'].push(d1['time'][inds[i]])
	    d2['ann'].push(d1['ann'][inds[i]])
        d2['noise'].push(d1['noise'][inds[i]])
       }
        s2.change.emit();
    """)
)

#ColumnDataSource(data=dict(x=[], y=[], time=[], ann=[], change=[],noise=[]))


callback3 = CustomJS(args=dict(s2=s2, s4=s4, s3 = s3),code="""
                           d2 = s2.data;
                           d4 = s4.data;
                           d3 = s3.data;
                           
                             d4['x']=[];
                             d4['y']=[];
	                         d4['time']=[];
                             d4['ann']=[];
                             d4['noise']=[];
                             
                             
                             d3['x']=[];
                             d3['y']=[];
	                         d3['time']=[];
                             d3['ann']=[];
                             d3['noise']=[];
                             d3['change'] = [];
                             
                             
                         
                           
                           //console.log(cb_obj.active);
                           
                           if (cb_obj.active.includes(0) && cb_obj.active.includes(1) && cb_obj.active.includes(2))
                            {
                            
                            for (var i = 0; i < d2['x'].length; i++) 
                            {
                             d4['x'].push(d2['x'][i])
                             d4['y'].push(d2['y'][i])
	                         d4['time'].push(d2['time'][i])
                             d4['ann'].push(d2['ann'][i])
                             d4['noise'].push(d2['noise'][i])
                             
                             d3['x'].push(d2['x'][i])
                             d3['y'].push(d2['y'][i])
	                         d3['time'].push(d2['time'][i])
                             d3['ann'].push(d2['ann'][i])
                             d3['noise'].push(d2['noise'][i])
                             d3['change'].push(0)
                            }
                            }
                           else if(cb_obj.active.includes(0) && cb_obj.active.includes(1) )
                           {
                           for (var i = 0; i < d2['x'].length; i++) 
                           {
                            if((d2['ann'][i]==='N') || (d2['ann'][i]==='V'))
                            {
                             d4['x'].push(d2['x'][i])
                             d4['y'].push(d2['y'][i])
	                         d4['time'].push(d2['time'][i])
                             d4['ann'].push(d2['ann'][i])
                             d4['noise'].push(d2['noise'][i]+'N')
                             
                             d3['x'].push(d2['x'][i])
                             d3['y'].push(d2['y'][i])
	                         d3['time'].push(d2['time'][i])
                             d3['ann'].push(d2['ann'][i])
                             d3['noise'].push(d2['noise'][i])
                             d3['change'].push(0)
                             
                            }
                            }
                            }
                            else if(cb_obj.active.includes(0) && cb_obj.active.includes(2) )
                            {
                            for (var i = 0; i < d2['x'].length; i++) 
                           {
                            if((d2['ann'][i]==='N') || (d2['noise'][i]==='True'))
                            {
                             d4['x'].push(d2['x'][i])
                             d4['y'].push(d2['y'][i])
	                         d4['time'].push(d2['time'][i])
                             d4['ann'].push(d2['ann'][i])
                             d4['noise'].push(d2['noise'][i])
                             
                             d3['x'].push(d2['x'][i])
                             d3['y'].push(d2['y'][i])
	                         d3['time'].push(d2['time'][i])
                             d3['ann'].push(d2['ann'][i])
                             d3['noise'].push(d2['noise'][i])
                             d3['change'].push(0)
                            }
                            }
                            }
                            else if(cb_obj.active.includes(1) && cb_obj.active.includes(2))
                            {
                            //console.log('first')
                            for (var i = 0; i < d2['x'].length; i++) 
                           {
                           //console.log('sec')
                            if((d2['ann'][i]==='V') || (d2['noise'][i]==='True'))
                            {
                            
                             d4['x'].push(d2['x'][i])
                             d4['y'].push(d2['y'][i])
	                         d4['time'].push(d2['time'][i])
                             d4['ann'].push(d2['ann'][i])
                             d4['noise'].push(d2['noise'][i])
                             
                             d3['x'].push(d2['x'][i])
                             d3['y'].push(d2['y'][i])
	                         d3['time'].push(d2['time'][i])
                             d3['ann'].push(d2['ann'][i])
                             d3['noise'].push(d2['noise'][i])
                             d3['change'].push(0)
                            }
                            }
                            }
                            else if(cb_obj.active.includes(0))
                            {
                            for (var i = 0; i < d2['x'].length; i++) 
                           {
                            if(d2['ann'][i]==='N')
                            {
                             d4['x'].push(d2['x'][i])
                             d4['y'].push(d2['y'][i])
	                         d4['time'].push(d2['time'][i])
                             d4['ann'].push(d2['ann'][i])
                             d4['noise'].push(d2['noise'][i]+'N')
                             
                             d3['x'].push(d2['x'][i])
                             d3['y'].push(d2['y'][i])
	                         d3['time'].push(d2['time'][i])
                             d3['ann'].push(d2['ann'][i])
                             d3['noise'].push(d2['noise'][i])
                             d3['change'].push(0)
                            }
                            }
                            }
                            else if(cb_obj.active.includes(1))
                            {
                            for (var i = 0; i < d2['x'].length; i++) 
                           {
                            if(d2['ann'][i]==='V')
                            {
                             d4['x'].push(d2['x'][i])
                             d4['y'].push(d2['y'][i])
	                         d4['time'].push(d2['time'][i])
                             d4['ann'].push(d2['ann'][i])
                             d4['noise'].push(d2['noise'][i]+'N')
                             
                             d3['x'].push(d2['x'][i])
                             d3['y'].push(d2['y'][i])
	                         d3['time'].push(d2['time'][i])
                             d3['ann'].push(d2['ann'][i])
                             d3['noise'].push(d2['noise'][i])
                             d3['change'].push(0)
                            }
                            }
                            }
                            else if(cb_obj.active.includes(2))
                            {
                            //console.log('entred');
                            
                            for (var i = 0; i < d2['x'].length; i++) 
                           {
                           //console.log(d2['noise'][i]);
                           
                            if(d2['noise'][i]==='True')
                            {
                            
                             d4['x'].push(d2['x'][i])
                             d4['y'].push(d2['y'][i])
	                         d4['time'].push(d2['time'][i])
                             d4['ann'].push(d2['ann'][i])
                             d4['noise'].push(d2['noise'][i])
                             
                             d3['x'].push(d2['x'][i])
                             d3['y'].push(d2['y'][i])
	                         d3['time'].push(d2['time'][i])
                             d3['ann'].push(d2['ann'][i])
                             d3['noise'].push(d2['noise'][i])
                             d3['change'].push(0)
                            }
                            }
                            }
                            
                            s3.change.emit();
                            s4.change.emit();
                            
                            """)
                    

checkboxes = CheckboxGroup(name="Select beats to display",labels=['N','V','Q'], active=[0, 1,2],callback = callback3,height = 120)

checkboxes.active = []
checkboxes.js_on_click(callback3)

div = Div(text="""<b>Select annotations to change: </b>""",
width=200, height=0)

div2 = Div(text="""<b>Change annotations to : </b>""",
width=200, height=0)

div3 = Div(text="""<b>Select noise level : </b>""",
width=200, height=0)





cb_rgrp_button = CustomJS(args=dict(source= source), code="""
	var data = source.data;
	var button_value =data['value'];
	console.log("button_value = ", button_value);
	var ann_value = cb_obj.active;
	button_value[0] = ann_value;
	console.log("button value ", button_value[0]);
	source.change.emit();
    """)





callback = CustomJS(args=dict(s1=s1, s2=s4, s3=s3, source = source), code="""
                    
    var d1 = s1.data;
	var d2 = s2.data;
	var d3 = s3.data;
    
    d3['x']=[];
    d3['y']=[];
    d3['time']=[];
    d3['ann']=[];
    d3['noise']=[];
    d3['change']=[];

	var temp = 0;
    var index = 0;

	var data = source.data;
	var button_value =data['value'];

	var ann_value = button_value[0];
	var ann_string = "";

	var d2_len = d2['ann'].length;

	    switch(ann_value)
	    {
		case 0:
		    ann_string = "N";
		break;
		case 1:
		    ann_string = "V"
		    break;
		case 2:
		    ann_string = "Q"
		    break;
		case 3:
		    ann_string = "Delete Bin"
		    break;
	    case 4:
		    ann_string = "Noise Bin"
		    break;
	    }

	for (var i = 0; i < d2_len; i++)
	{
		index = d1['time'].indexOf(d2['time'][i]);

		switch(d2['ann'][i])
		{
			case "N":
				temp = 0;
				break;
			case "V":
				temp = 1;
				break;
			case "Q":
				temp = 2;
				break;
			case "Delete Bin":
				temp = 3;
				break;
			case "Noise Bin":
				temp = 4;
				break;
		}

		//console.log("temp", temp);
		console.log("ann value", ann_value);
		//console.log("ann string", ann_string);
        d3['change'][index] = 0;
		if ((temp != ann_value) && (temp!=4))
		{
			//d1['ann'][index] = ann_string;
			//d1['change'][index] = 1;
            console.log(index)
			d3['ann'][index] = ann_string;
			d3['change'][index] = 1;
			d3['x'][index] = d1['x'][index];
			d3['y'][index] = d1['y'][index];
			d3['time'][index] = d1['time'][index];
            console.log('conf'+d3['time'][index])
            d3['noise'][index] = d1['noise'][index];

			d2['ann'][i] = ann_string; 
		}
        
        if ((temp != ann_value) && (temp==4))
		{
			//d1['ann'][index] = ann_string;
			//d1['change'][index] = 1;
            console.log(index)
			d3['ann'][index] = ann_string;
			d3['change'][index] = 1;
			d3['x'][index] = d1['x'][index];
			d3['y'][index] = d1['y'][index];
			d3['time'][index] = d1['time'][index];
            console.log('conf'+d3['time'][index])
            d3['noise'][index] = 'True';

			d2['ann'][i] = ann_string; 
            d2['noise'][i] = 'True';
		}
	}
	console.log("here ")
        //s1.change.emit();
	s2.change.emit();
	s3.change.emit();
    """)


#cb_button = CustomJS(args=dict(source=s1), code="""
cb_button = CustomJS(args=dict(source=s3), code="""
		var data = source.data;
		var filetext = 'epochTime,beatChar,noise\\n';
        var len = data['time'].length;

		for (i=0; i < len; i++)
		{
			if(data['change'][i])
			{
                
				var currRow = [data['time'][i].toString(), data['ann'][i].toString(),data['noise'][i].toString().concat('\\n')];
				var joined = currRow.join();
				filetext = filetext.concat(joined);
			}
            //if(data['change'][i]!=1)
            //{
              //  console.log('conf'+data['time'][i])
			//	var currRow = [data['time'][i].toString(), data['ann'][i].toString(),data['noise'][i].toString().concat('\\n')];
			//	var joined = currRow.join();
			//	filetext = filetext.concat(joined);
            //}
		}

		var filename = 'Data Changes.csv';
		var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });

		//addresses IE
		if (navigator.msSaveBlob) {
			navigator.msSaveBlob(blob, filename);
		}

		else {
			var link = document.createElement("a");
			link = document.createElement('a')
			link.href = URL.createObjectURL(blob);
			link.download = filename
			link.target = "_blank";
			link.style.visibility = 'hidden';
			link.dispatchEvent(new MouseEvent('click'))
		}
	""") 




annotation_select = RadioButtonGroup(labels=["N", "V", "Q", "Delete Bin", "Noise Bin"], callback=cb_rgrp_button,height=15)

refresh = Button(label="Refresh ", button_type="success", callback = callback,sizing_mode='scale_height',width=100,height=10)
refresh.js_on_click(callback)



change_button = Button(label="Change ", button_type="success", sizing_mode='scale_width',callback = callback,width=100,height=10)

button = Button(label="Download Changed Annotations", button_type="success", callback = cb_button,height=0) 

figure = row(p1, column(div3,slider,div,checkboxes,div2,annotation_select,row(change_button, refresh), button),p2)

show(figure)
