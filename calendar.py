# -*- coding: utf-8 -*-
import datetime
import sqlite3

# 今日の日付データを代入
today = datetime.date.today()

# 空のリストを作成
day = []
month = []
year = []

# 今日の年、月、日、を代入
today_year = int(today.year)
today_month = int(today.month)
today_day = int(today.day)

# DBに接続する
conn = sqlite3.connect("zemi.db")
cur = conn.cursor()

# 5年分のリストを追加
for i in range(1, 32):
    day.append("")

for i in range(1, 13):
    hoge = day[:]
    month.append(hoge)

for i in range(1, 5):
    hoge = month[:]
    year.append(hoge)

# DBにあるデータをリストに入れる
cur.execute("select * from calendar")
for row in cur:
    db_day = row[0]
    db_day_split = db_day.split("-")
    db_year = int(db_day_split[0])
    db_month = int(db_day_split[1])-1
    db_day = int(db_day_split[2])-1
    db_title = row[1]
    db_place = row[2]
    db_time = row[3]
    db_content = row[4]
    db_event = {
            "タイトル": db_title,
            "場所": db_place,
            "時間": db_time,
            "詳細内容": db_content
            }
    db_year = db_year - today_year
    if len(year[db_year][db_month][db_day]) != 0:
        year[db_year][db_month][db_day].append(db_event)
    else:
        year[db_year][db_month][db_day] = [db_event]
cur.close()

while True:
    # 日付を入力してもらう
    while True:
        try:
            time = str(input("日付を入力してください (入力例:2017-12-26) :"))
            hoge = time.split("-")
            # 入力してもらった日付データを分割
            select_year = int(hoge[0])
            select_month = int(hoge[1])-1
            select_day = int(hoge[2])-1
            break
        except ValueError:
            print("入力例に従って入力してください")
            print()
            # 入力してもらった年と現在の年の差を出す
    diff_year = select_year-today_year

    if year[diff_year][select_month][select_day] == ""\
       or not year[diff_year][select_month][select_day]:

        # 予定を入力してもらう
        print()
        print("予定を入力してください")
        title = input("タイトル :")
        place = input("場所 :")
        event_time = input("時間 :")
        event_detile = input("詳細内容 :")

# 予定を辞書型にする
        event = {
                "タイトル": title,
                "場所": place,
                "時間": event_time,
                "詳細内容": event_detile
                }

# 選択した日に何も予定がなければイベントを追加する
        year[diff_year][select_month][select_day] = [event]
        choice_day = year[diff_year][select_month][select_day]
        print()
        print("予定を追加しました。")
        print("タイトル：", choice_day[0]["タイトル"])
        print("場所：", choice_day[0]["場所"])
        print("時間：", choice_day[0]["時間"])
        print("詳細内容：", choice_day[0]["詳細内容"])
        day_data = (time, title, place, event_time, event_detile)
        conn.execute("insert into calendar values(?, ?, ?, ?, ?)", day_data)
        conn.commit()
# 予定が一つでも入っていた場合は選択肢を出す
    else:
        print("0:予定を見る  1:予定を追加する  2:予定を削除する")
        select_number = int(input("上記の数字から選択してください :"))

        while True:
            if select_number == 0:
                for i in range(len(year[diff_year][select_month][select_day])):
                    choice_day = year[diff_year][select_month][select_day][i]
                    print(i)
                    print("タイトル：", choice_day["タイトル"])
                    print("場所：", choice_day["場所"])
                    print("時間：", choice_day["時間"])
                    print("詳細内容：", choice_day["詳細内容"])
                break

            elif select_number == 1:
                print("予定を入力してください")
                title = input("タイトル:")
                place = input("場所:")
                event_time = input("時間:")
                event_detile = input("詳細内容:")
                event = {
                        "タイトル": title,
                        "場所": place,
                        "時間": event_time,
                        "詳細内容": event_detile
                        }
                year[diff_year][select_month][select_day].append(event)
                day_data = (time, title, place, event_time, event_detile)
                conn.execute("insert into calendar values\
                                (?, ?, ?, ?, ?)", day_data)
                conn.commit()
                break

            elif select_number == 2:
                print("どの予定を削除しますか？")

    # 現在ある予定を表示する
                for i in range(len(year[diff_year][select_month][select_day])):
                    choice_day = year[diff_year][select_month][select_day]
                    print(i)
                    print("タイトル：", choice_day[i]["タイトル"])
                    print("場所：", choice_day[i]["場所"])
                    print("時間：", choice_day[i]["時間"])
                    print("詳細内容：", choice_day[i]["詳細内容"])

    # 削除したい予定の番号を入力してもらう
                while True:
                    try:
                        drop_index = int(input("削除したい予定の番号を入力してください :"))
                        del_title = (time, choice_day[drop_index]["タイトル"])
                        del choice_day[drop_index]
                        conn.execute("delete from calendar where\
                        day = ? and title = ?", del_title)
                        conn.commit()
                        break
                    except ValueError:
                        print("表示されている番号から選んでください")
                break

            else:
                print("上記の数字以外を選ばないでください")

    conti_end = str(input("0:続けますか？  1:終了しますか？ :"))

    if conti_end != "0":
        print("終了します")
        conn.close()
        break
