import pandas as pd
import jellyfish


def get_result(gender_filter='M',decade_filter = 1980,target_name = 'Chris'):
    # input decade
    # input gender
    # input target name
    # return rank of the name, same rank names across year
    names_by_decade = pd.read_csv('./data/names_by_decade.csv')


    def get_target_name(target_name):
        df = names_by_decade['Rank'][(names_by_decade['Gender']==gender_filter) &
                                                   (names_by_decade['Name']==target_name) &
                                                   (names_by_decade['Decade']==decade_filter)]
        if len(df):
            target_name_rank = df.iloc[0]
            return target_name_rank, target_name
        else:
            # if no names are similar, return a similar name
            df = names_by_decade[(names_by_decade['Gender'] == gender_filter) &
                                 (names_by_decade['Decade'] == decade_filter)].copy()
            df['distance'] = df['Name'].map(lambda x: jellyfish.levenshtein_distance(unicode(x), unicode(target_name)))
            new_target_name = df['Name'][df['distance']==min(df['distance'])].iloc[0]
            if target_name <> new_target_name:
                print("%s not found.  Using %s instead" % (target_name, new_target_name))
            return get_target_name(new_target_name)

    target_name_rank, target_name = get_target_name(target_name)
    names_list = set(names_by_decade[(names_by_decade['Gender']==gender_filter) &
                                           (names_by_decade['Rank']==target_name_rank) &
                                     (names_by_decade['Decade']>=decade_filter)
                     ].Name)

    return (target_name, target_name_rank,
            names_by_decade[names_by_decade.Name.isin(names_list) &
                            (names_by_decade.Gender == gender_filter) &
                            (names_by_decade['Decade'] >= decade_filter)],
            names_by_decade[(names_by_decade.Gender == gender_filter) &
                            (names_by_decade['Decade'] >= decade_filter)],
            )




if __name__=='__main__':
    # Example
    rank, df = get_result()

    from bokeh.plotting import figure, show, output_file, ColumnDataSource
    from bokeh.models import HoverTool
    output_file('output/plot.html')
    hover = HoverTool(
        tooltips=[
        ("Series", "@series_name"),
        ("Date", "@Name"),
        ("Value", "@Decade"),
    ]
    )
    p = figure(tools=[hover])
    p.circle('Decade','Rank', color='Name', source=ColumnDataSource(df))
    show(p)
