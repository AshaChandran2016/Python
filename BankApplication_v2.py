import os.path    # imported for file operations

def main():       # Menu
    getMenu()

def getMenu():
    print("Bank account application")
    print("1) Create new account")
    print("2) Credit/Debit an account")
    print("3) List all accounts")
    print("4) List account history")
    todo = eval(input("What would you like to do:"))  # Functions called below based on the option selected
    transactions(todo)
    proceed = (input("Do you want to proceed (Y/N)? "))
    if proceed == "Y":
        getMenu()
    else:
        print("Thanks for your business. Have a nice day!")

def transactions(todo):
    if todo == 1:
        createAccount()
    elif todo == 2:
        creditDebit()
    elif todo == 3:
        listAccounts()
    elif todo == 4:
        accNo = eval(input("Enter Account Number:"))
        accountHistory(accNo)

def extractFiles(fileName, header=""):
    if os.path.isfile(fileName):
        accFile = open(fileName, 'r+')
    else:
        accFile = open(fileName, 'w+')
        accFile.write(header)
    return accFile

def transFile(fileName, header=""):
    if os.path.isfile(fileName):
        accFile = open(fileName, 'a+')
    else:
        accFile = open(fileName, 'w+')
        accFile.write(header)
    return accFile

def closeFile(fileObject):
    fileObject.close()

def createAccount():    # Function for creating the account
    print("Creating a new account...")
    print("Please enter the individuals")
    fName = input("First Name: ")
    lName = input("Last Name: ")
    beginningBalance = eval(input("Beginning Balance (USD): "))
    AccNo = []
    maxAccNo = 0
    accHeader = "AccNo, FirstName, LastName, Balance\n"
# If the accountsummary file dont exist then create else open to read and append
    accFile = extractFiles("Bank\AccountSummary.csv", accHeader)
    for line in accFile:
        AccNo.append(line.split(',')[0])
    if len(AccNo) >= 2:
        maxAccNo = int(AccNo[-1])
        maxAccNo += 1
        newAcc = str(maxAccNo) + " ," + fName + " ," + lName + " ," + str(beginningBalance)+"\n"
        accFile.write(newAcc)
        print("New account created for " + fName + " " + lName + "(Account: " + '{0:0>3s}'.format(str(maxAccNo)) + ")")
    else:
        maxAccNo = 1
        newAcc = "1" + " ," + fName + " ," + lName + " ," + str(beginningBalance)+"\n"
        accFile.write(newAcc)
        print("New account created for " + fName + " " + lName + "(Account: 001)")

    transactionHeader = "AcctNo ,Balance , TransactionAmount\n"
    transactionDetails = transFile("Bank\Transaction_Details.csv",transactionHeader)
    transactionDetails.writelines(str(maxAccNo) + " ," + str(beginningBalance) + " ,0\n")

    transactionDetails.close()
    accFile.close()


# Function to perform credit/debit
def creditDebit():
    print("Crediting/Debiting an account...")
    accNo = eval(input("Please enter the account number: "))
    accSummary = extractFiles("Bank\AccountSummary.csv")
    newAccSummary = extractFiles("Bank\AccountSummary_new.csv")
    transactionDetails = transFile("Bank\Transaction_Details.csv")
    accFound = False
    for line in accSummary:
        # print([line.split(',')[0].rstrip(), accNo])
        eachAcc = line.split(',')
        if eachAcc[0].rstrip() == str(accNo):
            accFound = True
            fName = eachAcc[1]
            print("Welcome " + fName)
            balance = int(eachAcc[-1])
            Amount = 0
            newBalance = 0
            strAmount = ""
            print("Your Account Balance is " + str(balance))
            tranType = input("What would you like to do (Credit or Debit): ")
            if tranType.rstrip().upper() == "CREDIT" or tranType.rstrip().upper() == "DEBIT":
                Amount = eval(input("Please enter the amount:"))
                if tranType.rstrip().upper() == "CREDIT":
                    newBalance = balance + int(Amount)
                    eachAcc[-1] = str(newBalance)
                    strAmount = str(Amount)
                else:
                    newBalance = balance - int(Amount)
                    eachAcc[-1] = str(newBalance)
                    strAmount = "-" + str(Amount)

                newline = ""
                for each in eachAcc:
                    newline += each + ","
                newAccSummary.writelines(newline[:-1]+"\n")
                print(fName + ", your account is " + tranType + "ed and new Balance is " + str(eachAcc[-1]))
                transactionDetails.write(eachAcc[0]+" ,"+str(balance) + " ,"+strAmount+"\n")
                transactionDetails.write(eachAcc[0]+" ,"+str(newBalance) + " ,0\n")
            else:
                print("Your entry is invalid. Please try again!")
                newAccSummary.writelines(line)
        else:
            newAccSummary.writelines(line)
    closeFile(newAccSummary)
    closeFile(accSummary)
    os.remove("Bank\AccountSummary.csv")
    os.rename("Bank\AccountSummary_new.csv", "Bank\AccountSummary.csv")
    closeFile(transactionDetails)
    if not accFound:
        print("The account does not exist. Please create an account first!")


# Function to list all the accounts
def listAccounts():
    print("Listing accounts...")
    accSummary = extractFiles("Bank\AccountSummary.csv")
    header = accSummary.readline()
    if header != "":
        for eachAccount in accSummary:
            eachDetails = eachAccount.split(',')
            print(eachDetails[0], eachDetails[1], eachDetails[2], '${0:.2f}'.format(float(eachDetails[3])))
        accSummary.close()
    else:
        print("No accounts to display!")
        accSummary.close()
        os.remove("Bank\AccountSummary.csv")


# Function to list all the account history
def accountHistory(accNum):
    print("Transaction history")
    if os.path.isfile("Bank\Transaction_Details.csv"):
        transDetails = open("Bank\Transaction_Details.csv", 'r')
        fName, lName = "", ""
        (fName, lName) = accountDetails(accNum)
        print(str('{:03d}'.format(accNum)) + '\t' + fName + ' '+lName)
        for line in transDetails:
            eachDetails = line.split(',')
            if eachDetails[0].rstrip() == str(accNum):
                if eachDetails[-1].rstrip() != "0":

                    if int(eachDetails[-1].rstrip()) < 0:
                        transSign = eachDetails[-1][0]
                        transAmount = eachDetails[-1][1:]
                    else:
                        transSign = "+"
                        transAmount = eachDetails[-1]
                    # print(transAmount)
                    print('${0:.2f}'.format(float(eachDetails[-2])), transSign + " " + '${0:.2f}'.format(float(transAmount)))
                finalbalance = eachDetails[-2]
        print('${0:.2f}'.format(float(finalbalance)))
    transDetails.close()

# Function to display account details, which can be used in any other functions as needed
def accountDetails(acctNo):
    accSummary = open("Bank\AccountSummary.csv", 'r')

    for line in accSummary:
        eachAcc = line.split(',')
        if eachAcc[0].rstrip() == str(acctNo):
            fName = eachAcc[1]
            lName = eachAcc[2]
    accSummary.close()
    return (fName, lName)
# Calling main function which inturn invoke all other functions as per business inputs


main()


