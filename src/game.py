import math
import random
import sys
from enum import IntEnum

import pygame


class MAZE(IntEnum):
    # 床
    FLOOR = 0
    # 壁
    WALL = 1
    # 柱
    PILLAR = 2


class DUNGEN(IntEnum):
    # 床
    FLOOR = 0
    # 宝箱
    TREASURE = 1
    # 繭
    COCOON = 2
    # 階段
    STAIRS = 3
    # 壁
    WALL = 9
    # 壁と壁が繋がっている場合
    WALL2 = 10


class PLAYER_INFO(IntEnum):
    # X座標
    X = 0
    # Y座標
    Y = 1
    # 画像
    IMG = 2


class PLAYER_IMAGE(IntEnum):
    # 後ろ姿の左足前方
    BACK1 = 0
    # 後ろ姿の右足前方
    BACK2 = 1
    # 正面姿の左足前方
    FRONT1 = 2
    # 正面姿の右足前方
    FRONT2 = 3
    # 左向き姿の左足前方
    LEFT_FACING1 = 4
    # 左向き姿の左足前方
    LEFT_FACING2 = 5
    # 右向き姿の左足前方
    RIGHT_FACING1 = 6
    # 右向き姿の左足前方
    RIGHT_FACING2 = 7


# グローバル変数
MAZE_WIDTH = 11
MAZE_HEIGHT = 9
DUNGEN_SCALE = 3
FILED_CELL_WIDTH = 80
FILED_CELL_HEIGHT = 80
SCREEN_WIDTH = 880
SCREEN_HEIGHT = 720
# 色の設定
Color = {
    # 背景 (黒)
    "BACK_GROUND": (0, 0, 0),
    "CYAN": (0, 255, 255),
    "GRAY": (96, 96, 96),
}
# ダンジョン画像
imgDungen = {
    # 床
    DUNGEN.FLOOR: pygame.image.load("image/floor.png"),
    # 壁
    DUNGEN.WALL: pygame.image.load("image/wall.png"),
    # 壁と壁が繋がっている場合
    DUNGEN.WALL2: pygame.image.load("image/wall2.png"),
    # 宝箱
    DUNGEN.TREASURE: pygame.image.load("image/tbox.png"),
    # 繭
    DUNGEN.STAIRS: pygame.image.load("image/cocoon.png"),
    # 階段
    DUNGEN.STAIRS: pygame.image.load("image/stairs.png"),
}
# プレイヤー画像
imgPlayer = {
    # 後ろ姿の左足前方
    PLAYER_IMAGE.BACK1: pygame.image.load("image/mychr0.png"),
    # 後ろ姿の右足前方
    PLAYER_IMAGE.BACK2: pygame.image.load("image/mychr1.png"),
    # 正面姿の左足前方
    PLAYER_IMAGE.FRONT1: pygame.image.load("image/mychr2.png"),
    # 正面姿の右足前方
    PLAYER_IMAGE.FRONT2: pygame.image.load("image/mychr3.png"),
    # 左向き姿の左足前方
    PLAYER_IMAGE.LEFT_FACING1: pygame.image.load("image/mychr4.png"),
    # 左向き姿の左足前方
    PLAYER_IMAGE.LEFT_FACING2: pygame.image.load("image/mychr5.png"),
    # 右向き姿の左足前方
    PLAYER_IMAGE.RIGHT_FACING1: pygame.image.load("image/mychr6.png"),
    # 右向き姿の左足前方
    PLAYER_IMAGE.RIGHT_FACING2: pygame.image.load("image/mychr7.png"),
}


# メイン処理
def main():
    # pygameの初期化
    pygame.init()
    # 画面サイズの設定
    size = get_screen_size()
    width, height = size
    screen = pygame.display.set_mode((width, height))
    # 時間クラスの取得
    clock = pygame.time.Clock()
    # プレイヤーの設定
    player = [0, 0, PLAYER_IMAGE.FRONT1]
    # 迷路の作成
    maze = make_maze()
    # ダンジョンの作成
    dungen = make_dungen(maze)
    # プレイヤーの初期化処理
    init_player(dungen, player)
    # ゲームループ処理
    while True:
        # イベントの取得
        for event in pygame.event.get():
            # 終了イベント
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # キー情報
        key = pygame.key.get_pressed()
        # プレイヤーの位置更新
        move_player(key, dungen, player)
        # ダンジョンの描画
        draw_dungen(screen, dungen, player)
        # プレイヤーの描画
        draw_player(screen, player)
        # 画面の更新
        pygame.display.update()
        # フレームレート指定　(1秒間に何回処理させるか)
        clock.tick(10)


# 画面サイズを取得
def get_screen_size():
    width = SCREEN_WIDTH
    height = SCREEN_HEIGHT
    return width, height


# ダンジョンサイズを取得
def get_dungen_size():
    maze_size = get_maze_size()
    maze_width, maze_height = maze_size
    scale = get_dungen_scale()
    width = maze_width * scale
    height = maze_height * scale
    return width, height


# 迷路サイズを取得
def get_maze_size():
    width = MAZE_WIDTH
    height = MAZE_HEIGHT
    return width, height


# フィールドのセルサイズを取得
def get_filed_cell_size():
    width = FILED_CELL_WIDTH
    height = FILED_CELL_HEIGHT
    return width, height


# スケールサイズを取得
def get_dungen_scale():
    scale = DUNGEN_SCALE
    if scale < 1:
        return 1
    else:
        return scale


# 描画エリアを取得
def get_draw_area():
    # 画面サイズを取得
    screen_size = get_screen_size()
    screen_width, screen_height = screen_size
    # フィールドサイズを取得
    filed_cell_size = get_filed_cell_size()
    filed_cell_width, filed_cell_height = filed_cell_size
    # 画面サイズ内のセル数を取得
    filed_cell_width_num = screen_width / filed_cell_width
    filed_cell_height_num = screen_height / filed_cell_height
    # 描画エリアを取得
    x_end = int(math.ceil(filed_cell_width_num / 2))
    x_start = int(x_end - filed_cell_width_num)
    y_end = int(math.ceil(filed_cell_height_num / 2))
    y_start = int(y_end - filed_cell_height_num)
    return x_start, x_end, y_start, y_end


# ダンジョンの描画
def draw_dungen(screen, dungen, player):
    # 背景の初期化
    screen.fill(Color["BACK_GROUND"])
    # 迷路のサイズを取得
    size = get_dungen_size()
    width, height = size
    # プレイヤーの中心位置から描画を行う
    area = get_draw_area()
    for y in range(area[2], area[3]):
        for x in range(area[0], area[1]):
            # ダンジョンの表示位置
            dungen_x = player[PLAYER_INFO.X] + x
            dungen_y = player[PLAYER_INFO.Y] + y
            # ダンジョン範囲内の場合
            if (
                dungen_x >= 0
                and dungen_x < width
                and dungen_y >= 0
                and dungen_y < height
            ):
                # ダンジョンの描画
                # フィールドのサイズを取得
                filed_cell_size = get_filed_cell_size()
                filed_cell_width, filed_cell_height = filed_cell_size
                # 画像の表示位置とデータを取得
                image = imgDungen[dungen[dungen_y][dungen_x]]
                img_x = (x - area[0]) * filed_cell_width
                img_y = (y - area[2]) * filed_cell_height
                # 壁の場合
                if dungen[dungen_y][dungen_x] == DUNGEN.WALL:
                    screen.blit(image, [img_x, img_y - 40])
                    # 壁と壁が繋がっている場合
                    if dungen_y >= 1 and dungen[dungen_y - 1][dungen_x] == DUNGEN.WALL:
                        screen.blit(imgDungen[DUNGEN.WALL2], [img_x, img_y - 80])
                else:
                    screen.blit(image, [img_x, img_y])


def draw_player(screen, player):
    # プレイヤーの画像
    img = imgPlayer[player[PLAYER_INFO.IMG]]
    # 描画エリアを取得
    area = get_draw_area()
    # フィールドのサイズを取得
    filed_size = get_filed_cell_size()
    filed_width, filed_height = filed_size
    # 画像の表示位置とデータを取得(プレイヤーは中心位置のため、開始位置の距離が描画位置)
    img_x = abs(area[0]) * filed_width
    img_y = abs(area[2]) * filed_height
    # プレイヤー描画
    screen.blit(img, [img_x, img_y - 80])


def move_player(key, dungen, player):
    # プレイヤーの表示位置
    x = player[PLAYER_INFO.X]
    y = player[PLAYER_INFO.Y]
    img = player[PLAYER_INFO.IMG]
    # 移動の更新処理
    if key[pygame.K_UP] == 1:  # 上方向
        # 位置の取得
        y = y - 1
        # 画像の取得
        if img == PLAYER_IMAGE.BACK1:
            img = PLAYER_IMAGE.BACK2
        else:
            img = PLAYER_IMAGE.BACK1
    elif key[pygame.K_DOWN] == 1:  # 下方向
        # 位置の取得
        y = y + 1
        # 画像の取得
        if img == PLAYER_IMAGE.FRONT1:
            img = PLAYER_IMAGE.FRONT2
        else:
            img = PLAYER_IMAGE.FRONT1
    elif key[pygame.K_LEFT] == 1:  # 左方向
        # 位置の取得
        x = x - 1
        # 画像の取得
        if img == PLAYER_IMAGE.LEFT_FACING1:
            img = PLAYER_IMAGE.LEFT_FACING2
        else:
            img = PLAYER_IMAGE.LEFT_FACING1
    elif key[pygame.K_RIGHT] == 1:  # 右方向
        # 位置の取得
        x = x + 1
        # 画像の取得
        if img == PLAYER_IMAGE.RIGHT_FACING1:
            img = PLAYER_IMAGE.RIGHT_FACING2
        else:
            img = PLAYER_IMAGE.RIGHT_FACING1
    # 移動の更新処理
    if dungen[y][x] != DUNGEN.WALL:
        player[PLAYER_INFO.X] = x
        player[PLAYER_INFO.Y] = y
        player[PLAYER_INFO.IMG] = img


# 迷路を作成(棒倒し)
def make_maze():
    # 迷路の初期化
    maze = []
    size = get_maze_size()
    width, height = size
    for i in range(height):
        maze.append([MAZE.FLOOR] * width)
    # 壁で囲む
    for x in range(width):
        maze[0][x] = MAZE.WALL
        maze[height - 1][x] = MAZE.WALL
    for y in range(1, height - 1):
        maze[y][0] = MAZE.WALL
        maze[y][width - 1] = MAZE.WALL
    # 棒倒し法
    # 棒を倒す座標(下、右、上、左)
    x_pole = [0, 1, 0, -1]
    y_pole = [-1, 0, 1, 0]
    for y in range(2, height - 2, 2):
        for x in range(2, width - 2, 2):
            # １マス置きに柱を立てる
            maze[y][x] = MAZE.PILLAR
            if x < 2:  # 2列目からは左に壁を作らない
                pole_coor = random.randint(0, 3)
            else:
                pole_coor = random.randint(0, 2)
            # ランダムで上下左右に柱を追加
            maze[y + y_pole[pole_coor]][x + x_pole[pole_coor]] = MAZE.PILLAR
    return maze


# ダンジョンを作成
def make_dungen(maze):
    # ダンジョンの初期化
    # 迷路のサイズを取得
    maze_size = get_maze_size()
    maze_width, maze_height = maze_size
    # ダンジョンのスケールを取得
    scale = get_dungen_scale()
    # ダンジョンのサイズを取得
    dungen_size = get_dungen_size()
    dungen_width, dungen_height = dungen_size
    # ダンジョンの作成 (壁のみ)
    dungen = []
    for i in range(dungen_height):
        dungen.append([DUNGEN.WALL] * dungen_width)
    # ダンジョンの作成
    for y in range(maze_height):
        for x in range(maze_width):
            # スケールアップした座標系の中心座標を求める
            medium = int(scale / 2 + 1)
            # スケールアップした座標の迷路の位置を求める
            scale_x = x * scale + medium - 1
            scale_y = y * scale + medium - 1
            # スケールアップの幅を求める
            room_start = 0 - medium + 1
            room_end = medium
            # 床の場合に通路と部屋に分ける
            if maze[y][x] == MAZE.FLOOR:
                if random.randint(0, 99) > 20:  # 20%の確率で部屋を作成
                    for room_y in range(room_start, room_end):
                        for room_x in range(room_start, room_end):
                            # スケール幅分の部屋を作る
                            dungen[scale_y + room_y][scale_x + room_x] = DUNGEN.FLOOR
                else:  # 80%の確率で通路を作成
                    # 通路をスケールアップした迷路位置を設定
                    dungen[scale_y][scale_x] = DUNGEN.FLOOR
                    # 通路をスケール幅分拡大させる
                    for i in range(1, room_end):
                        if maze[y - 1][x] == MAZE.FLOOR:  # 上方向
                            dungen[scale_y - i][scale_x] = DUNGEN.FLOOR
                        if maze[y + 1][x] == MAZE.FLOOR:  # 下方向
                            dungen[scale_y + i][scale_x] = DUNGEN.FLOOR
                        if maze[y][x - 1] == MAZE.FLOOR:  # 左方向
                            dungen[scale_y][scale_x - i] = DUNGEN.FLOOR
                        if maze[y][x + 1] == MAZE.FLOOR:  # 右方向
                            dungen[scale_y][scale_x + i] = DUNGEN.FLOOR
    return dungen


# プレイヤーの初期化処理
def init_player(dungen, player):
    # ダンジョンのサイズを取得
    dungen_size = get_dungen_size()
    dungen_width, dungen_height = dungen_size
    while True:
        # ダンジョンの位置をランダムで取得 (囲いの壁を除く)
        x = random.randint(3, dungen_width - 4)
        y = random.randint(3, dungen_height - 4)
        # 壁でない場合はプレイヤーの位置に決定
        if dungen[y][x] != DUNGEN.WALL:
            player[PLAYER_INFO.X] = x
            player[PLAYER_INFO.Y] = y
            break


# 実行
if __name__ == "__main__":
    main()
