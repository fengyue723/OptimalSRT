import os
import re
from queue import Queue
from datetime import time
import datetime

filePath = '.'
movie_type = ".mkv"
subtitle_type = ".srt"

strinfo = re.compile('{.*?}')

# print(os.listdir())

target_names = []
sub_file = []

def time_shrink(ori_time):
    s, ms = ori_time.split(",")
    if int(ms) > 0:
        return s + "," + "%03d"%(int(ms)-1)
    else:
        base = time(0,0,1)
        h,m,s = s.split(":")
        a = time(int(h),int(m),int(s))
        fin_time =  str(time_diff(a, base))
        fin_time = ":".join(["%02d"%int(p) for p in fin_time.split(":")]) +",999"
        return fin_time

def time_diff(t1, t2):
    today = datetime.date.today()
    return (datetime.datetime.combine(today, t1) - datetime.datetime.combine(today, t2))

for filename in os.listdir():
    if movie_type in filename:
        target_names.append(filename)
    elif subtitle_type in filename:
        sub_file.append(filename)

if len(target_names) != len(sub_file):
    print("Length connot match!")
else:
    if  subtitle_type == ".srt":
        for a,b in zip(sub_file, target_names):
            print(a,b)
            
            time_zone_queue = Queue(maxsize=5)

            with open(a, "r", encoding="utf-8") as fin:
                with open(a[:-4]+"_001"+subtitle_type,"w", encoding="utf-8") as fout:
                    for line in fin:
                        new_line = strinfo.sub('', line)
                        if "-->" in new_line:
                            if new_line in time_zone_queue.queue:
                                new_line_list = new_line.split()
                                new_line = " ".join(new_line_list[:-1] + [time_shrink(new_line_list[-1])])+"\n"
                                # print("xxxxxxxxxxx", time_zone_queue.queue)
                            if time_zone_queue.full():
                                time_zone_queue.get()
                            time_zone_queue.put(new_line)
                        fout.write(strinfo.sub('', new_line))
            
            # 删除原字幕
            os.remove(a)
            os.rename(a[:-4]+"_001"+subtitle_type, b[:-4]+subtitle_type)
    elif subtitle_type == ".ass":
        pass