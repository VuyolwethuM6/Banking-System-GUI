from CTkMessagebox import CTkMessagebox
from time import gmtime, strftime
import customtkinter as ctk
from PIL import Image
import random


# Check if input is numeric
def is_number(s):
    try:
        number = float(s)
        if number > 0:
            return True
        else:
            return False
    except ValueError:
        return False


# Check if Account number exits
def check_acc_nmb(num):
    try:
        fpin = open(num + ".txt", 'r')
    except FileNotFoundError:
        CTkMessagebox(title="Error", message="User not found, check Credentials!", icon="warning")
        return 0
    fpin.close()
    return


def home_return(master):
    master.destroy()
    Main_Menu()


# Create user files
def write(master, name, oc, pin):
    # Validate the user input
    if (is_number(name)) or (is_number(oc) == 0) or name == "":
        CTkMessagebox(title="Error", message="Invalid Credentials\nPlease try again.", icon="warning")
        master.destroy()
        return

    f1 = open("Account_Record.txt", 'r')
    account_no = int(f1.readline())
    account_no += 1
    f1.close()

    f1 = open("Account_Record.txt", 'w')
    f1.write(str(account_no))
    f1.close()

    fdet = open(str(account_no) + ".txt", "w")
    fdet.write(pin + "\n")
    fdet.write(oc + "\n")
    fdet.write(str(account_no) + "\n")
    fdet.write(name + "\n")
    fdet.close()

    frec = open(str(account_no) + "-rec.txt", 'w')
    frec.write("Date                             Transaction            Balance\n")
    frec.write(str(strftime("[%Y-%m-%d][%H:%M:%S]  ", gmtime())) + "    " + oc + "                " + oc + "\n")
    frec.close()

    CTkMessagebox(title="Acc Details", message="Your Account Number is: " + str(account_no), icon="check")
    master.destroy()
    return


# Update Users Credit/Deposits
def crdt_write(master, amount, account):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    if is_number(amount) == 0:
        CTkMessagebox(title="Error", message="Invalid Input!", icon="cancel")
        master.destroy()
        return

    fdet = open(account + ".txt", 'r')
    pin = fdet.readline()
    camt = int(fdet.readline())
    fdet.close()

    amti = int(amount)
    cd = amti + camt
    fdet = open(account + ".txt", 'w')
    fdet.write(pin)
    fdet.write(str(cd) + "\n")
    fdet.write(account + "\n")
    fdet.close()

    frec = open(str(account) + "-rec.txt", 'a+')
    frec.write(
        str(strftime("[%Y-%m-%d][%H:%M:%S]  ", gmtime())) + "+" + str(amti) + "              " + str(cd) + "\n")
    frec.close()
    CTkMessagebox(message="Deposit Successful!", icon="check")
    master.destroy()
    return


# Update Users Debits/Withdrawal
def debit_write(master, amount, account):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    if is_number(amount) == 0:
        CTkMessagebox(title="Error", message="Invalid Input!", icon="cancel")
        master.destroy()
        return

    fdet = open(account + ".txt", 'r')
    pin = fdet.readline()
    camt = int(fdet.readline())
    fdet.close()

    if int(amount) > camt:
        CTkMessagebox(title="Error", message="Insufficient Funds!", icon="cancel")
    else:
        amti = int(amount)
        cd = camt - amti
        fdet = open(account + ".txt", 'w')
        fdet.write(pin)
        fdet.write(str(cd) + "\n")
        fdet.write(account + "\n")
        fdet.close()

        frec = open(str(account) + "-rec.txt", 'a+')
        frec.write(str(strftime("[%Y-%m-%d][%H:%M:%S]  ", gmtime())) + "-" + str(amti) + "              " +
                   str(cd) + "\n")
        frec.close()
        CTkMessagebox(message="Withdrawal Successful!", icon="check")
        master.destroy()
        return


# Make deposit window
def deposit_amt(account):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    deposit_wind = ctk.CTkToplevel()
    deposit_wind.geometry("500x500")
    deposit_wind.title("Deposits")

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/dposit_money.png"), size=(200, 200))
    disply_icon = ctk.CTkLabel(deposit_wind, image=icon, text='').pack(padx=20, pady=20)

    l1 = ctk.CTkLabel(deposit_wind, text="Enter Amount to be deposited: ")
    e1 = ctk.CTkEntry(deposit_wind)
    l1.pack(pady=12, padx=10)
    e1.pack(pady=12, padx=10)

    # Deposit Button
    b = ctk.CTkButton(deposit_wind, text="Deposit", command=lambda: crdt_write(deposit_wind, e1.get(), account))
    b.pack(pady=12, padx=10)
    deposit_wind.bind("<Return>", lambda x: crdt_write(deposit_wind, e1.get(), account))

    # Cancel Button
    b1 = ctk.CTkButton(deposit_wind, text="Cancel", command=deposit_wind.destroy)
    b1.pack(pady=12, padx=10)


# Make Deposit window
def withdraw_amt(account):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    withdraw_wind = ctk.CTkToplevel()
    withdraw_wind.geometry("500x500")
    withdraw_wind.title("Withdrawals")

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/withdraw_money.png"), size=(200, 200))
    disply_icon = ctk.CTkLabel(withdraw_wind, image=icon, text='').pack(padx=20, pady=20)

    l1 = ctk.CTkLabel(withdraw_wind, text="Enter Amount to be withdrawn: ")
    e1 = ctk.CTkEntry(withdraw_wind)
    l1.pack(pady=12, padx=10)
    e1.pack(pady=12, padx=10)

    # Withdraw Button
    b = ctk.CTkButton(withdraw_wind, text="Withdraw", command=lambda: debit_write(withdraw_wind, e1.get(), account))
    b.pack(pady=12, padx=10)
    withdraw_wind.bind("<Return>", lambda x: debit_write(withdraw_wind, e1.get(), account))

    # Cancel Button
    b1 = ctk.CTkButton(withdraw_wind, text="Cancel", command=withdraw_wind.destroy)
    b1.pack(pady=12, padx=10)


# Display Balance
def disp_bal(account):
    fdet = open(account + ".txt", 'r')
    fdet.readline()
    bal = fdet.readline()
    fdet.close()
    CTkMessagebox(title="Balance", message="Current Balance: R" + str(bal))


# Display transaction history
def disp_tr_hist(account):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    transaction_wind = ctk.CTkToplevel()
    transaction_wind.geometry("500x680")
    transaction_wind.title("Transaction History")

    # Title/Heading
    l_title = ctk.CTkLabel(master=transaction_wind, text="CodeX Banking System", font=('Times New Roman Bold', 20))
    l_title.pack(pady=20)

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/transaction-history.png"), size=(200, 200))
    disply_icon = ctk.CTkLabel(transaction_wind, image=icon, text='').pack(padx=20, pady=20)

    l1 = ctk.CTkLabel(transaction_wind, text="Your Transaction History:",  padx=100, pady=20, width=1000)
    l1.pack(side="top")

    scrollable_frame = ctk.CTkScrollableFrame(master=transaction_wind, width=200, height=200)
    scrollable_frame.pack(side="top", pady=20, padx=40, fill='both', expand=True)

    frec = open(account + "-rec.txt", 'r')
    for line in frec:
        l = ctk.CTkLabel(scrollable_frame, text=line, padx=100, pady=20, width=1000)
        l.pack(side="top")

    b = ctk.CTkButton(transaction_wind, text="Quit", command=transaction_wind.destroy)
    b.pack(pady=12, padx=10)
    frec.close()
    

def logged_in_menu(account):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root_wind = ctk.CTkToplevel()
    root_wind.geometry("320x540")
    root_wind.title("CodeX  Banking System")

    # Title/Heading
    l_title = ctk.CTkLabel(master=root_wind, text="CodeX  Banking System", 
                           font=('Times New Roman Bold', 20))
    l_title.grid(row=0, column=0, columnspan=2, pady=20)

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/Welcome.png"), size=(240, 200))
    disply_icon = ctk.CTkLabel(root_wind, image=icon, text='').grid(row=1, column=0, columnspan=2, pady=20)

    # Retrieve username 
    fdet = open(account + ".txt", 'r')
    fdet.readline()
    username = fdet.readline()
    fdet.close()
    
    label = ctk.CTkLabel(master=root_wind, text=f"Welcome Back {username}")
    label.grid(row=2, column=0, columnspan=2)

    # Deposit Button
    b2 = ctk.CTkButton(master=root_wind, text="Deposit", 
                       command=lambda: deposit_amt(account))
    b2.grid(row=3, column=0, pady=12, padx=10, sticky='nsew')

    # View Balance Button
    b4 = ctk.CTkButton(master=root_wind, text="View Balance", 
                       command=lambda: disp_bal(account))
    b4.grid(row=3, column=1, pady=12, padx=10, sticky='nsew')

    # Withdraw Button
    b3 = ctk.CTkButton(master=root_wind, text="Withdraw", 
                       command=lambda: withdraw_amt(account))
    b3.grid(row=4, column=0, pady=12, padx=10, sticky='nsew')

    # View Transaction History Button
    b5 = ctk.CTkButton(master=root_wind, text="Transaction History", 
                       command=lambda: disp_tr_hist(account))
    b5.grid(row=4, column=1, columnspan=2, pady=12, padx=10, sticky='nsew')

    # Log Out Button
    b6 = ctk.CTkButton(master=root_wind, text="Logout",
                       command=lambda: logout(root_wind))
    b6.grid(row=5, column=0, pady=12, padx=10, sticky='nsew')


# Log out the user
def logout(master):
    CTkMessagebox(title="Log Out", message="You Have Been Successfully Logged Out!!", icon="check")
    master.destroy()
    Main_Menu()


# Login Validation
def check_log_in(master, account_num, pin):
    if check_acc_nmb(account_num) == 0:
        # master.destroy()
        # Main_Menu()
        return

    if is_number(pin) == 0:
        CTkMessagebox(title="Error", message="Account Number does not exist.\nPlease try again.", icon="warning")
        # master.destroy()
        # Main_Menu()
    else:
        master.destroy()
        logged_in_menu(account_num)


def log_in(master):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    master.destroy()

    login_wind = ctk.CTkToplevel()
    login_wind.geometry("500x500")
    login_wind.title("Log in")

    # Title/Heading
    l_title = ctk.CTkLabel(master=login_wind, text="CodeX Banking System", font=('Times New Roman Bold', 20))
    l_title.grid(row=0, column=0, columnspan=3, pady=20)

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/login.png"), size=(250, 200))
    disply_icon = ctk.CTkLabel(login_wind, image=icon, text='')
    disply_icon.grid(row=1, column=0, columnspan=3, pady=20)

    # Details Frame
    frame = ctk.CTkFrame(master=login_wind)
    frame.grid(row=2, column=0, columnspan=3, pady=20)

    # Enter Account number
    l2 = ctk.CTkLabel(frame, text="Enter account number:")
    l2.grid(row=0, column=0, padx=10, sticky="e")
    e2 = ctk.CTkEntry(frame)
    e2.grid(row=0, column=1, pady=12, padx=10)

    # Enter Account Pin
    l3 = ctk.CTkLabel(frame, text="Enter your PIN:")
    l3.grid(row=1, column=0, padx=10, sticky="e")
    e3 = ctk.CTkEntry(frame, show="*")
    e3.grid(row=1, column=1, pady=12, padx=10)

    # Show and Hide Pin
    def show_and_hide():
        if e3.cget('show') == '*':
            e3.configure(show='')
        else:
            e3.configure(show='*')

    pin_checkbox = ctk.CTkCheckBox(frame, text="Show Password", fg_color='red', font=('verdana', 11),
                                   command=show_and_hide)
    pin_checkbox.grid(row=1, column=2, pady=12, padx=10, sticky="w")

    # Login Button
    b = ctk.CTkButton(frame, text="Submit", command=lambda: check_log_in(login_wind, e2.get().strip(), e3.get().strip()))
    b.grid(row=2, column=0, pady=12, padx=10, sticky="e")

    # Forgot Password Button
    forgot_button = ctk.CTkButton(frame, text="Forgot Password", command=lambda: forgot_password(login_wind))
    forgot_button.grid(row=2, column=1, pady=12, padx=10)

    # Back Button
    b1 = ctk.CTkButton(frame, text="Back", command=lambda: home_return(login_wind))
    b1.grid(row=2, column=2, pady=12, padx=10, sticky="w")
    login_wind.bind("<Return>", lambda x: check_log_in(login_wind, e2.get().strip(), e3.get().strip()))


def reset_pass(master, passw):
    print(passw)
    
    
# Add this function for handling forgotten passwords
def forgot_password(master):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    forgotPassword_wind = ctk.CTkToplevel()
    forgotPassword_wind.geometry("200x200")
    forgotPassword_wind.title("Forgot Password")
    
    l1 = ctk.CTkLabel(forgotPassword_wind, text="Enter Account number: ")
    e1 = ctk.CTkEntry(forgotPassword_wind)
    l1.grid(row=0, column=0, padx=10, pady= 10, sticky="e")
    e1.grid(row=0, column=1, padx=10, pady= 10, sticky="e")

    l2 = ctk.CTkLabel(forgotPassword_wind, text="Enter New Password: ")
    e2 = ctk.CTkEntry(forgotPassword_wind)
    l2.grid(row=1, column=0, padx=1, pady= 10, sticky="e")
    e2.grid(row=1, column=1, padx=10, pady= 10, sticky="e")
    
    l3 = ctk.CTkLabel(forgotPassword_wind, text="Connfirm New Password: ")
    e3 = ctk.CTkEntry(forgotPassword_wind)
    l3.grid(row=2, column=0, padx=10, pady= 10, sticky="e")
    e3.grid(row=2, column=1, padx=10, pady= 10, sticky="e")
    
    reset_button = ctk.CTkButton(forgotPassword_wind, text="Reset", command=lambda: reset_pass(forgotPassword_wind, e2))
    reset_button.grid(row=3, column=1, padx=10, pady= 10, sticky="e")
    forgotPassword_wind.bind("<Return>", lambda x: reset_pass(forgotPassword_wind, e2))

    # Implement the logic for forgotten passwords here
    #CTkMessagebox(title="Forgot Password", message="Sorry, this feature is not implemented yet.", icon="info")


# Register a new user window
def signup():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    signup_wind = ctk.CTkToplevel()
    signup_wind.geometry("570x600")
    signup_wind.title("Create Account")

    # Title/Heading
    l_title = ctk.CTkLabel(master=signup_wind, text="CodeX   Banking   System", font=('Times New Roman Bold', 20))
    l_title.pack(pady=20)

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/Sign.jpg"), size=(200, 200))
    disply_icon = ctk.CTkLabel(signup_wind, image=icon, text='').pack(padx=20, pady=20)

    # Details Frame
    frame = ctk.CTkFrame(master=signup_wind)
    frame.pack(pady=20, padx=40, fill='both', expand=False)

    # Enter Name
    l1 = ctk.CTkLabel(frame, text="Enter Name:")
    l1.grid(row=0, column=0, pady=12, padx=10)
    e1 = ctk.CTkEntry(frame)
    e1.grid(row=0, column=1, pady=12, padx=10)

    # Enter the opening amount
    l3 = ctk.CTkLabel(frame, text="Enter opening amount:")
    l3.grid(row=1, column=0, pady=12, padx=10)
    e2 = ctk.CTkEntry(frame)
    e2.grid(row=1, column=1, pady=12, padx=10)

    # Display and Generate PIN
    generated_pin_label = ctk.CTkLabel(frame, text="Generated Password:")
    generated_pin_label.grid(row=2, column=0, pady=12, padx=10)

    e3 = ctk.CTkEntry(frame, show="*")
    e3.grid(row=2, column=1, pady=12, padx=10)
    
    def generate_pin():
        
        # Initializing our character values
        lowerCase = "abcdefghijklmnopqrstuvwxyz"
        upperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers = "0123456789"
        symbols = "!@#$%^&*()."

        # The string variable is created by concatenating all these character sets
        string = lowerCase + upperCase + numbers + symbols

        # The length variable specifies the desired length of the password.
        length = 16

        # Randomly shuffle the characters in the string
        shuffled_string = ''.join(random.sample(string, len(string)))

        # Randomly select length number of characters from the shuffled string
        password = ''.join(random.sample(shuffled_string, length))
        
        # random_pin = str(random.randint(1000, 9999))
        e3.delete(0, 'end')  # Clear any existing PIN in the entry field
        e3.insert(0, password)  # Insert the generated PIN into the entry field

    # Show and Hide Pin
    def show_and_hide():
        if e3.cget('show') == '*':
            e3.configure(show='')
            
        else:
            e3.configure(show='*')
            

    pin_checkbox = ctk.CTkCheckBox(frame, text="Show Password", fg_color='red', font=('verdana', 11),
                                command=show_and_hide)
    pin_checkbox.grid(row=4, column=0, pady=12, padx=10)

    # Generate PIN Button
    generate_pin_button = ctk.CTkButton(frame, text="Generate Password", command=generate_pin)
    generate_pin_button.grid(row=4, column=1, pady=12, padx=10)

    # Sign up Button
    b = ctk.CTkButton(frame, text="Submit", command=lambda: write(signup_wind, e1.get().strip(), e2.get().strip(), e3.get().strip()))
    b.grid(row=4, column=2, pady=12, padx=10)

    # Back Button
    b1 = ctk.CTkButton(signup_wind, text="Back", command=signup_wind.destroy)
    b1.grid(row=5, column=2, pady=12, padx=10)

    signup_wind.bind("<Return>", lambda x: write(signup_wind, e1.get().strip(), e2.get().strip(), e3.get().strip()))
    return


# Welcome/Main Window
def Main_Menu():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    rootwn = ctk.CTkToplevel()
    rootwn.geometry("500x500")
    rootwn.title("CodeX Banking System")

    # Title
    l_title = ctk.CTkLabel(master=rootwn, text="CodeX   Banking   System", font=('Times New Roman Bold', 20))
    l_title.pack(pady=20)

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/X.png"), size=(200, 200))
    disply_icon = ctk.CTkLabel(rootwn, image=icon, text='').pack(padx=20, pady=20)

    # Sign up button
    b1 = ctk.CTkButton(rootwn, text="Sign Up", command=signup)
    b1.pack(pady=12, padx=10)

    # Login Button
    b2 = ctk.CTkButton(rootwn, text="Login", command=lambda: log_in(rootwn))
    b2.pack(pady=12, padx=10)

    # Quite Button
    b6 = ctk.CTkButton(rootwn, text="Exit", command=rootwn.destroy)
    b6.pack(pady=12, padx=10)

    rootwn.mainloop()


Main_Menu()


'''
  Validate all user inputs
  Forgot password button & logic
  Connect to database
  - Invest button
'''
