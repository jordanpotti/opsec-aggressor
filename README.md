# opsec-aggressor
Aggressor script that gets the latest commands from CobaltStrikes opsec page and creates an aggressor script based on tool options.

Grabs latest commands from https://www.cobaltstrike.com/help-opsec and sets block/allow based on tool input. 

**Options of commands to block/allow are:**

- API-only
- House-keeping Commands
- Inline Execute (BOF)
- Post-Exploitation Jobs (Fork&Run)
- Process Execution
- Process Execution (cmd.exe)
- Process Execution (powershell.exe)
- Process Injection (Remote)
- Process Injection (Spawn&Inject)
- Service Creation

## Credit

Thanks to bluescreenofjeff and _tifkin for the original [opsec aggressor scripts](https://github.com/bluscreenofjeff/AggressorScripts/tree/master/OPSEC%20Profiles). It was more better since it rewrote some of the dropdown options but it hasn't been updated in 4 years, much has changed since then. 

## Usage 

```
usage: get_opsec.py [-h] [-c COMMANDS]

optional arguments:
  -h, --help            show this help message and exit
  -c COMMANDS, --commands COMMANDS
                        Beacon commands to enable (comma delimted) Options: API-only House-keeping bof Post-Exploitation cmd.exe powershell.exe remote spawn&inject service
```

## Example

```
$ python3 get_opsec.py -c API-only,House-keeping,bof,cmd.exe | tee opsec.cna
#TTP: API-only
%commands["cd"]="true";
%commands["cp"]="true";
%commands["connect"]="true";
%commands["download"]="true";
%commands["drives"]="true";
%commands["exit"]="true";
.
.
.
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
        "Synopsis: opsec

" .
        "Displays a list of command settings for the currently loaded opsec profile.");

alias("opsec",{
        blog($1,"The current opsec profile has the following commands set to block/block: ");
        foreach $key (sorta(keys(%commands))) {
                blog2($1,$key . " - " . %commands[$key]);
        }
});
```


