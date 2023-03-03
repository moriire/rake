# Rake
## _Whois on command line_
Rake is a domain level information gathering tool

![N|Solid](./assets/rake_windows.PNG)

## Installation
### Windows
```sh
git clone --depth 1 https://www.github.com/moriire/rake
cd rake
sudo install.sh
```
### Linux
```sh
git clone --depth 1 https://www.github.com/moriire/rake
cd rake
python setup.py install
```
## Usage
#### Commands
--- info - Domain name information
--- gui - Rake gui interface
--- cloner - Website cloner
```sh
rake info --url www.domain.tld
rake info --url www.domain.tld --o raw|table\n\t
rake info --url www.domain.tld --o raw|table ./name.txt      
            
rake cloner  --url www.doamin.tld 
rake cloner --url www.domain.tld ./web/about.html

rake gui
 ```

### To get detail infomation about a specific domain name
```sh
rake info --url domain-name -o raw|table   myfilename.ext
supported ext - txt, csv, json
```
### OR

### GUI option
```sh
rake gui
```
### To clone a specific url
```sh
rake clone --url domain-name  myfilename.ext
```