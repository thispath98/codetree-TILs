N, M, P, C, D = map(int, input().split())
r, c = map(int, input().split())
r, c = r - 1, c - 1
santas = [list(map(int, input().split())) for _ in range(P)]
santas.sort(key=lambda x: x[0])
santas = [[s_n, s_r - 1, s_c - 1] for s_n, s_r, s_c in santas]

r_move = [
    [-1, -1], [-1, 0], [-1, 1],
    [0, -1], [0, 0], [0, 1],
    [1, -1], [1, 0], [1, 1],
]
s_move = [[-1, 0], [0, 1], [1, 0], [0, -1]]

def get_dist(r_1, c_1, r_2, c_2):
    return (r_1 - r_2) ** 2 + (c_1 - c_2) ** 2

scores = [0 for _ in range(P)]
alive = [True for _ in range(P)]
stun = [0 for _ in range(P)]
for m in range(M):
    # 살아 있는 산타 없으면 종료
    if not any(alive):
        break

    # 0: 빈칸, -1: 루돌프, 1~P: 산타
    # dist_list에 (산타 번호, 거리, r, c) 저장
    board = [[0 for _ in range(N)] for _ in range(N)]
    board[r][c] = -1
    dist_list = []
    for i in range(P):
        s_n, s_r, s_c = santas[i]
        # 살아 있으면 이동, 아니면 거리 무한대로
        if alive[i]:
            board[s_r][s_c] = s_n
            dist = get_dist(r, c, s_r, s_c)
        else:
            dist = float("inf")
        dist_list.append([s_n, dist, s_r, s_c])

    # 가장 가까운 산타 선택
    sorted_dist = sorted(dist_list, key=lambda x: (x[1], -x[2], -x[3]))
    s_n, s_dist, s_r, s_c = sorted_dist[0]
    r_coord = []
    move = []
    for dr, dc in r_move:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < N and 0 <= nc < N:
            dist = get_dist(nr, nc, s_r, s_c)
            if dist < s_dist:
                s_dist = dist
                r_coord = [nr, nc]
                move = [dr, dc]

    # 충돌 시 밀려남
    if r_coord == [s_r, s_c]:
        s_r += move[0] * C
        s_c += move[1] * C
        scores[s_n - 1] += C
        stun[s_n - 1] = 2

        while True:
            # 탈락 처리
            if 0 <= s_r < N and 0 <= s_c < N:
                santas[s_n - 1][1] = s_r
                santas[s_n - 1][2] = s_c

                # 상호작용
                t_n = board[s_r][s_c]
                board[s_r][s_c] = s_n
                if t_n == 0:
                    # 밀려난 위치가 빈칸이면 그대로 끝
                    break
                else:
                    # 밀려난 위치에 산타가 있으면 다시 상호작용
                    s_n = t_n
                    s_r = santas[s_n - 1][1] + move[0]
                    s_c = santas[s_n - 1][2] + move[1]
            else:
                alive[s_n - 1] = False
                break

    # 루돌프 이동
    board[r][c] = 0
    r, c = r_coord
    board[r][c] = -1

    # 산타 처리
    for i in range(P):
        # 탈락 시 안움직임
        if not alive[i]:
            continue

        # 기절 시 안움직임
        if stun[i] > 0:
            stun[i] -= 1
            continue

        # 움직일 수 있는 경우
        s_n, s_r, s_c = santas[i]
        s_dist = get_dist(r, c, s_r, s_c)
        s_coord = []
        move = []
        for dr, dc in s_move:
            nr = s_r + dr
            nc = s_c + dc
            if 0 <= nr < N and 0 <= nc < N and board[nr][nc] in [0, -1]:
                dist = get_dist(r, c, nr, nc)
                if dist < s_dist:
                    s_dist = dist
                    s_coord = [nr, nc]
                    move = [dr, dc]

        # 이동할 수 없을 경우 제자리
        if not move:
            continue

        # 충돌, 탈락 처리
        if s_coord == [r, c]:
            # 이동한 위치에 루돌프가 있다면
            board[s_r][s_c] = 0
            s_r = s_coord[0] - move[0] * D
            s_c = s_coord[1] - move[1] * D
            scores[i] += D
            stun[i] = 1

            while True:
                # 탈락 처리
                if 0 <= s_r < N and 0 <= s_c < N:
                    santas[s_n - 1][1] = s_r
                    santas[s_n - 1][2] = s_c

                    # 상호작용
                    t_n = board[s_r][s_c]
                    board[s_r][s_c] = s_n
                    if t_n == 0:
                        # 밀려난 위치가 빈칸이면 그대로 끝
                        break
                    else:
                        # 밀려난 위치에 산타가 있으면 다시 상호작용
                        s_n = t_n
                        s_r = santas[s_n - 1][1] - move[0]
                        s_c = santas[s_n - 1][2] - move[1]
                else:
                    alive[s_n - 1] = False
                    break
        else:
            # 이동한 위치에 루돌프가 없으면 그대로 이동
            santas[s_n - 1][1] = s_coord[0]
            santas[s_n - 1][2] = s_coord[1]
            board[s_r][s_c] = 0
            board[s_coord[0]][s_coord[1]] = s_n

    # 살아남았을 경우 +1점
    for i in range(P):
        if alive[i]:
            scores[i] += 1

print(*scores)