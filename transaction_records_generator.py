import csv
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker to generate fake data
fake = Faker()

# generate transaction records into a csv file
def generate_records(no_of_unique_customers, no_of_records, filename = 'records.csv'):
    customers = generate_customer_info(no_of_unique_customers)
    with open(filename, mode='w', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'name', 'debit_card_number', 'debit_card_type', 'bank_name', 'transaction_date', 'amount_spend'])
        i = 0
        while i < no_of_records:
            (customer_id, customer_name) = customers[random.randint(0, no_of_unique_customers - 1)]
            writer.writerow([
                customer_id,
                customer_name,
                generate_card_number(),
                generate_card_type(),
                generate_bank_name(),
                generate_transaction_time(),
                generate_amount_spent()
                
            ])
            i += 1
    print(f"{filename} generated")

# generate amount spend
def generate_amount_spent():
    amount_spent = round(random.uniform(1, 1000), 2)
    return amount_spent

# generate transaction datetime
def generate_transaction_time():
    transaction_date = fake.date_time_between(start_date="-1y", end_date="now").strftime('%Y-%m-%d %H:%M:%S')
    return transaction_date

#genarate bank name
def generate_bank_name():
    bank_list = ['State Bank','Bank of America', 'HDFC','BOB','ICICI','AXIS', 'PNB']
    return bank_list[random.randint(0, 6)]

# generate unique customer_id with corresponding customer_name in a list
def generate_customer_info(no_of_customers):
    customer_id_name_list = [(fake.random_int(min=1000, max=9999), fake.name()) for _ in range(no_of_customers)] # (customer_id, customer_name)
    return customer_id_name_list

# generate 16 digit debit card number as integer
def generate_card_number():
    card_no = 4       #visa card starts with 4
    for i in range(15):
        card_no = card_no*10 + random.randint(0, 9)
    return card_no


# generate card type as string
def generate_card_type():
    return random.choice(['Visa', 'MasterCard', 'American Express', 'RuPay'])


if __name__ == '__main__':
    for day in range(19, 23):
        generate_records(1000, 1000000, f"{day}_03_2024.csv")
