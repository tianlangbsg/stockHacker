import tushare as ts
import pyecharts.options as opts
from pyecharts.charts import Bar, Line
dw = ts.get_k_data('603515')
df = dw[-30:]
x_data = df['date'].values
bar = (
    Bar()
    .add_xaxis(list(x_data))
    .add_yaxis("开", list(df['open'].values),label_opts=opts.LabelOpts(is_show=False))
    .add_yaxis("收", list(df['close'].values),label_opts=opts.LabelOpts(is_show=False))
)
#bar.render_notebook()
line = (
    Line()
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="高",
        #线上不显示数值
        label_opts=opts.LabelOpts(is_show=False),
        y_axis=df['high'].values,
    )
    .add_yaxis(
        series_name="低",
        label_opts=opts.LabelOpts(is_show=False),
        #是否显示阴影
        #areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        y_axis=df['low'].values,
    )
    .set_global_opts(
    tooltip_opts=opts.TooltipOpts(
        is_show=True, trigger="axis", axis_pointer_type="cross"
    ),
    yaxis_opts=opts.AxisOpts(
        type_="value",
        axistick_opts=opts.AxisTickOpts(is_show=True),
        splitline_opts=opts.SplitLineOpts(is_show=True),
    ),
    xaxis_opts=opts.AxisOpts(
        type_="category",
        boundary_gap=False,
        axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
    ),
  )
)
#line.render_notebook()
bar.overlap(line).render_notebook()