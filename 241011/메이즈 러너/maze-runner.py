N, M, K = map(int, input().split())

# 0: 빈칸, 1~9: 벽(내구도)
board = [[-1] * N] + [[-1] + list(map(int, input().split())) + [-1] for _ in range(N)] + [[-1] * N]
player = [list(map(int, input().split())) for _ in range(M)]
exit_coord = list(map(int, input().split()))

move = [[-1, 0], [1, 0], [0, -1], [0, 1]]

def get_dist(r1, c1, r2, c2):
    # 출구와의 거리 찾기
    return abs(r1 - r2) + abs(c1 - c2)

def move_fn():
    movement = 0
    for i in range(M):
        r, c = player[i]
        cur_dist = get_dist(r, c, *exit_coord)
        for dr, dc in move: # 상 하 좌 우 순
            nr, nc = r + dr, c + dc
            if 1 <= nr <= N and 1 <= nc <= N and board[nr][nc] == 0:
                dist = get_dist(nr, nc, *exit_coord)
                if dist < cur_dist:
                    cur_dist = dist
                    player[i] = [nr, nc]

        # 첫 위치랑 현재 위치랑 다르다면 거리 + 1
        if [r, c] != player[i]:
            movement += 1
            if player[i] == exit_coord:
                player[i] = [0, 0]

    return movement

def get_square():
    for d in range(2, N + 1):
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                e_check = True if i <= exit_coord[0] < i + d and j <= exit_coord[1] < j + d else False
                p_check = [True if i <= r < i + d and j <= c < j + d else False for r, c in player]
                # print(e_check, p_check)
                if e_check and any(p_check):
                    si, sj, rot_n = i, j, d
                    return si, sj, rot_n
                    

def rotate(si, sj, n):
    # 회전해야 하는 사람 선택
    rot_p = []
    for i in range(M):
        r, c = player[i]
        if si <= r < si + n and sj <= c < sj + n:
            rot_p.append(i)

    # 회전
    t_board = [row[:] for row in board]
    for i in range(n):
        for j in range(n):
            ni = si + n - j - 1
            nj = sj + i
            board[si + i][sj + j] = max(t_board[ni][nj] - 1, 0)

    # 사람 회전
    for i in rot_p:
        r, c = player[i]
        ro, co = r - si, c - sj
        player[i] = [si + co, sj + n - 1 - ro]

    # 출구 회전
    ci, cj = exit_coord
    cio, cjo = ci - si, cj - sj
    return [si + cjo, sj + n - 1 - cio]

movements = 0
for k in range(1, K + 1):
    if all([[0, 0] == p for p in player]):
        break

    # 움직일 수 있는 위치 찾고, 이동한 거리 더해주기
    movement = move_fn()
    movements += movement

    if all([[0, 0] == p for p in player]):
        break

    si, sj, rot_n = get_square()

    exit_coord = rotate(si, sj, rot_n)

print(movements)
print(*exit_coord)