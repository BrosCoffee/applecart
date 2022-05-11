'''
Part 4:
Add instructions for running your program taking a Person ID as command-line argument and
print out the list of connected persons (First Last, one per line) to the console, assuming two text
files ‘persons.json’ and ‘contacts.json’ are found in the same directory. The program should
combine the rules from Parts 2 and 3 where two persons can be connected through either rule
or both.
'''

import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

person_f = open('./person.json')
person_objs = json.load(person_f)

contacts_f = open('./contacts.json')
contacts_objs = json.load(contacts_f)

def test_get_target():
    # get_target() uses global var person_objs
    assert get_target(9999) == (None, None, None)
    assert get_target(1) == ('1', '2121234567', [{"company": "BananaCart", "title": "Digital Media Manager", "start": "2020-01-01", "end": None }])
    assert get_target(4) == ('1', '7181234567', [])

def get_target(pk: int) -> tuple[str, str, list[dict]]: # '1', 2123458974', [{'company': 'OrangeCart', 'start': '2017-01-01', 'end': null}]
    '''
    Part 1:
    {
        "id": 0,
        "first": "Jane",
        "last": "Doe",
        "phone": "1-2123458974",
        "experience": [{
            "company": "OrangeCart",
            "title": "Director of Marketing",
            "start": "2017-01-01",
            "end": null
        }]
    }
    Notes:
    - “id” values are unique
    - the “phone” field may be null
    - when not null, “phone” is a normalized string containing country code and phone
    number, separated by a dash
    - “start” and “end” in an “experience” are normalized strings containing dates (null values
    for “end” mean the present)
    '''
    for obj in person_objs:
        if obj['id'] == int(pk):
            if obj['phone']:
                cty_code, phone = obj['phone'].split('-')[0], obj['phone'].split('-')[1]
            else:
                cty_code = phone = None
            assert phone == None or len(phone) == 10, f"phone expected a 10 digit number, got {len(phone)}"
            experience = obj['experience']
            return cty_code, phone, experience
            break
    return None, None, None

def test_check_company_period():
    exp1 = [{
        "company": "BananaCart",
        "title": "Digital Media Manager",
        "start": "2020-01-01",
        "end": None
    }]
    exp2 = [{
        "company": "BananaCart",
        "title": "Associate, Political Campaigns",
        "start": "2018-01-01",
        "end": None
    }]
    exp3 = [{
        "company": "Banana Co.",
        "title": "Associate",
        "start": "2021-01-01",
        "end": None
    }]
    exp4 = [{
        "company": "OrangeCart",
        "title": "Director of Marketing",
        "start": "2017-01-01",
        "end": "2018-12-31"
    },
    {
        "company": "Banana Co.",
        "title": "CEO",
        "start": "2018-02-01",
        "end": None
    }]
    exp5 = [{
        "company": "Banana Co.",
        "title": "Associate",
        "start": "2017-10-31",
        "end": "2018-04-30"
    }]
    exp6 = [{
        "company": "Banana Co.",
        "title": "Associate",
        "start": "2017-10-31",
        "end": None
    }]
    assert check_company_period(exp1, exp2) == True
    assert check_company_period(exp2, exp3) == False
    assert check_company_period(exp3, exp4) == True
    assert check_company_period(exp4, exp5) == False # less than 3 months
    assert check_company_period(exp5, exp6) == True # a little more less than 6 months

def check_company_period(exp1_ls: list[dict], exp2_ls: list[dict], month=6) -> bool: # Default 6 months
    '''
    Part 2:
    Write a function that takes a collection of Person records and a Person ID (that exists in the
    collection) and returns a list of “connected” Person IDs. Two Persons are connected if they
    worked for the same company and their timelines at the company overlap by at least six
    months.

    Check overlap scenarios:
    Case 1. no overlap (ignore):
     <---->
                <----->
    Case 2. overlap:
    Case 2-a:
    s1   e1
    <---->
       <----->
       s2    e2
    Case 2-b:
    s2   e2
    <---->
       <----->
       s1    e1
        2-a: s1 < s2 < e1 < e2
        2-b: s2 < s1 < e2 < e1
    Case 3. same start, diff end:
    <---->
    <----------->
    Case 4. diff period, same end: 
           <---->
    <----------->
    Case 5. same period: 
    <----------->
    <----------->  
    '''
    for exp1 in exp1_ls:
        for exp2 in exp2_ls:
            if exp1['company'] == exp2['company']: # same company
                exp1_start = datetime.strptime(exp1['start'], "%Y-%m-%d").date() # 2017-01-01 -> datetime.date(2017, 1, 1)
                exp1_end = datetime.strptime(exp1['end'], "%Y-%m-%d").date() if exp1['end'] else datetime.now().date()
                exp2_start = datetime.strptime(exp2['start'], "%Y-%m-%d").date()
                exp2_end = datetime.strptime(exp2['end'], "%Y-%m-%d").date() if exp2['end'] else datetime.now().date()
                # Case 5
                if exp1_start == exp2_start and exp1_end == exp2_end and exp1_start + relativedelta(months=month) <= exp1_end:
                    # print('case 5')
                    return True
                # Case 3
                elif exp1_start == exp2_start and exp1_end != exp2_end:
                    min_end = min(exp1_end, exp2_end)
                    # print('case 3')
                    if exp1_start + relativedelta(months=month) <= min_end:
                        return True
                # Case 4
                elif exp1_start != exp2_start and exp1_end == exp2_end:
                    max_start = max(exp1_start, exp2_start)
                    # print('case 4')
                    if max_start + relativedelta(months=month) <= exp1_end:
                        return True
                # Case 2
                elif exp1_start != exp2_start and exp1_end != exp2_end:
                    # Case 2-a
                    if exp1_start < exp2_start < exp1_end < exp2_end:
                        # print('case 2-a')
                        if exp2_start + relativedelta(months=month) <= exp1_end:
                            return True
                    # Case 2-b
                    elif exp2_start < exp1_start < exp2_end < exp1_end:
                        # print('case 2-b')
                        if exp1_start + relativedelta(months=month) <= exp2_end:
                            return True

    return False

def get_exp_connect(pk: int, exp: list[dict]) -> list[str]: # ['John Doe', 'Mary Jane']
    res = []
    for person_obj in person_objs:
        if pk != person_obj['id'] and check_company_period(exp, person_obj['experience']):
            res.append(person_obj['first'] + ' ' + person_obj['last'])
    return res

def test_clean_number():
    assert clean_number('+19173454768') == '9173454768'
    assert clean_number('(212) 345-8974') == '2123458974'
    assert clean_number('+886 0958787482') == '0958787482'
    assert len(clean_number('(718) 123-4567')) == 10

def clean_number(phone: str) -> str:
    clean_number = re.sub('[+()-]', '', phone).replace(' ','')[-10:]
    assert len(clean_number) == 10, f"clean number expected a 10 digit number, got {len(clean_number)}"
    assert clean_number.isdigit() and isinstance(clean_number, str)
    return clean_number

def test_check_phone_number():
    # check_phone_number() uses global var contacts_objs
    assert check_phone_number(1, "2123458974") == True
    assert check_phone_number(2, "2123458974") == True
    assert check_phone_number(3, "2123458974") == False

def check_phone_number(target_pk: int, phone: str) -> bool:
    '''
    Part 3:
    {
        "id": 0,
        "owner_id": 123,
        "contact_nickname": "Mom",
        "phone": [
            {
                "number": "(212) 345-8974",
                "type": "landline"
            }, {
                "number": "+19173454768",
                "type": "cell"
            }
        ]
    }
    Notes:
    - a Contact belongs to a Person (via foreign key “owner_id”)
    - “phone” is an array of arbitrary length containing phone numbers that are not normalized.
    These string values may contain dashes, parentheses and whitespace.
    - when the country code is included in a phone number, it is always “1” and it may be
    preceded by the “+” sign
    - phone numbers always have ten digits (excluding the optional country code)

    Write a function implementing a new rule for connectedness: two Persons are connected when
    either one has the other’s phone number in their list of contacts.
    '''
    for obj in contacts_objs:
        number_ls = [clean_number(number['number']) for number in obj['phone']]
        if target_pk == obj['owner_id'] and phone in number_ls:
            return True
            break
    return False

def get_cotact_connect(pk: int, phone: str) -> list[str]: # ['John Doe', 'Mary Jane']
    res = []
    for person_obj in person_objs:
        if pk != person_obj['id'] and check_phone_number(person_obj['id'], phone):
            res.append(person_obj['first'] + ' ' + person_obj['last'])
    return res

if __name__ == '__main__':
    print('Please enter a Person ID.')
    input_id = input()
    if input_id.isdigit():
        cty_code, phone, exp = get_target(input_id)
        if cty_code == phone == exp == None:
            print('ID not found!')
        else:
            exp_connect, cotact_connect = [], []
            if exp:
                exp_connect = get_exp_connect(int(input_id), exp)
            if phone:
                cotact_connect = get_cotact_connect(int(input_id), phone)
            # delete duplicates and sort the order
            connect_persons = sorted(list(set(exp_connect + cotact_connect)))
            print('Connected Persons:')
            if connect_persons:
                for person in connect_persons:
                    print(person)
            else:
                print('None.')
    else:
        print('Invalid ID!')
