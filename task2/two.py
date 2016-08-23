string="ololo"
def polindrom (s):
   # print(s[:len(s)//2:1])
   # print(s[len(s):len(s)//2:-1])
    if s[:len(s)//2:1] == s[len(s):len(s)//2:-1]:
        return print("The String is polindrome")
    else:
        return print("The String is not polindrome")

polindrom(string)

