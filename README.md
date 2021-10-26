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
- [External sources](#external-sources)
  - [Protoargs](#protoargs)

# How to run

Navigate to the Docker file location.

## How to run tests (recommended)

docker build -t {ImageName} .
- Example -> docker build -t python3gametest .

docker run --rm {ImageName}
- Example  -> docker run --rm python3gametest  


## How to run (recommended)

:warning: Before you "run" - READ THROUGH **INFORMATION BELOW** section.

docker run --rm -v {pathToFiles}:/opt/yarn -v {pathToFolderForBackups}:/opt/backup python3gametest /opt/yarn --BCKP /opt/backup


# General information

This project is a part of Game development suite. It is dedicated to work with Yarn Spinner dialogue tool.

**[Yarn Spinner](https://yarnspinner.dev/)** is a tool for writing game dialogues.

All Yarn Spinner files are subjects to game localization process. For proper localization, particular lines of Yarn Spinner file should be marked for translation with a *[unique identifier](https://yarnspinner.dev/docs/unity/localisation/)*.

This standalone tool parses Yarn Spinner dialogue files and generates missing or replaces existing localization identifiers. It detects conflicts and tries to resolve them as well (if the appropriate option was enabled).


## Requirements

**OS** - Linux/Mac/Windows  
**Python** - 3.6 or above  
**Additional python library** - libscrc 1.3 or above (*pip install libscrc*)  


## Description

Program collects all the files in folder(s) (recursively) by file extension(s).

*Both folder path and file extension(s) are user specified*. Though, files should be of a text format.
Also, default extensions are .yarn and .txt.

Creates backup copies at a specified folder, or if not specified - at the same
folder as the source files.

Data is processed in files line-by-line. Program finds all lineIDs that already exist and checks:
1. that they are of valid hexadecimal type. 
   If not - log as conflict.
2. that existing lineID is unique through all the files.  
   If not - log as conflict.
In case user decided not to resolve existing conflicts and they were found - program will terminate.  
If user defined to resolve conflicts, or there were none found - program
will then analyze the data again, and this time it will:  
    - Check if line has lineID:
      - if there is a lineID:
        - check if it is present among the conflicts:
          - if among conflicts:
            - look to the value of "compat" (compatibility) parameter and generate corresponding new lineID
          - if not among conflicts:
            - check if its length complies with "compat" parameter:
              - if complies - go to the next line
              - if does not comply - generate corresponding new lineID
      - If there is no lineID present:
        - decide if the line needs it:
          - if does not need lineID - skip the line
          - if does need lineID - check "newcompat" parameter value and generate corresponding new lineID.
3. Change the line in accordance with the results of previous steps above (if needed).
4. Re-write files with new data.
5. Provide results and metrics (*WIP*)


# INFORMATION BELOW

To run via Docker - change *Dockerfile*. Comment "test command" and edit and uncomment "run" command.

It is strongly recommended to specify a separate backup folder (via parameter) - as backup files are hoarded, and they may flood your source folder a little.  

You can run the *[SetLineid.py](SetLineid.py)* file without any parameters (or with *-h* parameter)
to receive a help notes for the possible parameters. Which also can be found at the *[SL.proto](SL.proto)* file:

   - required string SRC             = 1;                                    // Path to folder which contain yarn spinner files
   - optional string BCKP            = 2 [default = ""];                     // Path to folder for backing up files in SRC 
   - optional string ext	           = 3 [default = ".txt_.yarn_.yarn.txt"]; // Extensions of files for procession
   - optional string compat          = 4 [default = ""];                     // Initial lineID length check. ""/"yarn"/"long"
   - optional string resolve         = 5 [default = ""];                     // LineID length for conflict resolve. ""/"yarn"/"long"
   - optional string newcompat       = 6 [default = "yarn"];                 // Newly generated lineID length. "yarn"/"long"

### Parameter values:
1. **"yarn"** - length of generated lineID hexadecimal is *3 bytes (6 characters)*
2. **"long"** - length of generated lineID hexadecimal is *8 bytes (16 characters)*
3. **""** - empty parameter results in 'None' or default value.

### Parameters:
1. **"compat"** - general compatibility.
**Default value** - *""*.  
If set to *"yarn"* or *"long"* - present lineIDs will we re-generated (if needed) to comply with this parameter.  
If set to *""* - present lineIDs will stay as they are.  

2. **"resolve"** - whether to resolve found conflicts.  
**Default value** - *""*.  
If "resolve" set to *"yarn"* or *"long"* - generate lineID of 
appropriate length (see 'Parameter values' section above).  
If *"resolve"* set to *""* - in case conflicts are found - program will terminate  
and inform of the problem, without setting any lineIDs.  

3. **"newcompat"** - all lines which do not have lineID, but should have one -
will be generated of a chosen length - *"yarn"* or *"long"*.  
**Default value** - *"yarn"*.  


# Project current status

**WIP**:
- [x] **Arguments** - receive parameters and their values from command line (terminal)
- [ ] **Metrics** - general information and results.
- [ ] **Beauty** - minor fixes and upgrades. Like usage of relative path to the folders, restore from backup. 


# External sources

## Protoargs

For argument parsing an external code was used - **[protoargs](https://github.com/ashlander/protoargs)**.