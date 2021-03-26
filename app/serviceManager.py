import time
import datetime
import ast
from datetime import date
from dbManager import get_entries_date_range, get_entries_from_date
from eeManager import Encryptor, load_public_key, encode_base64_key_and_data, encode_base64
# USED TO DEMO DECRYPTION
from app.eeManager import Decryptor, load_private_key, decode_base64_key_and_data

a = '2021-1-10'
b = '2021-3-21'
the_key = load_public_key('secrets/public_key.pem')
the_secret = load_private_key('secrets/private_key.pem')
max_day_range = 60


def date_compare(date1, date2):
    """
    Support function for execute()
    :param date1: start date format '%Y-%m-%d'
    :param date2: stop date format '%Y-%m-%d'
    :return: difference between the two dates in days.
    """
    alpha = time.strptime(date1, "%Y-%m-%d")
    omega = time.strptime(date2, "%Y-%m-%d")
    f_date = date(alpha.tm_year, alpha.tm_mon, alpha.tm_mday)
    l_date = date(omega.tm_year, omega.tm_mon, omega.tm_mday)
    delta = l_date - f_date
    return delta.days


def execute(_start_time, _stop_time, public_key=None):
    """
    Function that fetches data entries from database. If public_key is provided data is encrypted and then encoded.
    If no key is provided the data is only encoded.
    :param _start_time: start date format '%Y-%m-%d'
    :param _stop_time: stop date format '%Y-%m-%d'
    :param public_key:
    :return: encoded data.
    """
    today = date.today()

    # CHECK IF START DATE IS IN THE FUTURE
    if date_compare(_start_time, today.strftime('%Y-%m-%d')) <= 0:
        start_time = today.strftime('%Y-%m-%d')
    else:
        start_time = _start_time

    # CHECK IF STOP DATE IS IN THE FUTURE
    if date_compare(_stop_time, today.strftime('%Y-%m-%d')) <= 0:
        stop_time = today.strftime('%Y-%m-%d')
    else:
        stop_time = _stop_time

    # FETCH DATA FROM DB
    # CHECK IF START DATE IS BEFORE STOP DATE
    if date_compare(start_time, stop_time) <= 0:
        data = get_entries_from_date(stop_time)

    else:
        alpha = time.strptime(start_time, "%Y-%m-%d")
        omega = time.strptime(stop_time, "%Y-%m-%d")
        f_date = date(alpha.tm_year, alpha.tm_mon, alpha.tm_mday)
        l_date = date(omega.tm_year, omega.tm_mon, omega.tm_mday)
        delta = l_date - f_date

        # CHECK IF RANGE IS OUTSIDE SCOPE
        if delta.days > max_day_range:
            new_start_time = l_date - datetime.timedelta(max_day_range)
            data = get_entries_date_range(new_start_time, stop_time)
        
        else:
            data = get_entries_date_range(start_time, stop_time)

    # ENCRYPTION & ENCODING
    if public_key is not None:
        bytes_data = bytes(str(data), 'utf-8')
        encryptor = Encryptor(bytes_data, public_key)
        data = encode_base64_key_and_data(*encryptor.return_key_and_data())

    # ENCODING
    else:
        data = encode_base64(data)

    return data


if __name__ == "__main__":
    gogo = execute(a, b, the_key)
    # gogo = execute(a, b)
    print(gogo)
    print('------------------------------')

    sym_key, data = decode_base64_key_and_data(gogo)
    decryptor = Decryptor(data, sym_key, the_secret)
    x, y = decryptor.return_key_and_data()
    res = ast.literal_eval(y.decode('utf-8'))
    print(res)

    # print(decode_base64(gogo))
