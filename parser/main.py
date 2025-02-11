import csv
import datetime
import os
import re


def get_first_timestamp(path: str) -> str:
    """ ファイルの1行目に存在して欲しい時刻を取得する。
    ファイル名からYYYY-MM-DD形式の文字列を取得しT00:00:00Zを付与して返す。

    Args:
        path (str): 歩数記録のファイルパス

    Returns:
        str: 生成時刻文字列 (YYYY-MM-DDT00:00:00Z)
    """    
    DATE_PATTERN = re.compile(r'(\d{4}-\d{2}-\d{2})')
    date = re.findall(DATE_PATTERN, os.path.basename(path))

    return f'{date[0]}T00:00:00Z'


def need_complement(last_timestamp: str, current_timestamp: str) -> bool:
    """ 前の行の時刻と現在行の時刻を比較し、補完が必要か判定する。
    前の行の時刻と現在行の時刻の差が1分より大きい場合、補完が必要と判定する。

    Args:
        last_timestamp (str): 前の行の時刻
        current_timestamp (str): 現在行の時刻

    Returns:
        bool: (True: 補完が必要, False: 補完が不要)
    """
    last = datetime.datetime.strptime(current_timestamp, '%Y-%m-%dT%H:%M:%SZ')
    current = datetime.datetime.strptime(last_timestamp, '%Y-%m-%dT%H:%M:%SZ')

    return last - current > datetime.timedelta(minutes=1)


def next_timestamp(timestamp: str) -> str:
    """ 補完用の時刻を生成する。

    Args:
        timestamp (str): 前の行の時刻

    Returns:
        str: 補完用の時刻
    """
    d_timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    next_time = d_timestamp + datetime.timedelta(minutes=1)

    return next_time.strftime('%Y-%m-%dT%H:%M:%SZ')


def main():
    INPUT_FILE = './fitbit_files/steps/steps_2025-02-01.csv'
    
    # CSV取得
    with open(INPUT_FILE) as f:
        # ファイル名から最初の行の時刻を生成
        first_timestamp = get_first_timestamp(INPUT_FILE)

        # 歩数ファイルは1分毎に行が作成されるが、歩数0の行は作成されない。
        # そのため、前の行との差が1分より大きい場合は、歩数0の行を補完する。
        
        # ヘッダー除外
        reader = csv.reader(f)
        header = next(reader)

        last_timestamp = first_timestamp
        
        for row in reader:
            print(row)

            # 補完対象判定
            while need_complement(last_timestamp, row[0]):
                print('補完対象')
                
                next_time = next_timestamp(last_timestamp)
                # 補完処理
                complement_row = [next_time, 0]
                print(complement_row)

                last_timestamp = next_time

            last_timestamp = row[0]
            break


if __name__ == '__main__':
    main()
