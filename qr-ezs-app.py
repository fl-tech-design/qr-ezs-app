#! /home/peti/qr-ezs-app/venv/bin/python

from qrbill import QRBill
import tkinter as tk
import ast
import pathlib


def set_data(keyword, data):
    f = open(lang_path.get(), 'r')
    data_dict_str = f.read()
    f.close()
    data_dict = ast.literal_eval(data_dict_str)
    data_dict[keyword] = data
    f = open(lang_path.get(), 'w')
    f.write(str(data_dict))
    f.close()


def get_data(keyword):
    f = open(lang_path.get(), 'r')
    data_dict_str = f.read()
    f.close()
    state_dict = ast.literal_eval(data_dict_str)
    act_data = state_dict[keyword]
    return act_data


def exportBill():
    my_bill = QRBill(
        account=iban.get(),
        creditor={
            'name': e_entry.get(1.0, "end"),
            'pcode': e_plz.get(),
            'city': e_ort.get(),
        },
        amount=betrag.get(),
        currency=currency.get(),
        language='de',
        ref_number=reference.get(),
        debtor={
            'name': a_entry.get(1.0, "end"),
            'pcode': a_plz.get(),
            'city': a_ort.get()
        },
    )
    my_bill.as_svg(bill_path + '-bill.svg')
    list_entrys = [e_plz, e_ort, iban, reference, betrag, a_plz, a_ort, e_entry, a_entry]
    for index in range(len(list_entrys) - 2):
        list_entrys[index].delete(0, 'end')
    for item in range(2):
        list_entrys[item + 7].delete('1.0', 'end')


def create_Labels(l_text, r, c, cs, st, f_size=2, py=3):
    fon = ('Arial', 12)
    if f_size == 0:
        fon = ('Arial', 14)
    if f_size == 1:
        fon = ('Arial', 16)
    tk.Label(mainwindow, text=l_text, font=fon).grid(row=r, column=c,
                                                     columnspan=cs,
                                                     sticky=st,
                                                     padx=20, pady=py)


if __name__ == '__main__':
    label_german = str(pathlib.Path().absolute()) + '/qr-ezs-app/.labels_de.txt'
    label_english = str(pathlib.Path().absolute()) + '/qr-ezs-app/.labels_en.txt'
    bill_path = str(pathlib.Path().absolute())

    mainwindow = tk.Tk()
    mainwindow.title('QR Einzahlungschein')
    mainwindow.geometry('800x390')
    mainwindow.resizable(width=False, height=False)

    # Variabeln
    lang_path = tk.StringVar(value=label_german)
    currency = tk.StringVar()
    language = tk.StringVar()

    # Titel
    create_Labels(get_data('lab_tit'), 0, 0, 3, 'w', 1, 15)
    create_Labels(get_data('lab_man'), 1, 0, 4, 'w', 10)

    lab_empf_list = [get_data('lab_emp'), '', '', get_data('lab_plz'),
                     get_data('lab_ort'), get_data('lab_iba'),
                     get_data('lab_bet'), get_data('lab_ref')]

    for i in range(len(lab_empf_list)):
        if i == 0:
            create_Labels(lab_empf_list[i], i + 2, 0, 1, 'nw')
        else:
            create_Labels(lab_empf_list[i], i + 2, 0, 1, 'w')

    # Empfängertextfeld für Name und Adresse und PLZ
    e_entry = tk.Text(mainwindow, width=30, height=3, bd=1)
    e_entry.grid(row=2, column=1, rowspan=3)

    e_plz = tk.Entry(mainwindow, width=30, bd=1)
    e_plz.grid(row=5, column=1)

    e_ort = tk.Entry(mainwindow, width=30, bd=1)
    e_ort.grid(row=6, column=1)

    iban = tk.Entry(mainwindow, width=30, bd=1)
    iban.grid(row=7, column=1)

    betrag = tk.Entry(mainwindow, width=30, bd=1)
    betrag.grid(row=8, column=1)

    reference = tk.Entry(mainwindow, width=30, bd=1)
    reference.grid(row=9, column=1)

    # Absender
    # Absendertextfeld für Name und Adresse und PLZ
    lab_abs_list = [get_data('lab_abs'), '', '', get_data('lab_plz'),
                    get_data('lab_ort'), get_data('lab_cur'), get_data('lab_lan')]

    for i in range(len(lab_abs_list)):
        if i == 0:
            create_Labels(lab_abs_list[i], i + 2, 2, 1, 'nw')
        else:
            create_Labels(lab_abs_list[i], i + 2, 2, 1, 'ww')

    a_entry = tk.Text(mainwindow, width=30, height=3, bd=1)
    a_entry.grid(row=2, column=3, rowspan=3, columnspan=2)

    a_plz = tk.Entry(mainwindow, width=30, bd=1)
    a_plz.grid(row=5, column=3, columnspan=2)

    a_ort = tk.Entry(mainwindow, width=30, bd=1)
    a_ort.grid(row=6, column=3, columnspan=2)

    tk.Radiobutton(mainwindow, text='CHF', indicatoron=0, width=10,
                   variable=currency, value='CHF', selectcolor='green',
                   command=lambda: currency.set('CHF')).grid(row=7, column=3, sticky='e')
    tk.Radiobutton(mainwindow, text='EUR', indicatoron=0, width=10,
                   variable=currency, value='EUR', selectcolor='green',
                   command=lambda: currency.set('EUR')).grid(row=7, column=4, sticky='w')
    tk.Radiobutton(mainwindow, text=get_data('lan_ger'), indicatoron=0, width=10,
                   variable=lang_path, value='de', selectcolor='green',
                   command=lambda: lang_path.set(label_german)).grid(row=8, column=3, sticky='e')
    tk.Radiobutton(mainwindow, text=get_data('lan_eng'), indicatoron=0, width=10,
                   variable=lang_path, value='en', selectcolor='green',
                   command=lambda: lang_path.set(label_english)).grid(row=8, column=4, sticky='w')

    tk.Button(mainwindow, text=get_data('lab_fin'), font=('Calibri', 16), width=50, command=exportBill, bd=2).grid(
        row=10, column=0,
        columnspan=5,
        padx=30, pady=15)

    mainwindow.mainloop()
