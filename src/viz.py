###Adapted from soccer_analytics GitHub repository by CleKraus

# import packages
import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def create_empty_field(
    below=False, colour="green", line_colour=None, size=1, len_field=105, wid_field=68
):
    """
    Function returns a plotly figure of a soccer field.
    :param below: (bool) If true, any additional traces will overlay the field; otherwise, the field will overlay the
                         additional traces
    :param colour: (str) Colour of the field; currently only "green" and "white" are supported
    :param line_colour: (str) Colour of the line; if none it is automatically set based on the field colour
    :param size: (float) Size relative to the standard size
    :param len_field: (int) Length of soccer field in meters (needs to be between 90m and 120m)
    :param wid_field: (int) Width of soccer field in meters (needs to be between 60m and 90m)
    :return: go.Figure with a soccer field
    """

    # check the input for correctness
    assert 90 <= len_field <= 120
    assert 60 <= wid_field <= 90
    assert colour in ["green", "white"]
    assert type(below) is bool

    # size for center point and penalty points
    size_point = 0.5

    field_colour = "rgba(0,255,112,1)" if colour == "green" else "white"

    if line_colour is None:
        line_colour = "white" if colour == "green" else "black"

    # set the overall layout of the field
    layout = go.Layout(
        # make sure the field is green
        plot_bgcolor=field_colour,
        xaxis=dict(
            range=[-5, len_field + 5],
            zeroline=False,
            showgrid=False,
            showticklabels=False,
        ),
        yaxis=dict(
            range=[-5, wid_field + 5],
            zeroline=False,
            showgrid=False,
            showticklabels=False,
        ),
    )

    # create an empty figure for which only the layout is set
    fig = go.Figure(layout=layout)

    # add the halfway line
    ######################
    fig.add_shape(
        dict(
            type="line",
            x0=len_field / 2,
            y0=0,
            x1=len_field / 2,
            y1=wid_field,
            line=dict(color=line_colour, width=2),
        )
    )

    # add left penalty area
    ########################
    y_box = (wid_field - 40.32) / 2
    x_vals = [0, 16, 16, 0]
    y_vals = [wid_field - y_box, wid_field - y_box, y_box, y_box]

    for i in range(len(x_vals) - 1):
        fig.add_shape(
            # Line Vertical
            dict(
                type="line",
                x0=x_vals[i],
                y0=y_vals[i],
                x1=x_vals[i + 1],
                y1=y_vals[i + 1],
                line=dict(color=line_colour, width=2),
            )
        )

    # add left goal area
    ####################
    y_small_box = 7.32 / 2 + 5.5
    x_vals = [0, 5.5, 5.5, 0]
    y_vals = [
        wid_field / 2 - y_small_box,
        wid_field / 2 - y_small_box,
        wid_field / 2 + y_small_box,
        wid_field / 2 + y_small_box,
    ]

    for i in range(len(x_vals) - 1):
        fig.add_shape(
            # Line Vertical
            dict(
                type="line",
                x0=x_vals[i],
                y0=y_vals[i],
                x1=x_vals[i + 1],
                y1=y_vals[i + 1],
                line=dict(color=line_colour, width=2),
            )
        )

    # add right penalty area
    ########################
    x_vals = [len_field, len_field - 16, len_field - 16, len_field]
    y_vals = [wid_field - y_box, wid_field - y_box, y_box, y_box]

    for i in range(len(x_vals) - 1):
        fig.add_shape(
            # Line Vertical
            dict(
                type="line",
                x0=x_vals[i],
                y0=y_vals[i],
                x1=x_vals[i + 1],
                y1=y_vals[i + 1],
                line=dict(color=line_colour, width=2),
            )
        )

    # add right goal area
    #####################
    y_small_box = 7.32 / 2 + 5.5
    x_vals = [len_field, len_field - 5.5, len_field - 5.5, len_field]
    y_vals = [
        wid_field / 2 - y_small_box,
        wid_field / 2 - y_small_box,
        wid_field / 2 + y_small_box,
        wid_field / 2 + y_small_box,
    ]

    for i in range(len(x_vals) - 1):
        fig.add_shape(
            # Line Vertical
            dict(
                type="line",
                x0=x_vals[i],
                y0=y_vals[i],
                x1=x_vals[i + 1],
                y1=y_vals[i + 1],
                line=dict(color=line_colour, width=2),
            )
        )

    # add left penalty point
    ########################
    pen_point = (11, wid_field / 2)
    x_vals = [pen_point[0] - size_point, pen_point[0] + size_point]
    y_vals = [pen_point[1] - size_point, pen_point[1] + size_point]

    fig.add_shape(
        # unfilled circle
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=x_vals[0],
            y0=y_vals[0],
            x1=x_vals[1],
            y1=y_vals[1],
            line_color=line_colour,
            fillcolor=line_colour,
        )
    )

    # add right penalty point
    #########################
    pen_point = (len_field - 11, wid_field / 2)
    x_vals = [pen_point[0] - size_point, pen_point[0] + size_point]
    y_vals = [pen_point[1] - size_point, pen_point[1] + size_point]

    fig.add_shape(
        # unfilled circle
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=x_vals[0],
            y0=y_vals[0],
            x1=x_vals[1],
            y1=y_vals[1],
            line_color=line_colour,
            fillcolor=line_colour,
        )
    )

    # add center spot
    #################
    pen_point = (len_field / 2, wid_field / 2)
    x_vals = [pen_point[0] - size_point, pen_point[0] + size_point]
    y_vals = [pen_point[1] - size_point, pen_point[1] + size_point]

    fig.add_shape(
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=x_vals[0],
            y0=y_vals[0],
            x1=x_vals[1],
            y1=y_vals[1],
            line_color=line_colour,
            fillcolor=line_colour,
        )
    )

    # add center circle
    ###################

    # radius of the center circle (in meters)
    rad_circle = 9.15

    circle_y = wid_field / 2 - rad_circle
    circle_x = len_field / 2 - rad_circle

    fig.add_shape(
        dict(
            type="circle",
            xref="x",
            yref="y",
            x0=circle_x,
            y0=circle_y,
            x1=len_field - circle_x,
            y1=wid_field - circle_y,
            line_color=line_colour,
        )
    )

    # add outer lines
    ###################

    fig.add_shape(
        dict(
            type="line",
            x0=0,
            y0=0,
            x1=len_field,
            y1=0,
            line=dict(color=line_colour, width=2),
        )
    )

    # add the out lines
    fig.add_shape(
        dict(
            type="line",
            x0=0,
            y0=0,
            x1=0,
            y1=wid_field,
            line=dict(color=line_colour, width=2),
        )
    )

    # add the out lines
    fig.add_shape(
        dict(
            type="line",
            x0=0,
            y0=wid_field,
            x1=len_field,
            y1=wid_field,
            line=dict(color=line_colour, width=2),
        )
    )

    # add the out lines
    fig.add_shape(
        dict(
            type="line",
            x0=len_field,
            y0=0,
            x1=len_field,
            y1=wid_field,
            line=dict(color=line_colour, width=2),
        )
    )

    # add goals
    ###########

    goal_width = 7.32

    # left goal
    fig.add_shape(
        dict(
            type="line",
            x0=0,
            y0=(wid_field - goal_width) / 2,
            x1=-2,
            y1=(wid_field - goal_width) / 2,
            line=dict(color=line_colour, width=2),
        )
    )

    fig.add_shape(
        dict(
            type="line",
            x0=0,
            y0=(wid_field + goal_width) / 2,
            x1=-2,
            y1=(wid_field + goal_width) / 2,
            line=dict(color=line_colour, width=2),
        )
    )

    fig.add_shape(
        dict(
            type="line",
            x0=-2,
            y0=(wid_field - goal_width) / 2,
            x1=-2,
            y1=(wid_field + goal_width) / 2,
            line=dict(color=line_colour, width=2),
        )
    )

    # right goal
    fig.add_shape(
        dict(
            type="line",
            x0=len_field,
            y0=(wid_field - goal_width) / 2,
            x1=len_field + 2,
            y1=(wid_field - goal_width) / 2,
            line=dict(color=line_colour, width=2),
        )
    )

    fig.add_shape(
        dict(
            type="line",
            x0=len_field,
            y0=(wid_field + goal_width) / 2,
            x1=len_field + 2,
            y1=(wid_field + goal_width) / 2,
            line=dict(color=line_colour, width=2),
        )
    )

    fig.add_shape(
        dict(
            type="line",
            x0=len_field + 2,
            y0=(wid_field - goal_width) / 2,
            x1=len_field + 2,
            y1=(wid_field + goal_width) / 2,
            line=dict(color=line_colour, width=2),
        )
    )

    # configure the layout such that additional traces overlay the field
    if below:
        for shape in fig.layout["shapes"]:
            shape["layer"] = "below"

    # update the layout such that the field looks symmetrical
    fig.update_layout(
        autosize=False, width=len_field * 8 * size, height=wid_field * 9 * size
    )

    return fig


def _build_hover_text(row, dict_info):
    """
    Helper function to build the hover text
    """
    text = ""
    for key in dict_info.keys():
        if "display_type" in dict_info[key]:
            text += "{}: {:^{display_type}}<br />".format(
                key,
                row[dict_info[key]["values"]],
                display_type=dict_info[key]["display_type"],
            )
        else:
            text += "{}: {}<br />".format(key, row[dict_info[key]["values"]])
    return text