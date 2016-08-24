string = "ololo"


def palindrome(s):
   # print(s[:len(s)//2:1])
   # print(s[len(s):len(s)//2:-1])
    if s[:len(s) // 2:1] == s[len(s):len(s) // 2:-1]:
        return print("The String is palindrome")
    else:
        return print("The String is non palindrome")

palindrome(string)
