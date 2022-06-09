# a = [1,3,5,7]
# b = [4,3,2,1]
# for i in range(len(a)):
#     a[i] += b[i]

# # print(a)a
# a = ['46 seconds ago', '3 days ago', '7 days ago']
# for i in a :
#     if 'minutes'  in i or 'secounds' in i:  
#         print('yes')
#     else:print('Noo')


# b = '46 hours  ago' 
# # if 'minutes'  or 'hours' or 'seconds' and 'ago' in b:
# if  'hours' and 'ago' in b:
#     print(22)

# a = 0
# b = 0
# c = 0
# d = 0
# if (a or b or c or d) > 0:print('yess')
# else:print('Noo')


# a = 'True'
# print(type(bool(a)))

import asyncio
import os
import urllib.request
 
async def download_coroutine(url):
    #"A coroutine to download the specified url"
    request = urllib.request.urlopen(url)
    filename = os.path.basename(url)
 
    with open(filename, 'wb') as file_handle:
        while True:
            chunk = request.read(1024)
            if not chunk:
                break
            file_handle.write(chunk)
    msg = 'Finished downloading {filename}'.format(filename=filename)
    return msg
 
async def main(urls):
    """
    Creates a group of coroutines and waits for them to finish
    """
    coroutines = [download_coroutine(url) for url in urls]
    completed, pending = await asyncio.wait(coroutines)
    for item in completed:
        print(item.result())
 
 
if __name__ == '__main__':
    urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"]
 
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(urls))
    finally:
        event_loop.close()