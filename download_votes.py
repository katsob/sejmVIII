import lxml.html as lh
import requests
import os
import time
import pandas as pd
import sys



id_last = 51948
id_first = 43846

clubs = ['PiS', 'PO-KO', 'PO', 'PSL', 'PSL-KP', 'Kukiz15', 'Konfederacja', 'UPR', 'TERAZ!',
         'PP', 'WiS', 'niez.', 'N', 'PSL-UED', 'L-S', 'W-S']
path = 'data/votes.csv'

def func(id_last):
    for id in range(id_last, id_first, -1):
        try:
            if id % 10 == 0:
                print(id)
            poslowie = {}
            for cl in clubs:
                url = 'http://www.sejm.gov.pl/sejm8.nsf/agent.xsp?symbol=klubglos&IdGlosowania=%d&KodKlubu=%s&' % (id, cl)
                time.sleep(4)
                session = requests.Session()
                page = session.get(url)

                doc = lh.fromstring(page.content)
                tr_elements = doc.xpath('//tr')
                glosowanie = doc.xpath('/html/body/form/div/div[1]/div/div[2]/div[2]/h1')[0].text

                votes = {}
                for tr in tr_elements:
                    if len(tr) > 2:
                        col = tuple(map(lambda x: x.text.encode('raw_unicode_escape').decode('utf-8'), tr[1:3]))
                        votes[col[0]] = col[1]
                        try:
                            col = list(map(lambda x: x.text.encode('raw_unicode_escape').decode('utf-8'), tr[4:6]))
                            votes[col[0]] = col[1]
                        except IndexError:
                            pass
                            # print('ERROR. Klub %s %s' % (
                            #     klub, str(tuple(map(lambda x: x.text.encode('raw_unicode_escape').decode('utf-8'), tr)))))
                    else:
                        # print('KLUB %s NIE ISTNIEJE' % klub)
                        break

                a = votes.pop('Nazwisko i imię')
                if not len(a):
                    print('BLAD')
                poslowie.update(votes)

            if not len(poslowie) == 460:
                print('Liczba poslow: %d!! POMINIETY KLUB?????' % len(poslowie))
                print('SPRAWDZ GLOSOWANIE: %s' % glosowanie.encode('raw_unicode_escape').decode('utf-8'))

            if not os.path.exists(path):
                pd.DataFrame(poslowie, index=[id]).to_csv(path, index=True)
            else:
                new_votes = pd.Series(poslowie, name=id)
                df2 = pd.read_csv(path, index_col=0)
                df2 = df2.append(new_votes)
                df2.to_csv(path, index=True)
        except:
            return id



if __name__ == '__main__':
    vote_id = int(sys.argv[1])
    i = func(vote_id)
