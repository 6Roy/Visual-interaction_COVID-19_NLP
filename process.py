

# %%
from collections import defaultdict

# %%

content = []
with open("templates/wordcloud.js", 'r') as f:
    for line in f.readlines():
        content.append(line)
# %%
template_name = '            "name": "{}",\n'
template_value = '            "value": {},\n'

content[53]

# %%
from myScripts.wordData import date_data

# %%

# settings

K = 200 # top-200

# %%
data = defaultdict(int)
for paper in date_data:
    for (name, val) in paper[0]:
        data[name] += val

data = list(data.items())
data = sorted(data, reverse=True, key=lambda x: x[1])
data = data[:K]
# %%

old = content[51:1853]
# %%

count = 0
for line in old:
    if 'name' in line:
        name, value = data[count]
        old[count] =  template_name.format(name)
        old[count+1] = template_value.format(value)

content = content[:51] + old + content[1853:]

# %%

with open('wordcloud.js', 'w') as f:
    for line in content:
        f.write(line)
