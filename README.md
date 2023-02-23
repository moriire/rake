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
--- Start
--- gui
--- clone
--- stats

### To get detail infomation about a specific url
```sh
rake start --url domain-name -o raw|table|json --save txt|json|csv myfilename.ext
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

### To get a full stat of specific url
```sh
rake stats --url domain-name  myfilename.ext
```