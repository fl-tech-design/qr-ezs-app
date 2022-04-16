#!/usr/bin/python3

from qrbill import QRBill
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import ast
import pathlib


def save_fav_data(file, keyword, data):
    f = open(file, 'r')
    data_dict_str = f.read()
    f.close()
    data_dict = ast.literal_eval(data_dict_str)
    data_dict[keyword] = data
    f = open(file, 'w')
    f.write(str(data_dict))
    f.close()


def get_lang(keyword):
    f = open(lang_path.get(), 'r')
    data_dict_str = f.read()
    f.close()
    state_dict = ast.literal_eval(data_dict_str)
    act_data = state_dict[keyword]
    return act_data


def export_bill():
    name = e_entry.get(1.0, "end")
    nick = name.split(' ')
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
    if nick[0] not in fav_list:
        answer = messagebox.askokcancel('Favoriten speichern', 'Wollen Sie den Empfänger als Favorit speichern?')
        if answer:
            save_new_fav()
    my_bill.as_svg(bill_path + '/%s-bill.svg' % nick[0])
    delete_values()


def delete_values():
    list_entrys = [e_plz, e_ort, iban, reference, betrag, a_plz, a_ort, e_entry, a_entry]
    for index in range(len(list_entrys) - 2):
        list_entrys[index].delete(0, 'end')
    for item in range(2):
        list_entrys[item + 7].delete('1.0', 'end')


def create_labels(l_text, r, c, cs, st, f_size=2, py=3):
    fon = ('Arial', 12)
    if f_size == 0:
        fon = ('Arial', 14)
    if f_size == 1:
        fon = ('Arial', 16)
    tk.Label(mainwindow, text=l_text, font=fon).grid(row=r, column=c,
                                                     columnspan=cs,
                                                     sticky=st,
                                                     padx=20, pady=py)


def save_new_fav():
    favname = e_entry.get(1.0, "end")
    fav_name_list = favname.split(' ')
    f = open(fav_path + fav_name_list[0] + '.txt', 'w')
    f.write(str({'name': '', 'ort': '', 'plz': '', 'iban': ''}))
    f.close()
    save_fav_data(fav_path + fav_name_list[0] + '.txt', 'name', e_entry.get(1.0, 'end'))
    save_fav_data(fav_path + fav_name_list[0] + '.txt', 'ort', e_ort.get())
    save_fav_data(fav_path + fav_name_list[0] + '.txt', 'plz', e_plz.get())
    save_fav_data(fav_path + fav_name_list[0] + '.txt', 'iban', iban.get())
    listfavfile = open(fav_l_path, 'a')
    listfavfile.write(fav_name_list[0] + '\n')
    listfavfile.close()


def load_fav(selectedfav):
    print(selectedfav)
    f = open(fav_path + selectedfav + '.txt', 'r')
    fav_dict_str = f.read()
    f.close()
    f = open(fav_path + 'Hanspeter.txt', 'r')
    abs_dict_str = f.read()
    f.close()
    fav_dict = ast.literal_eval(fav_dict_str)
    abs_dict = ast.literal_eval(abs_dict_str)
    dict_list = [fav_dict, abs_dict]
    entry_list = [e_entry, a_entry]
    plz_list = [e_plz, a_plz]
    ort_list = [e_ort, a_ort]
    for fields in range(len(dict_list)):
        entry_list[fields].delete('0.1', 'end')
        entry_list[fields].insert('0.1', dict_list[fields]['name'])
        plz_list[fields].delete(0, 'end')
        plz_list[fields].insert(0, dict_list[fields]['plz'])
        ort_list[fields].delete(0, 'end')
        ort_list[fields].insert(0, dict_list[fields]['ort'])
    if selectedfav == 'Hanspeter':
        entry_list[1].delete('0.1', 'end')
        plz_list[1].delete(0, 'end')
        ort_list[1].delete(0, 'end')

    iban.delete(0, 'end')
    iban.insert(0, fav_dict['iban'])


def read_lists(list_file):
    comm_list_file = open(list_file, 'r')
    comm_list = comm_list_file.read().split()
    comm_list_file.close()
    return comm_list


def items_selected(event):
    selected_indices = listbox.curselection()  # get selected indices
    selected_fav = ",".join([listbox.get(index1) for index1 in selected_indices])  # get selected items
    msg = f'Wollen Sie: {selected_fav} auswählen?'
    select_fav(msg, selected_fav)


def select_fav(msg, selectedfav):
    reply = messagebox.askyesno('Bestätigen', msg)
    if reply:
        load_fav(selectedfav)


def set_lang(language):
    if language == 'de':
        lang_path.set(label_de)

    elif language == 'en':
        lang_path.set(label_en)


if __name__ == '__main__':
    # file and program path's
    label_de = str(pathlib.Path().absolute()) + '/qr-ezs-app/languages/.labels_de.txt'
    label_en = str(pathlib.Path().absolute()) + '/qr-ezs-app/languages/.labels_en.txt'
    bill_path = str(pathlib.Path().absolute())
    fav_path = str(pathlib.Path().absolute()) + '/qr-ezs-app/favourites/'
    fav_l_path = str(pathlib.Path().absolute()) + '/qr-ezs-app/favourites/list_fav.txt'

    # create the window
    mainwindow = tk.Tk()
    mainwindow.title('QR Einzahlungsschein')
    mainwindow.resizable(width=False, height=False)

    # variables
    lang_path = tk.StringVar()
    set_lang('de')
    currency = tk.StringVar()
    fav_list = read_lists(fav_l_path)
    fav_list_var = tk.StringVar(value=fav_list)
    # titel
    create_labels(get_lang('lab_tit'), 0, 0, 3, 'w', 1, 15)
    create_labels(get_lang('lab_man'), 1, 0, 4, 'w', 10)
    lab_empf_list = [get_lang('lab_emp'), '', '', get_lang('lab_plz'),
                     get_lang('lab_ort'), get_lang('lab_iba'),
                     get_lang('lab_bet'), get_lang('lab_ref')]
    for i in range(len(lab_empf_list)):
        if i == 0:
            create_labels(lab_empf_list[i], i + 2, 0, 1, 'nw')
        else:
            create_labels(lab_empf_list[i], i + 2, 0, 1, 'w')

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

    # Sender
    # lists with sender labels, which are stored in a dictionary in the language file
    lab_abs_list = [get_lang('lab_abs'), '', '', get_lang('lab_plz'),
                    get_lang('lab_ort'), get_lang('lab_cur'), get_lang('lab_fav')]
    for i in range(len(lab_abs_list)):
        if i == 0:
            create_labels(lab_abs_list[i], i + 2, 2, 1, 'nw')
        else:
            create_labels(lab_abs_list[i], i + 2, 2, 1, 'ww')

    # sendertextfield for name and adress
    a_entry = tk.Text(mainwindow, width=30, height=3, bd=1)
    a_entry.grid(row=2, column=3, rowspan=3, columnspan=2)
    a_plz = tk.Entry(mainwindow, width=30, bd=1)
    a_plz.grid(row=5, column=3, columnspan=2, padx=10)
    a_ort = tk.Entry(mainwindow, width=30, bd=1)
    a_ort.grid(row=6, column=3, columnspan=2)

    # Currency choice
    tk.Radiobutton(mainwindow, text='CHF', indicatoron=False, width=10,
                   variable=currency, value='CHF', selectcolor='lightgreen',
                   command=lambda: currency.set('CHF')).grid(row=7, column=3, sticky='e')
    tk.Radiobutton(mainwindow, text='EUR', indicatoron=False, width=10,
                   variable=currency, value='EUR', selectcolor='lightgreen',
                   command=lambda: currency.set('EUR')).grid(row=7, column=4, sticky='w')

    tk.Button(mainwindow, text=get_lang('lab_fin'), font=('Calibri', 16), width=50, command=export_bill, bd=2).grid(
        row=10, column=0,
        columnspan=5,
        padx=30, pady=15)
    tk.Button(mainwindow, text=get_lang('lab_clear'), command=delete_values, width=8). grid(row=9, column=2)

    listbox = Listbox(mainwindow, listvariable=fav_list_var, height=3, width=30, selectmode='browse')
    listbox.grid(row=8, column=3, pady=5, columnspan=2, rowspan=2)
    listbox.bind('<<ListboxSelect>>', items_selected)

    mainwindow.mainloop()
