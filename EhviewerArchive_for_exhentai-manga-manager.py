import re
import json
import sqlite3
import sys

eplanation='本用于bookList.json中的title字段(格式:gid-标题)中获取gid，和coverHash字段i_dump.sqlite之中修改相同gid的thumb值。注意修改后的thumb字段是格式为:https://ehgt.org/99/1d/coverHash-99999-9999-9999-jpg_l.jpg'

# 打开数据库连接
try:
    conn = sqlite3.connect('api_dump.sqlite')
    cursor = conn.cursor()
except FileNotFoundError:
    print("不存在api_dump.sqlite这个文件")
    sys.exit()

# 读取 bookHashMetadata.json 文件
try:
    with open('bookList.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    try:
        with open('bookHashMetadata.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("不存在bookList.json这个文件")
        sys.exit()
   
total,failures,success=0,0,0
# 遍历数据，更新数据库
for item in data:
    title = item.get('title')
    total += 1
    # 通过正则表达式提取 gid
    match = re.match(r'^(\d+)-', title)
    if not match:
        # 如果 title 不是以数字开头，则跳过
        print("失败,从 "+title+" 中提取字段gid")
        failures += 1
        continue
    gid = int(match.group(1))
    coverhash = item.get('coverHash')
    # 更新数据库中 gid 对应的 thumb 字段
    print("成功,从 "+title+" 中提取字段gid,替换sqlite中gid对应的Thumb字段中的hash值")
    success += 1
    newthumb="https://ehgt.org/99/99/"+coverhash+"-99999-9999-9999-jpg_l.jpg"
    conn.execute('UPDATE gallery SET thumb=? WHERE gid=?', (newthumb, gid))
    #print("修改后的thumb："+newthumb)
    
    
   
# 提交更改并关闭数据库连接
print("运行次数:",total,"失败次数:",failures,"成功次数:",success)
conn.commit()
conn.close()