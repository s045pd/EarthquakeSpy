import moment as m
import os


# current = "2018-05-03"
#
# def main():
#     endtime = m.date(current)
#     while endtime < m.now():
#         endtimestr = endtime.format("YYYY-MM-DD")
#         with open(endtimestr,"w") as f:
#             f.write("")
#         endtime = endtime.add(days=3)

def main():
    import requests
    print(requests.get("http://www.baidu.com").text)
        
if __name__ == '__main__':
    main()