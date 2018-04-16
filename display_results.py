import json

with open('ordered_comment_ids.json') as data_file:
    ordered_comment_ids = json.load(data_file)

with open('snippets.json') as data_file:
    snippets = json.load(data_file)

print 'length: ' + str(len(ordered_comment_ids))

i = 0
for comment_id in ordered_comment_ids:
    print snippets[comment_id]['textOriginal'] + '\n'
    i = i + 1
    if i == 499:
        exit()