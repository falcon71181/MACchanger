import subprocess
import winreg
import re
import codecs

print(""""

             [+] Window Mac Changer [+]
          
        ======================================= 
        [+] Programmed By : Falcon Clutch     |+
        [+] Instagram: falcon71181            |+
        [+] Youtube: Falcon Clutch            |+
        [+] Github : falcon71181              |+
        =======================================

        """)


mac_to_change_to = ["0A1122334455", "0E1122334455", "021122334455", "061122334455", "0A1122334457", "02D122334455", "0A1EA2334455", "0E112233445A", "0E11223D4455", "0EA122334455", "0DE122334A55", "DE1A22334455"]

mac_addresses = list()

macAddRegex = re.compile(r"([A-Za-z0-9]{2}[:-]){5}([A-Za-z0-9]{2})")

transportName = re.compile("({.+})")

adapterIndex = re.compile("([0-9]+)")


getmac_output = subprocess.run("getmac", capture_output=True).stdout.decode().split('\n')


for macAdd in getmac_output:
   
    macFind = macAddRegex.search(macAdd)
    
    transportFind = transportName.search(macAdd)
   
    if macFind == None or transportFind == None:
        continue
    
    mac_addresses.append((macFind.group(0),transportFind.group(0)))


print("Which MAC Address do you want to update?")
for index, item in enumerate(mac_addresses):
    print(f"{index} - Mac Address: {item[0]} - Transport Name: {item[1]}")


option = input("Select the menu item number corresponding to the MAC that you want to change:")


while True:
    print("Which MAC address do you want to use? This will change the Network Card's MAC address.")
    for index, item in enumerate(mac_to_change_to):
        print(f"{index} - Mac Address: {item}")

    
    update_option = input("Select the menu item number corresponding to the new MAC address that you want to use:")
    
    if int(update_option) >= 0 and int(update_option) < len(mac_to_change_to):
        print(f"Your Mac Address will be changed to: {mac_to_change_to[int(update_option)]}")
        break
    else:
        print("You didn't select a valid option. Please try again!")


controller_key_part = r"SYSTEM\ControlSet001\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"


with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
   
    controller_key_folders = [("\\000" + str(item) if item < 10 else "\\00" + str(item)) for item in range(0, 21)]
    
    for key_folder in controller_key_folders:
        
        try:
            
            with winreg.OpenKey(hkey, controller_key_part + key_folder, 0, winreg.KEY_ALL_ACCESS) as regkey:
                
                try:
                    
                    count = 0
                    while True:
                        
                        name, value, type = winreg.EnumValue(regkey, count)
                        
                        count = count + 1
                        
                        if name == "NetCfgInstanceId" and value == mac_addresses[int(option)][1]:
                            new_mac_address = mac_to_change_to[int(update_option)]
                            winreg.SetValueEx(regkey, "NetworkAddress", 0, winreg.REG_SZ, new_mac_address)
                            print("Successly matched Transport Number")
                            
                            break
                except WindowsError:
                    pass
        except:
            pass



run_disable_enable = input("Do you want to disable and reenable your wireless device(s). Press Y or y to continue:")

if run_disable_enable.lower() == 'y':
    run_last_part = True
else:
    run_last_part = False


while run_last_part:

    
    network_adapters = subprocess.run(["wmic", "nic", "get", "name,index"], capture_output=True).stdout.decode('utf-8', errors="ignore").split('\r\r\n')
    for adapter in network_adapters:
        
        adapter_index_find = adapterIndex.search(adapter.lstrip())
        
        if adapter_index_find and "Wireless" in adapter:
            disable = subprocess.run(["wmic", "path", "win32_networkadapter", "where", f"index={adapter_index_find.group(0)}", "call", "disable"],capture_output=True)
            
            if(disable.returncode == 0):
                print(f"Disabled {adapter.lstrip()}")
            
            enable = subprocess.run(["wmic", "path", f"win32_networkadapter", "where", f"index={adapter_index_find.group(0)}", "call", "enable"],capture_output=True)
            
            if (enable.returncode == 0):
                print(f"Enabled {adapter.lstrip()}")

    
    getmac_output = subprocess.run("getmac", capture_output=True).stdout.decode()
    
    mac_add = "-".join([(mac_to_change_to[int(update_option)][i:i+2]) for i in range(0, len(mac_to_change_to[int(update_option)]), 2)])
    
    if mac_add in getmac_output:
        print("Mac Address Spoofing................")
        print("Mac Address Success")
    
    break
