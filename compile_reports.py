import jinja2
import pandas as pd
import bokeh
import markdown2
from jinja2 import Environment, FileSystemLoader
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from datetime import date
from random import randint
from bokeh.models import ColumnDataSource
from generate_summary import get_result


def get_bokeh_component():
    plot = figure()
    plot.circle([1,2], [3,4])

    script, div = components(plot)

    data = dict(
        dates=[date(2014, 3, i + 1) for i in range(10)],
        downloads=[randint(0, 100) for i in range(10)],
    )
    source = ColumnDataSource(data)

    columns = [
        TableColumn(field="dates", title="Date", formatter=DateFormatter()),
        TableColumn(field="downloads", title="Downloads"),
    ]

    data_table = DataTable(source=source, columns=columns, width=400, height=280)

    script2, div2 = components(data_table)
    return script+script2, div, div2


def get_variable(config):
    from bokeh.embed import components
    name, rank, df, decade_df = get_result(config.gender, config.decade, config.name)
    if config.name <> name:
        message = "%s not found. Do you mean %s?" % (config.name, name)
    else:
        message =""

    birth_table = df.pivot(index='Decade', columns='Name', values='Births').fillna(0).to_html()
    rank_table = df.pivot(index='Decade', columns='Name', values='Rank').fillna(0).to_html()
    result_table = df[df['Rank']==rank][['Decade','Name','Rank']].sort('Decade').to_html(index=False)
    top_table = decade_df[(decade_df['Rank']<=8) &
                          (decade_df['Decade']==config.decade)].sort('Rank').to_html(index=False)
    from bokeh.charts import Line, save, output_file, ColumnDataSource
    from bokeh.resources import INLINE
    plot_path = "%s_%s_%i.html" % (config.name,config.gender,config.decade)
    output_file("output/" + plot_path, mode='inline')
    tooltips = [(c, '@' + c) for c in df.columns]
    p = Line(df, x='Decade', y='Rank', title="Rank across Time", color='Name',
             xlabel="Decade", ylabel="Rank",
             tooltips=tooltips)
    p.circle('Decade', 'Rank', color='gray', alpha=0.5, source=ColumnDataSource(df))
    save(p)

    #script, div = components(p)
    return {
            'plot_path': plot_path,
            'result_table': result_table,
            'rank_table': rank_table,
            'birth_table': birth_table,
            'top_table': top_table,
            'rank': rank,
            'config': config,
            'name': name,
            'message': message
            }

import collections
Config = collections.namedtuple('BirthConfig', 'name decade gender')

configs = [Config('Chris',1980,'M'),
           #Config('Wes', 1980, 'M'),
           #Config('John', 1980, 'M'),
           ]

results = [get_variable(i) for i in configs]


# Load jinja2 template environment
env = Environment(loader=FileSystemLoader('templates/'))
env.filters['markdown'] = lambda text: (markdown2.markdown(text))

script, div, div2 = get_bokeh_component()
df = pd.DataFrame({'a':[1,2,3], 'b':[3,4,5]})
templateVars = {
                "names_data": pd.read_csv("./data/names_cleaned.csv").head().to_html(),
                "names_by_decade": pd.read_csv("./data/names_by_decade.csv").head().to_html(),
                "results": results,
                "title_variable":'This title is inserted by Jinja2 template.',
                "rank": results[0]['rank'],
                "result_table": results[0]['result_table'],
                "plot_path": results[0]['plot_path']
               }

template = env.get_template('content.j2')

parsed_result = template.render(templateVars)

import io

with io.open("output/presentation.html", "w", encoding='utf-8') as fh:
    fh.write(parsed_result)