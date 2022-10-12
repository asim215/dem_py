import json

users = {
    1000: {
        'username': 'Елизар',
        'email': 'test@lalala.ru',
        'address': {
            'index': 1000,
            'city': 'Moscow',
            'street': 'Lubyanka',
            'house': '10a',
            'flat': '4',
        },
        'orders': {
            10: {
                'date': '2022-10-10',
                'price': 1000,
            }
        }
    },
    1001: {
        'username': 'Dmitry',
        'email': 'test@lalala.ru',
        'address': {
            'index': 1000,
            'city': 'Moscow',
            'street': 'Lubyanka',
            'house': '10b'
        }
    },
    1003: {
        'username': 'Anton',
        'email': 'test@lalala.ru',
        'address': {
            'index': 1000,
            'city': 'Moscow',
            'street': 'Lubyanka',
            'house': '10a',
            'flat': '4',
        },
        'orders': {
            11: {
                'date': '2022-10-12',
                'price': 1500,
            },
            12: {
                'date': '2022-10-15',
                'price': 500,
            },
        }
    },
    3000: {

    }
}


def print_users(users):
    for i in users:
        print('id:', i, '\tname:', users[i].get('username', "User has not a name"))


def get_address_by_user_id(users, id):
    address = users[id].get('address', {"city": "Unknown"})
    return f"{address.get('index', '000000')}, г. {address.get('city', 'Unknown')} " \
           f"{'ул. ' + address['street'] if 'street' in address else ''} " \
           f"{'д. ' + address['house'] if 'house' in address else ''} " \
           f"{'кв. ' + address['flat'] if 'flat' in address else ''} "


def add_order_to_user_by_id(users, user_id, order_id, order_date, order_price):
    user = users[user_id]
    if 'orders' not in user:
        user['orders'] = {}

    user['orders'][order_id] = {
        'date': order_date,
        'price': order_price
    }


def to_json(users) -> str:
    return json.dumps(users, ensure_ascii=False)

def from_json(str) -> dict:
    return json.loads(str)

print_users(users)

for i in users:
    print(i, "address: ", get_address_by_user_id(users, i))

add_order_to_user_by_id(users, 3000, 100, '2022-12-15', 7000)

print(to_json(users))