from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json, csv, numpy

analyzer = SentimentIntensityAnalyzer()

with open('edges.json') as fp:
    data = json.load(fp)

    print(len(data))

    for comment in data:
        vs = analyzer.polarity_scores(comment['text'])
        comment['polarity'] = vs

    agg = dict()
    for edge in data:
        if (edge['source'], edge['target']) in agg:
            agg[(edge['source'], edge['target'])].append(edge['polarity']['compound'])
        else:
            agg[(edge['source'], edge['target'])] = [edge['polarity']['compound']]

    source_agg = dict()
    for edge in data:
        if edge['source'] in source_agg:
            source_agg[edge['source']].append(edge['polarity']['compound'])
        else:
            source_agg[edge['source']] = [edge['polarity']['compound']]


    out = []
    for key in agg:
        out.append([key[0], key[1], len(agg[key]), numpy.mean(agg[key])])

    out_source = []
    for key in source_agg:
        out_source.append([key, len(source_agg[key]), numpy.mean(source_agg[key])])

    with open('interactions.tsv', 'w+') as sif:
        spamwriter = csv.writer(sif, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for edge in out:

            spamwriter.writerow(edge)

    with open('sources.tsv', 'w+') as sif:
        spamwriter = csv.writer(sif, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for edge in out_source:

            spamwriter.writerow(edge)

