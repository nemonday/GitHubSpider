import re

url = 'https://github.com/icai/vue2-calendar/stargazers'

data = re.search(r'https://github.com/(.*)/(.*)/stargazers', url).group(2)

print(data)
