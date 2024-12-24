# Missing newline at the end of file
![image](https://github.com/user-attachments/assets/2b6fc0b6-7fe5-492c-ae06-ff8b61357f12)
## In Fedora you can install it like this:
```
sudo dnf install gem
gem install git-newline-at-eof
```
After that you can use all the commands provided in the documentation, for example:
```
$ git newline-at-eof --check-all | grep "no newline"
I_RCPTransport/Makefile.am: no newline at end of file
I_RCPTransport/trs_iwf.pc.in: no newline at end of file
config/85-trs_fp.preset: no newline at end of file
lib/libBIP/include/bip_bicmp.h: no newline at end of file
lib/libBIP/include/bip_stream.h: no newline at end of file
<clipped as the output was too long>
```
And you can fix all those problems with single command as well:
```
$ git newline-at-eof -a
```
## Trailing white spaces
![image](https://github.com/user-attachments/assets/64c35cd2-5989-49fd-8e76-8c4a0f216e53)
### How to fix the error
1. You can fix such a change with `git rebase --whitespace=fix HEAD~1` this will fix all the whitespace errors in the last commit.
2. VSCode
Click toolbar of the left bottom, choose "Spaces", and then select "Trim Trailing Whitespace" in "Select Action" listbox
![image](https://github.com/user-attachments/assets/a9373df0-7271-45d8-ba23-6fc4ce0ef924)
3. NotePad++
   ![image](https://github.com/user-attachments/assets/7de559b3-66ae-4597-b0b1-536ad657b785)
## Line endings change
![image](https://github.com/user-attachments/assets/c0e0167a-f3c5-4321-a2b8-a20b33a69e3e)
### How to fix the error
In Unix, it is very easy to fix the error.
```
$ dos2unix vagentsecret.cpp
dos2unix: converting file vagentsecret.cpp to Unix format...
$ file vagentsecret.cpp
vagentsecret.cpp: C source, ASCII text
```
![image](https://github.com/user-attachments/assets/b1f04875-dc52-435b-8209-f97116f93aff)

## Replace tab with 4 spaces
### How to fix the error
![image](https://github.com/user-attachments/assets/f7a884b2-a681-49b0-b96d-3342dead1e4e)
![image](https://github.com/user-attachments/assets/76cf8c92-d2f8-47e8-9db3-edf89716acdc)  
[replace-tab-by-space-or-replace-spaces-by-tab-in-linux](https://songhuiming.github.io/pages/2016/07/31/replace-tab-by-space-or-replace-spaces-by-tab-in-linux/)

## astyle usage
astyle:  A Free, Fast, and Small Automatic Formatter for C, C++, C++/CLI, Objective‑C, C#, and Java Source Code
link: http://astyle.sourceforge.net/
![image](https://github.com/user-attachments/assets/a663abd1-b529-44fe-ab17-867a9740dcd8)


