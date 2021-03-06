import json

kp = """
[
{"id":"30000","kp":"30000-Palembang"},
{"id":"31100","kp":"31100-Prabumulih"},
{"id":"31300","kp":"31300-Muara Enim"},
{"id":"31400","kp":"31400-Lahat"},
{"id":"31600","kp":"31600-Lubuk Linggau"},
{"id":"32100","kp":"32100-Baturaja"},
{"id":"33100","kp":"33100-Pangkal Pinang"},
{"id":"33400","kp":"33400-Tanjung Pandan"},
{"id":"34100","kp":"34100-Metro"},
{"id":"34500","kp":"34500-Kota Bumi"},
{"id":"35000","kp":"35000-Bandar Lampung"},
{"id":"36000","kp":"36000-Jambi"},
{"id":"37100","kp":"37100-Sungai Penuh"},
{"id":"37200","kp":"37200-Muara Bungo"},
{"id":"38000","kp":"38000-Bengkulu"},
{"id":"39000","kp":"39000-Curup"}
]
"""
import ast
import uuid
kp = kp.strip()
dc = ast.literal_eval(kp)
# print(dc)
ls = []
for row in dc:
    obj = {
        'model': 'website.kantorpos',
        'pk': str(uuid.uuid4()),
        'fields':
        {
            'kode': row['id'],
            'regional': '3',
            'nama': row['kp'].split('-')[1]
        }
    }
    ls.append(obj)
    
print(ls)
with open('kantorpos2.json', 'w') as outfile:
    json.dump(ls, outfile, indent=4)


