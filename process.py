

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

# %%
data = defaultdict(int)
for paper in date_data:
    for (name, val) in paper[0]:
        data[name] += val

data = list(data.items())
data = sorted(data, reverse=True, key=lambda x: x[1])
data = data 
# %%

old = content[51:1853]
# %%

try:
    count = 0
    for i, line in enumerate(old):
        if 'name' in line:
            name, value = data[count]
            old[i] =  template_name.format(name)
            old[i+1] = template_value.format(value)
            count += 1
except IndexError:
    pass

content = content[:51] + old + content[1853:]

# %%

with open('wordcloud.js', 'w', encoding='utf-8') as f:
    for line in content:
        f.write(line)


# %%