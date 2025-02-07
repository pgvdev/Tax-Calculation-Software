import tkinter
from tkinter import ttk
import tkinter.messagebox
from tkinter import messagebox as mbox
import os
import openpyxl

# Welcome message
mbox.showinfo(title="Welcome!", message="Welcome to the UK Tax Calculator!")


def clear_input_fields():
    first_name_entry.delete(0, tkinter.END)
    last_name_entry.delete(0, tkinter.END)
    organisation_entry.delete(0, tkinter.END)
    income_spinbox.delete(0, tkinter.END)
    accept_var.set("0")
    title_combobox.set("")


def ask_another_employee():
    result = tkinter.messagebox.askyesno("Add Another Employee",
                                         "The previous employee details inserted will be deleted, "
                                         "would you like to continue?")
    if result:
        clear_input_fields()
        window2.destroy()
    else:
        # Welcome message
        mbox.showinfo(title="Goodbye!", message="Thank you for using the UK Tax Calculator!")
        window.destroy()
        window2.destroy()


def is_decimal(income):
    try:
        float(income)
        return True
    except ValueError:
        return False


def enter_data():
    accepted = accept_var.get()

    if accepted == "Accepted":
        # Employee information
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        organisation = organisation_entry.get()
        income = income_spinbox.get()

        if not is_decimal(income):
            tkinter.messagebox.showwarning(title="Error", message="Income must be a decimal number.")
            return

        if float(income) <= 12570:
            tax = 0
            yearly_net_pay = float(income) - float(tax)
            monthly_income = float(yearly_net_pay) / 12
            monthly_tax = float(tax) / 12
            monthly_net_pay = float(monthly_income) - float(monthly_tax)
            weekly_income = float(monthly_income) / 4
            weekly_tax = float(monthly_tax) / 4
            tax_band = "Personal Allowance"
        elif float(income) <= 50270:
            tax = (float(income) - 12570) * 0.2
            yearly_net_pay = float(income) - float(tax)
            monthly_income = float(yearly_net_pay) / 12
            monthly_tax = float(tax) / 12
            monthly_net_pay = float(monthly_income) - float(monthly_tax)
            weekly_income = float(monthly_income) / 4
            weekly_tax = float(monthly_tax) / 4
            tax_band = "Basic Rate"
        elif float(income) <= 125140:
            tax = (float(income) - 50270) * 0.4 + (50270 - 12570) * 0.2
            yearly_net_pay = float(income) - float(tax)
            monthly_income = float(yearly_net_pay) / 12
            monthly_tax = float(tax) / 12
            monthly_net_pay = float(monthly_income) - float(monthly_tax)
            weekly_income = float(monthly_income) / 4
            weekly_tax = float(monthly_tax) / 4
            tax_band = "Higher Rate"
        else:
            tax = (float(income) - 125140) * 0.45 + (125140 - 50270) * 0.4 + (50270 - 12570) * 0.2
            yearly_net_pay = float(income) - float(tax)
            monthly_income = float(yearly_net_pay) / 12
            monthly_tax = float(tax) / 12
            monthly_net_pay = float(monthly_income) - float(monthly_tax)
            weekly_income = float(monthly_income) / 4
            weekly_tax = float(monthly_tax) / 4
            tax_band = "Additional Rate"
        if firstname and lastname and organisation and income:
            title = title_combobox.get()
            display_tax_in_custom_window(title, firstname, lastname, organisation,
                                         income, tax, yearly_net_pay, monthly_income, monthly_tax, monthly_net_pay,
                                         weekly_income, weekly_tax, tax_band)
        else:
            tkinter.messagebox.showwarning(title="Error", message="Full name, organisation and income are required.")
    else:
        tkinter.messagebox.showwarning(title="Error", message="You have not confirmed the information")


def display_tax_in_custom_window(title, firstname, lastname, organisation,
                                 income, tax, yearly_net_pay, monthly_income, monthly_tax, monthly_net_pay,
                                 weekly_income, weekly_tax, tax_band):
    global window2
    window2 = tkinter.Tk()
    window2.title("Employee Details")

    frame2 = tkinter.Frame(window2)
    frame2.pack()

    frame2 = tkinter.LabelFrame(frame2, text="General Information")
    frame2.pack(padx=20, pady=10)

    frame3 = tkinter.LabelFrame(window2, text="Payments Information")
    frame3.pack(padx=20, pady=10)

    frame4 = tkinter.LabelFrame(window2, text="Deductions")
    frame4.pack(padx=20, pady=10)

    frame5 = tkinter.LabelFrame(window2, text="")
    frame5.pack(padx=20, pady=10)

    name_label = tkinter.Label(frame2, text="Name: {} {} {}".format(title, firstname, lastname))
    name_label.pack()

    organisation2_label = tkinter.Label(frame2, text="Organisation: {}".format(organisation))
    organisation2_label.pack()

    income2_label = tkinter.Label(frame3, text="Yearly Gross Income: £{:.2f}".format(float(income)))
    income2_label.pack()

    tax_band_label = tkinter.Label(frame2, text="Tax Band: {}".format(tax_band))
    tax_band_label.pack()

    tax_label = tkinter.Label(frame4, text="Yearly Tax: £{:.2f}".format(float(tax)))
    tax_label.pack()

    yearly_net_pay_label = tkinter.Label(frame3, text="Yearly Net Income: £{:.2f}".format(float(yearly_net_pay)))
    yearly_net_pay_label.pack()

    monthly_income_label = tkinter.Label(frame3, text="Monthly Income: £{:.2f}".format(float(monthly_income)))
    monthly_income_label.pack()

    monthly_tax_label = tkinter.Label(frame4, text="Monthly Tax: £{:.2f}".format(float(monthly_tax)))
    monthly_tax_label.pack()

    monthly_net_pay_label = tkinter.Label(frame5, text="Monthly Net Income: £{:.2f}".format(float(monthly_net_pay)))
    monthly_net_pay_label.pack()

    weekly_income_label = tkinter.Label(frame3, text="Weekly Income: £{:.2f}".format(float(weekly_income)))
    weekly_income_label.pack()

    weekly_tax_label = tkinter.Label(frame4, text="Weekly Tax: £{:.2f}".format(float(weekly_tax)))
    weekly_tax_label.pack()

    # Button to ask for another employee
    another_employee_button = tkinter.Button(window2,
                                             text="Add Another Employee", command=ask_another_employee)
    another_employee_button.pack(padx=20, pady=10)

    # Close the window when another employee is added
    window2.protocol("WM_DELETE_WINDOW", ask_another_employee)

    filepath = r"/Users/pop/Downloads/uktaxcalculator.xlsx"

    if not os.path.exists(filepath):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        heading = ["Title", "First Name", "Last Name", "Organisation", "Income",
                   "Tax", "Net Pay", "Monthly Income", "Monthly Tax", "Weekly Income", "Weekly Tax"]
        sheet.append(heading)
        workbook.save(filepath)
    workbook = openpyxl.load_workbook(filepath)
    sheet = workbook.active
    sheet.append([title, firstname, lastname, organisation, income, tax, yearly_net_pay,
                  monthly_income, monthly_tax, weekly_income, weekly_tax])
    workbook.save(filepath)

    window2.mainloop()


window = tkinter.Tk()
window.title("UK Tax Calculator")
my_img = tkinter.PhotoImage(file="/Users/pop/Downloads/a4.png")
l2 = tkinter.Label(image=my_img)
l2.grid(row=0, column=0, padx=5, pady=5)

# Saving Employee Information
employees_info_frame = tkinter.LabelFrame(window, text="Employee Information")
employees_info_frame.grid(row=1, column=0, padx=20, pady=10)

title_label = tkinter.Label(employees_info_frame, text="Title")
title_combobox = ttk.Combobox(employees_info_frame, values=["Mr.", "Ms.", "Dr."])
title_label.grid(row=0, column=0)
title_combobox.grid(row=1, column=0)

first_name_label = tkinter.Label(employees_info_frame, text="First Name")
first_name_label.grid(row=0, column=1)
last_name_label = tkinter.Label(employees_info_frame, text="Last Name")
last_name_label.grid(row=0, column=2)

first_name_entry = tkinter.Entry(employees_info_frame)
last_name_entry = tkinter.Entry(employees_info_frame)
first_name_entry.grid(row=1, column=1)
last_name_entry.grid(row=1, column=2)

organisation_label = tkinter.Label(employees_info_frame, text="Organisation")
organisation_label.grid(row=2, column=0)
organisation_entry = tkinter.Entry(employees_info_frame)
organisation_entry.grid(row=3, column=0)

income_label = tkinter.Label(employees_info_frame, text="Income")
income_spinbox = tkinter.Spinbox(employees_info_frame, from_=0, to=99999999999999999999999999999999999999)
income_label.grid(row=2, column=1)
income_spinbox.grid(row=3, column=1)

# Button
button = tkinter.Button(employees_info_frame, text="Calculate", command=enter_data)
button.grid(row=3, column=2, sticky="news", padx=30, pady=20)

for widget in employees_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Save & Continue
save_frame = tkinter.LabelFrame(window, text="Required Field")
save_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

accept_var = tkinter.StringVar(value="Not Accepted")
save_continue = tkinter.Checkbutton(save_frame, text="I can confirm these details.",
                                    variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
save_continue.grid(row=0, column=0)

window.mainloop()
 