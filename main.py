import inquirer
import os


WINDOWS_FIREWALL_RULE_NAME = 'Steamshare'

def printInfo():
    os.system('cls')

    print("This tool helps you manage your Steam internet connection.");
    print("When you want to play a family-shared game simultaneously, disable the connection before starting the game. This will allow both of you to play at the same time.\n")
    
    print("Before using this tool, make sure you have set up a firewall rule. Here's how:")
    print(f"""
    1. Select 'Open Windows Firewall Settings'
    2. Choose Outbound rules
    3. Create a new rule
    4. Select 'Program'
    5. Select the Steam executable (Most commonly in C:\Program Files (x86)\Steam\steam.exe" )
    6. Block the connection
    7. Check all 3: Domain, Private and Public
    8. Give the rule the name '{WINDOWS_FIREWALL_RULE_NAME}' (VERY IMPORTANT)\n""")

current = os.popen(f"netsh advfirewall firewall show rule name=\"{WINDOWS_FIREWALL_RULE_NAME}\" | findstr \"Enabled\"").read();

if (current == ''):
    printInfo()
    print("Please restart the program when you have set the rule up.")

def getStatus(status):
    if ("Yes" in status):
        return "Internet Disabled"
    if ("No" in status):
        return "Internet Enabled"

    return "RULE_NOT_SET"

def execCommand(command):
    result = os.system(command)

    # os.system returns '0' when OK, '1' when error 
    if (result == 0):
        print("Done!")

    if (result == 1):
        print("Something went wrong while executing the command")
        print("Make sure to setup the rule in the firewall settings.")
        print("Does the rule have the name 'Steamshare'. If not, it won't work.")
        print("kthxbye.")
     
while (True):
    current = os.popen(f"netsh advfirewall firewall show rule name=\"{WINDOWS_FIREWALL_RULE_NAME}\" | findstr \"Enabled\"").read();

    print("Current status: " + getStatus(current))
    
    query = [
        inquirer.List('status',
            message="Give Steam access to Internet?",
            choices=['Yes', 'No', 'Info', 'Open Windows Firewall Settings', 'Exit'],
        ),
    ]

    prompt = inquirer.prompt(query)

    answer = prompt['status']

    if (answer == 'Yes'):
        execCommand('netsh advfirewall firewall set rule name="Steamshare" new enable=no')

    if (answer == 'No'):
        execCommand('netsh advfirewall firewall set rule name="Steamshare" new enable=yes')

    if (answer == 'Info'):
        printInfo()

    if (answer == 'Open Windows Firewall Settings'):
        execCommand('wf.msc')

    if (answer == 'Exit'):
        exit(0)

    

 