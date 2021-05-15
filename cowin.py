import requests
from datetime import date
import json
import logging


class cowin():
    def get_data(self, pincode):
        data = {}
        url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}'.format(pincode,
                                                                                                                     date.today().strftime("%d-%m-%Y"))
        headers = {
            'accept': 'application/json',
            'Accept-Language': 'en_IN',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0'
        }

        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            data = json.loads(str(r.content, encoding='utf-8'))['centers']
            logging.info(str(data))
        else:
            logging.error(r)
        return data

    def get_avail(self, data, all=False):
        if not data:
            logging.error('No data found')
            return []
        res = []
        compare = -1 if all else 0
        for center in data:
            for sess in center['sessions']:
                if sess['available_capacity'] > compare:
                    res.append([
                        sess.get('date'),
                        sess.get('available_capacity'),
                        sess.get('min_age_limit'),
                        sess.get('vaccine'),
                        #  center.get('address')
                        center.get('name')
                    ])
        logging.info(str(res))
        return res

    def format_data(self, data, all=False):
        avail = self.get_avail(data, all)
        if not avail:
            logging.error('No slots found')
            return ''
        table = "{:<12} {:<6} {:<4} {:<12} {:<15}".format(
            'Date', 'Avail', 'Age', 'Vaccine', 'Location')
        table += '\n' + '-'*60
        for a in avail:
            table += '\n' + \
                "{:<12} {:<6} {:<4} {:<12} {:<15}".format(
                    a[0], a[1], a[2], a[3], a[4])
        return table
