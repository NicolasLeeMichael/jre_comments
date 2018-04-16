# coding=utf-8
import glob
import hashlib
import json
import re
import dedupe
from unidecode import unidecode

fields = [
    {'field': 'processedComment', 'type': 'String'}
]


def matches_pattern(text):
    text = text.lower()
    return text.startswith(u'joe') and text.endswith(u'rogan')


def pre_process(feature):
    try:
        feature = feature.decode('utf-8')
    except Exception as e:
        pass
    feature = unidecode(feature)
    feature = re.sub(' +', ' ', feature)
    feature = re.sub('\n', ' ', feature)
    feature = re.sub('[“”\'\"()]', '', feature)
    feature = feature.lower().strip()
    return feature


def dedupe_snippets():

    deduper = dedupe.Dedupe(fields)
    deduper.sample(snippets, 15000)
    dedupe.consoleLabel(deduper)
    deduper.train()

    threshold = deduper.threshold(snippets, recall_weight=1)
    clustered_dupes = deduper.match(snippets, threshold)

    for (cluster_id, cluster) in enumerate(clustered_dupes):

        id_set, scores = cluster
        max_like_count = -1
        max_like_count_comment_id = ''

        for comment_id in id_set:

            like_count = snippets[comment_id]['likeCount']

            if like_count > max_like_count:

                snippets.pop(max_like_count_comment_id, None)
                max_like_count = like_count
                max_like_count_comment_id = comment_id

            else:
                snippets.pop(comment_id)


snippets = dict()

for filename in glob.glob('*.json'):
    j_comments = json.load(open(filename))

    for j_comment in j_comments['items']:
        snippet = j_comment['snippet']['topLevelComment']['snippet']

        if matches_pattern(snippet['textOriginal']):
            snippet_id = hashlib.md5(json.dumps(snippet)).hexdigest()
            processed_comment = pre_process(snippet['textOriginal'])
            snippet['processedComment'] = processed_comment
            snippets[snippet_id] = snippet

dedupe_snippets()
sorted_by_likes = []

for comment_id, snippet in snippets.iteritems():
    sorted_by_likes.append((comment_id, snippet['likeCount']))
sorted_by_likes = sorted(sorted_by_likes, key=lambda x: x[1], reverse=True)

ordered_comments_ids = []
for K, V in sorted_by_likes:
    ordered_comments_ids.append(K)

with open('ordered_comment_ids.json', 'w') as outfile:
    json.dump(ordered_comments_ids, outfile)

with open('snippets.json', 'w') as outfile:
    json.dump(snippets, outfile)






