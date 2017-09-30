from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json, csv, numpy

analyzer = SentimentIntensityAnalyzer()

with open('emd.json') as fp:
    data = json.load(fp)

    print(len(data))

    for comment in data:
        vs = analyzer.polarity_scores(comment['content'])
        comment['polarity'] = vs

    source_agg = dict()
    for edge in data:
        if (edge['author']['author'], edge['author']['level']) in source_agg:
            source_agg[(edge['author']['author'], edge['author']['level'])].append(edge['polarity']['compound'])
        else:
            source_agg[(edge['author']['author'], edge['author']['level'])] = [edge['polarity']['compound']]


    out_source = []
    for key in source_agg:
        out_source.append([key[0], key[1], len(source_agg[key]), numpy.mean(source_agg[key])])

    with open('authors.tsv', 'w+') as sif:
        spamwriter = csv.writer(sif, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for edge in out_source:

            spamwriter.writerow(edge)

