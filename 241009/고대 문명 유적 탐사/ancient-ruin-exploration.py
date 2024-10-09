K, M = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(5)]
item = list(map(int, input().split()))
item_idx = 0

def rotate(board, i, j, N):
    t_board = [row[:] for row in board]
    start_row, start_col = i - (N // 2), j - (N // 2)

    for r in range(N):
        for c in range(N):
            t_board[start_row + c][start_col + N - 1 - r] = board[start_row + r][start_col + c]

    return t_board

def bfs(board):
    visited = [[False for _ in range(5)] for _ in range(5)]
    move = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    total = 0
    total_coords = []
    for y in range(5):
        for x in range(5):
            q = [[y, x]]
            selected = board[y][x]
            visited[y][x] = True
            cnt = 1
            coords = [[y, x]]

            while q:
                r, c = q.pop()
                for dr, dc in move:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 5 and 0 <= nc < 5 and not visited[nr][nc] and selected == board[nr][nc]:
                        q.append([nr, nc])
                        visited[nr][nc] = True
                        cnt += 1
                        coords.append([nr, nc])

            if cnt >= 3:
                total += cnt
                total_coords.extend(coords)
    return total, total_coords

answer = []
for _ in range(K):
    ans = 0

    # 회전수, 열, 행, 보드
    cand = []
    # 3x3 회전
    for i in range(1, 4):
        for j in range(1, 4):
            t_board = rotate(board, i, j, 3)
            cand.append([1, i, j, t_board])
            t_board = rotate(t_board, i, j, 3)
            cand.append([2, i, j, t_board])
            t_board = rotate(t_board, i, j, 3)
            cand.append([3, i, j, t_board])

    # 5x5 회전
    t_board = rotate(board, 2, 2, 5)
    cand.append([1, 2, 2, t_board])
    t_board = rotate(t_board, 2, 2, 5)
    cand.append([2, 2, 2, t_board])
    t_board = rotate(t_board, 2, 2, 5)
    cand.append([3, 2, 2, t_board])

    # 1차 획득, 변경된 좌표
    count_list = []
    for i, candidate in enumerate(cand):
        count_list.append(bfs(candidate[-1]))

    # 최댓값 구함
    conditions = [[count[0], candidate[0], candidate[2], candidate[3], count[1]] for candidate, count in zip(cand, count_list)]
    count, _, _, board, coords = sorted(conditions, key=lambda x: (-x[0], x[1], x[2]))[0]

    if count == 0:
        # 유물 얻지 못했을 경우 끝
        break
    else:
        # 유물 채워넣기
        sorted_coords = sorted(coords, key=lambda x: (x[1], -x[0]))
        for y, x in sorted_coords:
            board[y][x] = item[item_idx]
            item_idx += 1
        ans += count

    # 연쇄획득
    while True:
        count, coords = bfs(board)
        if count == 0:
            break

        # 유물 채워넣기
        sorted_coords = sorted(coords, key=lambda x: (x[1], -x[0]))
        for y, x in sorted_coords:
            board[y][x] = item[item_idx]
            item_idx += 1
        ans += count
    answer.append(ans)

print(*answer)