from bs4 import BeautifulSoup
import requests
import sqlite3
import threading

debug = False


def log(info, error):
    if debug:
        print(info)
        print(error)


def gethtml(url):
    proxies = {
        "http": "127.0.0.1:7890",
        "https": "127.0.0.1:7890"
    }
    r = requests.get(url, proxies=proxies)
    return r.text


def savedata(conf, year, cat, title, href):
    conn = sqlite3.connect("./paper.db")
    c = conn.cursor()
    query = "INSERT INTO PAPER (CONFERENCE,\"YEAR\",CAT,TITLE,HREF) " \
            "VALUES ('{conf}','{year}','{cat}','{title}','{href}');"
    title = title.replace('\'', '\'\'')
    cat = cat.replace('\'', '\'\'')
    cat = cat.split("\n")[-1]
    query = query.format(conf=conf, year=year, cat=cat, title=title, href=href)
    try:
        c.execute(query)
        conn.commit()
    except sqlite3.OperationalError as e:
        log("[*] QUERY ERROR:" + query, e)
    except sqlite3.IntegrityError as e:
        log("[*] Duplicate found:" + query, e)
    conn.close()


def readdata(id):
    conn = sqlite3.connect("./paper.db")
    c = conn.cursor()
    query = "SELECT * FROM PAPER WHERE ID=" + str(int(id))
    try:
        cursor = c.execute(query).fetchone()
        conn.close()
        return cursor
    except sqlite3.OperationalError as e:
        log("[*] QUERY ERROR:" + query, e)
    except sqlite3.IntegrityError as e:
        log("[*] Duplicate found:" + query, e)
    conn.close()


def updatedata(id, abstract):
    conn = sqlite3.connect("./paper.db")
    c = conn.cursor()
    query = "UPDATE PAPER set ABSTRACT = '" + abstract + "' WHERE ID = " + str(int(id))
    print(query)
    try:
        print(c.execute(query))
        conn.commit()
    except sqlite3.OperationalError as e:
        log("[*] QUERY ERROR:" + query, e)
    except sqlite3.IntegrityError as e:
        log("[*] Duplicate found:" + query, e)
    conn.close()


def getresult(html, conference, year):
    soup = BeautifulSoup(html, 'html.parser')
    contents = soup.find('div', class_='clear-both')
    current_section = conference
    for s in contents.next_siblings:
        if s.name == "ul":
            for article in s.children:
                title = article.cite.find('span', class_='title').text
                link = article.nav.ul.li.div.a['href']
                print("[", current_section, "]", title, link)
                savedata(conference, year, current_section, title, link)
            current_section = ""
        elif s.name == "header":
            current_section = s.text.replace('\n', '')


def getabstract(id, html):
    # print(id, html)
    soup = BeautifulSoup(html, 'html.parser')
    # 处理ccs（ACM系列）
    try:
        content = soup.find('div', class_='abstractSection')
        abstract = ""
        for child in content.contents:
            if child == '\n' or child == ' ':
                pass
            else:
                try:
                    p = child.string.split("\n")
                except:
                    p = child.text.split("\n")
                for line in p:
                    abstract += line.strip()
                abstract += "\n"
        return abstract
    except AttributeError:
        pass
    # 处理sp（IEEE系列）
    try:
        abstract = soup.find('meta', attrs={"property": "twitter:description"})['content']
        return abstract
    except TypeError:
        pass
    # 处理uss
    try:
        abstract = soup.find('div', class_='field-name-field-paper-description').text
        return abstract
    except AttributeError:
        pass
    # 处理ndss
    try:
        abstract = list(soup.find('div', class_='entry-content'))[3].text
        return abstract
    except TypeError:
        pass

    # 处理ndss2017
    try:
        return list(soup.find('main', class_="main"))[-2].text
    except TypeError:
        pass



def conf(conference_dict, years):
    baseurl = "https://dblp.uni-trier.de/db/conf/"
    for year in years:
        for cname in conference_dict:
            for conference in conference_dict[cname]:
                url = baseurl + cname + '/' + conference + str(year) + '.html'
                print("[*]", cname, '-', conference, year, url)
                rawHTML = gethtml(url)
                getresult(rawHTML, conference, year)


def journal(journal_dict, volumes):
    baseurl = "https://dblp.uni-trier.de/db/journals/"
    for volume in volumes:
        for cname in journal_dict:
            for journal in journal_dict[cname]:
                url = baseurl + cname + '/' + journal + str(volume) + '.html'
                print("[*]", cname, '-', journal, volume, url)
                rawHTML = gethtml(url)
                getresult(rawHTML, journal, volume)


def update_abstract(id):
    print("Updating Abstract", id)
    abstract = getabstract(id, gethtml(readdata(id)[5]))
    if abstract:
        updatedata(id, abstract.replace("'", "''"))
    else:
        print("[E] Abstract is null.")


def ndss2018():
    html = gethtml("https://www.ndss-symposium.org/ndss2018/programme/")
    soup = BeautifulSoup(html, "html.parser")
    abstract = soup.find_all('tbody')[-1].find_all('div', class_='modal-body')
    title = soup.find_all('tbody')[-1].find_all('p', class_='')

    conn = sqlite3.connect("./paper.db")
    c = conn.cursor()

    for i in range(len(title)):
        t = title[i].find('b').text.strip().replace('\'', '\\\'')
        a = abstract[i].text
        query = "UPDATE PAPER set ABSTRACT = '" + a + "' WHERE ID = " + str(5151+i)
        c.execute(query)
        print("Update No", 5151+i)
    conn.commit()
    conn.close()


def ndss2016():
    html = gethtml("https://www.ndss-symposium.org/ndss2016/ndss-2016-programme/")
    soup = BeautifulSoup(html, "html.parser")
    t = soup.find('h3')
    title = ""
    abstract = []

    conn = sqlite3.connect("./paper.db")
    c = conn.cursor()

    while t is not None:
        if t.find('em') is not None and t.find('em') != -1:
            title += "."
            title = title.replace(" ", "")
            title = title.replace("’", "'")
            title = title.replace("'", "''")
            title = title.strip('\n')
            print("[T] ", title)
            abstract = '\\n'.join(abstract)
            print("[A] ", abstract)
            query = "UPDATE PAPER set ABSTRACT = '" + abstract + "' WHERE TITLE = '" + title + "'"
            print(query)
            c.execute(query)

            title = ""
            abstract = []
            t = t.next_sibling
        if t == '\n' or (t.find('a') and t.find('a').text == 'Slides'):
            t = t.next_sibling
        else:
            if t.name == 'h3':
                title = t.text
            if t.name == 'p' and title:
                abstract.append(t.text)
            t = t.next_sibling

    conn.commit()
    conn.close()




class myThread(threading.Thread):
    def __init__(self, threadID, id):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.id = id

    def run(self):
        update_abstract(self.id)


if __name__ == "__main__":
    conference_dict = {
        # "ccs": ["ccs"],
        # "sp": ["sp", "spw"],
        # "uss": ["uss", "cset", "foci"],
        # "acsac": ["acsac"],
        "ndss": ["ndss"]
    }
    years = [2021]
    # conf(conference_dict, years)

    # journal_dict = {
    #     "tdsc": ["tdsc"],
    #     # "tifs": ["tifs"]
    # }
    # volumes = [18, 17, 16, 15, 14, 13]
    # journal(journal_dict, volumes)

    # ids = [1535, 1536, 1538, 1543, 1550, 1551, 1552, 1556, 1563, 1566, 1567, 1568, 1571, 1572, 1577, 1579, 1583,
    # 1584, 1586, 1588, 1593, 1595, 1602, 1606, 1609, 1610, 1611, 1612, 1616, 1617, 1618, 1619, 1620, 1625, 1630,
    # 1633, 1635, 1637, 1643, 1645, 1646, 1648, 1661, 1662, 1663, 1673, 1674, 1675, 1677, 1686, 1739, 1800, 1834,
    # 1920, 1930, 1941, 1988, 2014, 2034, 2035, 2045, 2046, 2049, 2052, 2057, 2058, 2059, 2060, 2090, 2094, 2101,
    # 2103, 2105, 2114, 2117, 2128, 2139, 2190, 2208, 2264, 2306, 2379, 2386, 2394, 2417, 2445, 2446, 2455, 2456,
    # 2460, 2464, 2465, 2466, 2467, 2470, 2473, 2476, 2483, 2492, 2496, 2502, 2504, 2508, 2536, 2546, 2548, 2555,
    # 2556, 2558, 2563, 2566, 2573, 2590, 2593, 2594, 2609, 2611, 2613, 2636, 2642, 2643, 2661, 2665, 2672, 2681,
    # 2682, 2686, 2696, 2701, 2707, 2709, 2714, 2718, 2725, 2746, 2749, 2751, 2771, 2775, 2780, 2786, 2793, 2800,
    # 2803, 2806, 2813, 2815, 2817, 2818, 2827, 2830, 2840, 2842, 2852, 2857, 2862, 2863, 2866, 2879, 2884, 2896,
    # 2903, 2911, 2912, 2915, 2916, 2917, 2920, 2928, 2933, 2937, 2942, 2958, 2966, 2976, 2978, 2991, 2995, 2997,
    # 3001, 3008, 3011, 3025, 3026, 3028, 3031, 3034, 3037, 3038]
    #
    # for pid in range(5643, 5732):
    #     update_abstract(pid)
    # update_abstract(5290)

    # ids = [4254]
    # location = 0
    # while location < 4969:
    #     t_list = []
    #     for i in range(10):
    #         t_list.append(myThread(i, ids[location]))
    #         location += 1
    #     for t in t_list:
    #         t.start()
    #     for t in t_list:
    #         t.join()

    # ndss2016()