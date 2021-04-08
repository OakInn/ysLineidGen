- [How to run](#how-to-run)
  - [How to run tests (recommended)](#how-to-run-tests-recommended)
  - [How to run (recommended)](#how-to-run-recommended)
- [General information](#general-information)
  - [Requirements](#requirements)
  - [Description](#description)
  - [INFORMATION BELOW](#information-below)
    - [Parameter values:](#parameter-values)
    - [Parameters:](#parameters)
- [Project current status](#project-current-status)

# How to run
## How to run tests (recommended)

docker build -t python3gametest .  
docker run --rm python3gametest 


## How to run (recommended)

docker run --rm -v {pathToFiles}:/opt/yarn python3gametest  
:warning: BUT before you run - READ THROUGH **INFORMATION BELOW** section.


# General information

This project is a part of Game development suite. It is dedicated to work with Yarn Spinner dialogue tool.
**[Yarn Spinner](https://yarnspinner.dev/)** is a tool for writing game dialogues.  
All Yarn Spinner files are subjects for game localization process. For proper localization, particular lines of Yarn Spinner file should be marked for translation with a *[unique identifier](https://yarnspinner.dev/docs/unity/localisation/)*.  
This standalone tool parses Yarn Spinner dialogue files and inserts missing localization identifiers. It detects conflicts and tries to resolve them as well.


## Requirements

**OS** - Linux/Mac/Windows  
**Python** - 3.6 or above  
**Additional python library** - libscrc 1.3 or above (*pip install libscrc*)  


## Description

Program collects all the files in folder(s) (recursively) by file extension(s).  
*Both folder path and file extension(s) are user specified*.  
Creates backup copies (*WIP - Arguments*).  
Processes data in files line-by-line. Finds all lineIDs that already exist and checks:  
1. that they are of valid hexadecimal type.  
   If not - log as conflict.
2. that existing lineID is unique through all the files.  
   If not - log as conflict.
In case user decided not to resolve existing conflicts and they were found - program will terminate (*WIP - process termination*).
If user defined to resolve conflicts, or there were none found - program
will then analyze the data again. This time it will:  
    - Check if line has lineID:
      - if there is a lineID:
        - check if it is present among the conflicts:
          - if among conflicts:
            - look to the value of "compat" parameter and generate corresponding new lineID
          - if not among conflicts:
            - check if its length complies with "compat" parameter:
              - if complies - go to the next line
              - if does not comply - generate corresponding new lineID
      - If there is no lineID present:
        - decide if the line needs it:
          - if does not need line ID - skip the line
          - if does need line ID - check "newcompat" parameter value and generate corresponding new lineID
1. Change the line in accordance with the results of previous steps above (if needed).
Line formatting is kept as it was.
4. Re-write files with new data.
5. Provide results and metrics (*WIP*)


## INFORMATION BELOW
In *SetLineid.py* file there are some parameters, which should be revised:  
1. **variable "path"** - path to the folder with files.  
*example "/etc/folderName/folderName/", "C:\\folderName\\folderName\\"*
2. **variable "fileExt"**- set/list of file extensions.  
*example {".yarn", ".yarn.txt"}*
3. **generatorArguments** - parameters and their values.  
*example {"compat": "yarn", "resolve": "long", "newcompat": "yarn"}*

### Parameter values:
:warning: Parameter values are not final  
1. **"yarn"** - length of generated lineID hexadecimal is *3 bytes (6 characters)*
2. **"long"** - length of generated lineID hexadecimal is *8 bytes (16 characters)*
3. **"None"** - parameter with *"None"* value will take default value, or parameter  
is not used, or not applicable.

### Parameters:
:warning: Value *"None"* is currently not supported in any of the parameters!  
1. **"compat"** - general compatibility.  
**Default value** - *"yarn"*.  
If set to *"yarn"* or *"long"* - all present lineIDs will we re-generated to comply with inserted value.  
If set to *"None"* - present lineIDs will stay as they are.  
2. **"resolve"** - whether to resolve found conflicts.  
**Default value** - *"yarn"*.  
If "resolve" set to *"yarn"(default)* or *"long"* - generate lineID of 
appropriate length (see Parameter values above).  
If *"resolve"* set to *"None"* - if conflict are found - program should terminate  
and inform of the problem, without setting any lineIDs.  
3. **"newcompat"** - all lines which do not have lineID, but should have one -  
will be generated of a chosen length - *"yarn"(default)* or *"long"*.  
**Default value** - *"yarn"*.  


# Project current status

**WIP**:
- [ ] **Arguments** - receive parameters and their values from command line (terminal)
- [ ] **Metrics** - general information and results.