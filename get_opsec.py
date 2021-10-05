from bs4 import BeautifulSoup
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--commands', help='Beacon commands to enable (comma delimted)  Options: API-only House-keeping  bof Post-Exploitation cmd.exe  powershell.exe  remote  spawn&inject  service', type=str)
args = parser.parse_args()
my_list = [str(item) for item in args.commands.split(',')]

result = requests.get("https://www.cobaltstrike.com/help-opsec")
c = result.content

soup = BeautifulSoup(c, "lxml")

output = {}
for i in soup.findAll('p', "list"):
    k = i
    v = i.findPrevious('h3').text
    if v in output:
        output[v] = output[v] + k.text
    #v = [li.text for li in ul.findAll('li')]
    else:
        output[v] = k.text

#print(list(output.keys()))

for ttp in output.keys():
    action = "block"
    for element in my_list:
        if element.lower() in ttp.lower():
            action = "true"
            break
    print("#TTP: " + ttp)
    #print(output[ttp] + "\n")
    for line in str(output[ttp]).splitlines():
        line = line.replace("*", "")
        line = line.strip()
        #string = str(line)
        #print(string)
        #for element in my_list:
        #    if element in ttp:
        print("%%commands[\"%s\"]=\"%s\";" % (line, action))
        #    else:
        #        print("%%commands[\"%s\"]=\"block\";" % line)


rest = """
#configuring the block commands
foreach $key (sorta(keys(%commands))) {
        if (%commands[$key] eq "block") {
                alias($key, {
                        berror($1,"This command's execution has been blocked. Remove the opsec profile to run the command.");
                });
        }
}

#Adding the opsec command to check the current settings
beacon_command_register("opsec", "Show the settings of the loaded opsec profile",
        "Synopsis: opsec\n\n" .
        "Displays a list of command settings for the currently loaded opsec profile.");

alias("opsec",{
        blog($1,"The current opsec profile has the following commands set to block/block: ");
        foreach $key (sorta(keys(%commands))) {
                blog2($1,$key . " - " . %commands[$key]);
        }
});
"""

print(rest)
