import pandas as pd
import numpy as np
import jellyfish

import argparse


## https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def levenshtein(source, target, reversed=False):
    if len(source) < len(target):
        return levenshtein(target, source, True)

    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)

    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = np.array(tuple(source))
    target = np.array(tuple(target))

    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = np.arange(target.size + 1)
    for s in source:
        # Insertion (target grows longer than source):
        if not reversed:
            current_row = previous_row + 1
        else:
            current_row = previous_row + 1

        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).
        current_row[1:] = np.minimum(
                current_row[1:],
                np.add(previous_row[:-1], target != s))

        # Deletion (target grows shorter than source):

        if not reversed:
            current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + 1)
        else:
            current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + 1 )

        previous_row = current_row

    return previous_row[-1]


gender_filter = 'F'
decade_filter = '2010s'
target_name = 'Charlotte'
popular_weight = 0.2
count_threshold = 10000


names_by_decade = pd.read_csv('./data/names_by_decade.csv')

filtered_names = names_by_decade

#if gender_filter is not None:
#    print("Filter Gender %s" % gender_filter)
filtered_names = filtered_names[filtered_names['Gender']==gender_filter]

#if decade_filter is not None:
filtered_names = filtered_names[filtered_names['Decade']==decade_filter]

filtered_names = filtered_names[filtered_names['Births']>=count_threshold]



filtered_names = filtered_names.copy()

filtered_names['Edit_Distance'] = filtered_names['Name'].map(lambda x: levenshtein(x.lower(), target_name.lower()))

f = jellyfish.match_rating_codex

filtered_names['Edit_Distance'] = filtered_names['Name'].map(lambda x: 1-jellyfish.jaro_winkler(
    unicode(f(unicode(x))),
    unicode(f(unicode(target_name)))))





x = filtered_names['Edit_Distance'].median()
y = filtered_names['Edit_Distance'].min()
filtered_names['Edit_Score'] = (filtered_names['Edit_Distance'])

filtered_names['Popular_Score'] = 1-np.sqrt(filtered_names['Births']) / np.sqrt(filtered_names['Births']).max()


filtered_names['Total_Score'] = filtered_names['Popular_Score'] * popular_weight + \
                                filtered_names['Edit_Score']

filtered_names.sort('Total_Score').head(30)



print jellyfish.match_rating_codex(u'WingSum')
print jellyfish.match_rating_codex(u'Megan')

levenshtein('Chris', 'Chriaaaa')


if __name__=='__main__':
    hello()