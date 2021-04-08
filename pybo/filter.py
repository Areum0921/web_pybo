import locale
locale.setlocale(locale.LC_ALL,'')

def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    return value.strftime(fmt)

def format_ip(value):
    if(value):
        str_ip = str(value)
        cnt = 0
        str1 = ""
        str2 = ""
        for i in range(len(str_ip)):
            if (str_ip[i] == '.' and cnt == 0):
                str1 = str_ip[:i]
                str2 = str_ip[i:]
                cnt += 1
            if (str_ip[i] != '.' and cnt > 0):
                str2 = str2.replace(str_ip[i], '*')
        return str1 + str2
    else:
        return "주소저장x"








