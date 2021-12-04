from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line

bar = (
    Bar()
    .add_xaxis(dateList)
    .add_yaxis(
        "收盘涨停数量",
        close_high_limit_count_list,
        yaxis_index=0,
        color="	#DC143C",
    )
    .add_yaxis(
        "盘中涨停数量",
        reach_high_limit_count_list,
        yaxis_index=1,
        color="#FF8C00",
    )
    .add_yaxis(
        "收盘跌停停数量",
        low_limit_count_list,
        yaxis_index=1,
        color="#228B22",
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="收盘涨停数量",
            type_="value",
            min_=0,
            max_=250,
            position="right",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#d14a61")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
        )
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            type_="value",
            name="温度",
            min_=0,
            max_=25,
            position="left",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#675bba")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            ),
        )
    )
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            name="盘中涨停数量",
            min_=0,
            max_=250,
            position="right",
            offset=80,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#5793f3")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
        ),
        title_opts=opts.TitleOpts(title="Grid-Overlap-多 X/Y 轴示例"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(pos_left="25%"),
    )
)

line = (
    Line()
    .add_xaxis(["{}月".format(i) for i in range(1, 13)])
    .add_yaxis(
        "涨停开盘涨幅",
        avg_limit_high_open_range_list,
        yaxis_index=2,
        color="#675bba",
        label_opts=opts.LabelOpts(is_show=False),
    )
)

overlap_1 = bar.overlap(line)

grid = (
    Grid(init_opts=opts.InitOpts(width="1200px", height="800px"))
    .add(
        overlap_1, grid_opts=opts.GridOpts(pos_right="58%"), is_control_axis_index=True
    ).render("涨停趋势分析.html")
)
