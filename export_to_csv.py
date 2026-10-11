import pandas as pd
import numpy as np

def extract_data_from_gsheet(sheet_id: str, sheet_name: str, dtype=None):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    return pd.read_excel(url, sheet_name=sheet_name, dtype=dtype)

print("1. Mengekstrak data dari Google Spreadsheet...")
sheet_id = '1He4b-15DsAJG_dwYgBz5nDVNW_zQfXZ3VSYoASr4WVo'

transaction = extract_data_from_gsheet(sheet_id, 'transaction')
master_account = extract_data_from_gsheet(sheet_id, 'master_account')
master_customer = extract_data_from_gsheet(sheet_id, 'master_customer')
master_transaction_code = extract_data_from_gsheet(sheet_id, 'master_transaction_code')
master_bank_code = extract_data_from_gsheet(sheet_id, 'master_bank_code', dtype={'bank_code': pd.StringDtype()})
master_branch = extract_data_from_gsheet(sheet_id, 'master_branch')

print("2. Pembersihan duplikasi (Primary Key)...")
transaction = transaction.drop_duplicates(subset=['transaction_id'])
master_account = master_account.drop_duplicates(subset=['account_number'])
master_customer = master_customer.drop_duplicates(subset=['cif_number'])
master_transaction_code = master_transaction_code.drop_duplicates(subset=['transaction_code'])
master_bank_code = master_bank_code.drop_duplicates(subset=['bank_code'])
master_branch = master_branch.drop_duplicates(subset=['branch_code'])

print("3. Transformasi tanggal dan waktu...")
transaction['transaction_date'] = transaction['transaction_date'].astype(str)
transaction['transaction_date'] = pd.to_datetime(transaction['transaction_date'], format='%Y%j').dt.strftime('%Y-%m-%d')

transaction['transaction_time'] = transaction['transaction_time'].astype(str).str.zfill(6)
transaction['transaction_time'] = pd.to_datetime(transaction['transaction_time'], format='%H%M%S').dt.strftime('%H:%M:%S')

transaction['transaction_datetime'] = pd.to_datetime(transaction['transaction_date'] + ' ' + transaction['transaction_time'])
transaction = transaction.drop(columns=['transaction_time', 'transaction_date'])

transaction = transaction.sort_values(by=['account_number', 'transaction_datetime'], ascending=[True, True]).reset_index(drop=True)

print("4. Transformasi debit, credit, & additional fee...")
transaction['credit_amount'] = np.where(transaction['debit_or_credit'] == 'C', transaction['amount'], 0)
transaction['debit_amount'] = np.where(transaction['debit_or_credit'] == 'D', transaction['amount'], 0)
transaction = transaction.drop(columns=['amount'])

transaction = transaction.merge(master_transaction_code, on='transaction_code', how='left')

transaction_fee = transaction[transaction['transaction_code'] == 'TRX092'][['transaction_reference', 'debit_amount']].copy()
transaction_fee = transaction_fee.rename(columns={'debit_amount': 'additional_fee'})

transaction = transaction[transaction['transaction_code'] != 'TRX092'].copy()
transaction = transaction.merge(transaction_fee, on='transaction_reference', how='left')
transaction['additional_fee'] = transaction['additional_fee'].fillna(0.0)

print("5. Menghitung saldo berjalan (balance)...")
transaction['balance'] = transaction.groupby('account_number').apply(
    lambda g: (g['credit_amount'] - g['debit_amount'] - g['additional_fee']).cumsum(),
    include_groups=False
).reset_index(level=0, drop=True)

print("6. Klasifikasi trasmode_code...")
transfer_transaction = transaction[transaction['transaction_code'] == 'TRX002']
transfer_counts = transfer_transaction.groupby(['transaction_code', 'transaction_reference']).size().reset_index(name='total_transaction')
overbooking_refs = transfer_counts[transfer_counts['total_transaction'] > 1]['transaction_reference'].tolist()

def determine_transmode(row):
    tc = row['transaction_code']
    if tc == 'TRX001':
        return 'SETOR'
    elif tc == 'TRX003':
        return 'TARIK'
    elif tc == 'TRX004':
        return 'PURCHASE'
    elif tc == 'TRX091':
        return 'INTER'
    elif tc == 'TRX002':
        if row['transaction_reference'] in overbooking_refs:
            return 'OVERBOOKING'
        elif row['debit_or_credit'] == 'C':
            return 'INCOMING'
        elif row['debit_or_credit'] == 'D':
            return 'OUTGOING'
    return 'OTHER'

transaction['trasmode_code'] = transaction.apply(determine_transmode, axis=1)

print("7. Ekstraksi acquirer info...")
def get_acquirer_bank_code(row):
    remark = str(row['transaction_remark'])
    tmode = row['trasmode_code']
    if tmode == 'TARIK':
        parts = remark.split()
        if len(parts) >= 4 and parts[0] == 'TARIK' and parts[1] == 'VIA' and parts[2] == 'ATM':
            return parts[3]
    elif tmode == 'OUTGOING' and remark.startswith('QRIS_'):
        parts = remark.split('_')
        if len(parts) >= 2:
            return parts[1]
    elif tmode in ['INCOMING', 'OUTGOING', 'OVERBOOKING'] and (remark.startswith('TRF_') or remark.startswith('BIFAST_')):
        parts = remark.split('_')
        if len(parts) >= 2:
            return parts[1]
    return pd.NA

def get_acquirer_account_number(row):
    remark = str(row['transaction_remark'])
    tmode = row['trasmode_code']
    if tmode in ['INCOMING', 'OUTGOING', 'OVERBOOKING'] and (remark.startswith('TRF_') or remark.startswith('BIFAST_')):
        parts = remark.split('_')
        if len(parts) >= 3:
            return parts[2]
    return pd.NA

def get_acquirer_account_name(row):
    remark = str(row['transaction_remark'])
    tmode = row['trasmode_code']
    if tmode in ['INCOMING', 'OUTGOING', 'OVERBOOKING'] and (remark.startswith('TRF_') or remark.startswith('BIFAST_')):
        parts = remark.split('_', 3)
        if len(parts) >= 4:
            return parts[3]
    return pd.NA

transaction['acquirer_bank_code'] = transaction.apply(get_acquirer_bank_code, axis=1).astype(pd.StringDtype())
transaction['acquirer_account_number'] = transaction.apply(get_acquirer_account_number, axis=1).astype(pd.StringDtype())
transaction['acquirer_account_name'] = transaction.apply(get_acquirer_account_name, axis=1).astype(pd.StringDtype())

print("8. Integrasi dengan master tables...")
transaction = transaction.merge(
    master_bank_code[['bank_code', 'bank_name']].rename(columns={'bank_name': 'acquirer_bank_name'}),
    left_on='acquirer_bank_code',
    right_on='bank_code',
    how='left'
).drop(columns=['bank_code'])

transaction = transaction.merge(
    master_account[['account_number', 'cif_number', 'account_open_date', 'account_currency_type', 'account_status', 'product_code', 'product_name']],
    on='account_number',
    how='left'
)

transaction['account_aging'] = (transaction['transaction_datetime'].dt.floor('D') - pd.to_datetime(transaction['account_open_date'])).dt.days

transaction = transaction.merge(
    master_customer[['cif_number', 'customer_name', 'gender', 'branch_code']],
    on='cif_number',
    how='left'
)

transaction = transaction.merge(
    master_branch[['branch_code', 'branch_name']],
    on='branch_code',
    how='left'
)

transaction['created_date'] = pd.Timestamp.now()
transaction['created_by'] = 'SYSTEM'

output_file = 'fsb_estatement_transaction.csv'
print(f"9. Menyimpan hasil ke {output_file}...")
transaction.to_csv(output_file, index=False)
print(f"Selesai! Dimensi data: {transaction.shape[0]} baris x {transaction.shape[1]} kolom.")
print("Kolom yang tersedia:")
for col in transaction.columns:
    print(f"- {col}")
