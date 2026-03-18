import pymysql
import getpass


# DB接続
def get_connection():
    print("\n--- DB接続情報入力 ---")
    user = input("ユーザー名 (例: root): ").strip()
    password = getpass.getpass("パスワード: ")
    db = input("DB名 (例: pyapp): ").strip()

    try:
        connection = pymysql.connect(
            host="localhost",
            user=user,
            password=password,
            db=db,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
        )
        print("DB接続成功\n")
        return connection

    except Exception as e:
        print("DB接続に失敗しました")
        print(e)
        return None


# タスク一覧
def list_task(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT taskname, content, manager, deadline, status FROM task")
        tasks = cursor.fetchall()

    if not tasks:
        print("タスクはありません")
        return

    print("\n--- タスク一覧 ---")
    for i, task in enumerate(tasks, start=1):
        print(
            f"{i}. {task['taskname']} | "
            f"{task['content']} | "
            f"{task['manager']} | "
            f"{task['deadline']} | "
            f"{task['status']}"
        )


# タスク登録
def create_task(connection):
    print("\n--- タスク登録 ---")

    taskname = input("タスク名: ").strip()
    content = input("内容: ").strip()
    manager = input("担当者: ").strip()
    deadline = input("期限 (YYYY-MM-DD): ").strip()
    status = input("状態: ").strip()

    if not taskname:
        print("タスク名は必須です")
        return

    sql = """
        INSERT INTO task (taskname, content, manager, deadline, status)
        VALUES (%s, %s, %s, %s, %s)
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, (taskname, content, manager, deadline, status))

    connection.commit()
    print("タスクを登録しました")


# メイン処理
def main():
    connection = get_connection()
    if not connection:
        return

    try:
        print("-- タスク管理アプリ --")
        print("1: タスク登録")
        print("2: タスク一覧")
        print("3: 終了")

        operation = input("> ").strip()

        if operation == "1":
            create_task(connection)
        elif operation == "2":
            list_task(connection)
        elif operation == "3":
            print("終了します")
        else:
            print("1〜3を入力してください")

    finally:
        connection.close()


if __name__ == "__main__":
    main()