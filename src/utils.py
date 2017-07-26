from aiohttp import ClientSession

from bs4 import BeautifulSoup


class Record:
    def __init__(self, fake=None, name=None, priority=None, score=None, originals=None, real=None, details=None):
        self.fake = fake
        self.name = name
        self.priority = priority
        self.score = score
        self.originals = originals
        self.real = real
        self.details = details

    def __str__(self):
        return self.name


async def prepare(url):
    print("Not cached!")
    headers = {'Accept-Encoding': 'utf-8'}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            response = await resp.text()

            soup = BeautifulSoup(response, 'html.parser')
            return soup


def process(soup):
    try:
        table = soup.find_all('table')[3]
    except IndexError:
        table = soup.find_all('table')[1]

    tbody = table.find('tbody')

    priority = 9

    data = []

    title = str(soup.find(class_="title-description").parent)
    stats = str(soup.find(id='shortstat'))

    try:
        rows = tbody.find_all('tr')
    except AttributeError:
        table = soup.find_all('table')[2]
        tbody = table.find('tbody')
        thead = table.find('thead')
        rows = tbody.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols) == 6:
            pos = cols[0]
            name = cols[1]
            prior = cols[2]
            score = cols[3]
            details = cols[4]
            orig = cols[5]
        else:
            pos = cols[0]
            name = cols[1]
            prior = cols[2]
            score = cols[3]
            orig = cols[4]
            details = "-"
        try:
            p = int(cols[2])
        except ValueError:
            data.append(Record(fake=pos, name=name, priority=prior, score=score, originals=orig, details=details))
            continue

        if p <= priority:
            data.append(Record(fake=pos, name=name, priority=prior, score=score, originals=orig, details=details))

    counter = 1
    n_data = []
    priorities = list(range(1, priority + 1))
    for p in priorities:
        for entry in data:
            try:
                p1 = int(entry.priority)
            except ValueError:
                entry.real = counter
                n_data.append(entry)
                data.remove(entry)
                counter += 1
                continue
            if p == p1:
                entry.real = counter
                n_data.append(entry)
                counter += 1

    return n_data, title, stats

async def get_rating(url=None):
    data = await prepare(url=url)
    data = process(data)
    return data
