from bokeh.plotting import figure
from bokeh.embed import components

def kpi_graph():
    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

#################
    # create a new plot with a title and axis labels
    kpi1 = figure(title="RX Bitrate Uplink", x_axis_label='time', y_axis_label='frequency', toolbar_location=None, width=300, height=300)

    # add a line renderer with legend and line thickness to the plot
    kpi1.line(x, y,  line_width=2, color="green")
#################
    
#################
    # create a new plot with a title and axis labels
    kpi2 = figure(title="UL SINR", x_axis_label='time', y_axis_label='frequency', toolbar_location=None, width=300, height=300)

    # add a line renderer with legend and line thickness to the plot
    kpi2.line(x, y,  line_width=2, color="red")
#################
    
#################
    # create a new plot with a title and axis labels
    kpi3 = figure(title="PRB Requested", x_axis_label='time', y_axis_label='frequency', toolbar_location=None, width=300, height=300)

    # add a line renderer with legend and line thickness to the plot
    kpi3.line(x, y,  line_width=2, color="blue")
#################

#################
    # create a new plot with a title and axis labels
    kpi4 = figure(title="TX Bitrate Downlink", x_axis_label='time', y_axis_label='frequency', toolbar_location=None, width=300, height=300)

    # add a line renderer with legend and line thickness to the plot
    kpi4.line(x, y,  line_width=2, color="blue")
#################
    
#################
    # create a new plot with a title and axis labels
    kpi5 = figure(title="UL MCS", x_axis_label='time', y_axis_label='frequency', toolbar_location=None, width=300, height=300)

    # add a line renderer with legend and line thickness to the plot
    kpi5.line(x, y,  line_width=2, color="yellow")
#################
    
#################
    # create a new plot with a title and axis labels
    kpi6 = figure(title="PRB Granted", x_axis_label='time', y_axis_label='frequency', toolbar_location=None, width=300, height=300)

    # add a line renderer with legend and line thickness to the plot
    kpi6.line(x, y,  line_width=2, color="blue")

    script1, graph1 = components(kpi1)
    script2, graph2 = components(kpi2)
    script3, graph3 = components(kpi3)
    script4, graph4 = components(kpi4)
    script5, graph5 = components(kpi5)
    script6, graph6 = components(kpi6)

    return{
        "script1": script1,
        "script2": script2,
        "script3": script3,
        "script4": script4,
        "script5": script5,
        "script6": script6,
        "kpi1": graph1,
        "kpi2": graph2,
        "kpi3": graph3,
        "kpi4": graph4,
        "kpi5": graph5,
        "kpi6": graph6,
    }