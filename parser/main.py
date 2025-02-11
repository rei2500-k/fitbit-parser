import csv
import datetime
import os
import re


def main():
    INPUT_FILE = './fitbit_files/steps/steps_2025-02-01.csv'
    
    # CSV取得
    with open(INPUT_FILE) as f:
        # ファイル名から最初の行の時刻を生成
        print(os.path.basename(INPUT_FILE))
        # 正規表現でYYYY-MM-DDを取得
        DATE_PATTERN = re.compile(r'(\d{4}-\d{2}-\d{2})')
        date = re.findall(DATE_PATTERN, os.path.basename(INPUT_FILE))

        first_timestamp = f'{date[0]}T00:00:00Z'
        print(first_timestamp)


        # 歩数ファイルは1分毎に行が作成されるが、歩数0の行は作成されない。
        # そのため、前の行との差が1分より大きい場合は、歩数0の行を補完する。
        
        # ヘッダー除外
        reader = csv.reader(f)
        header = next(reader)

        last_timestamp = first_timestamp
        
        for row in reader:
            print(row)

            # 補完対象判定
            if datetime.datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%SZ') - datetime.datetime.strptime(last_timestamp, '%Y-%m-%dT%H:%M:%SZ') > datetime.timedelta(minutes=1):
                print('補完対象')
                print(row[0])
                print(last_timestamp)
                # 補完処理

            last_timestamp = row[0]
            break


if __name__ == '__main__':
    main()
