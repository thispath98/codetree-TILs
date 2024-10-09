L, N, Q = map(int, input().split())

# 0: 빈칸, 1: 함정, 2: 벽, 3~: 기사
chess = [[[] for _ in range(L)] for _ in range(L)]
for i in range(L):
    inputs = list(map(int, input().split()))
    for j in range(L):
        chess[i][j].append(inputs[j])

# (r, c, h, w, k, barrier_range)
knights = []
for i in range(N):
    r, c, h, w, k = map(int, input().split())
    r -= 1
    c -= 1
    barrier_range = []
    for b_r in range(r, r + h):
        for b_c in range(c, c + w):
            barrier_range.append([b_r, b_c])
            chess[b_r][b_c].append(i + 3)
    knights.append([r, c, h, w, k, barrier_range])

# (i, d): i번째 기사를 d로 한칸 이동
orders = []
for _ in range(Q):
    i, d = map(int, input().split())
    orders.append([i - 1, d])

move = [[-1, 0], [0, 1], [1, 0], [0, -1]]
origin_hp = [knight[-2] for knight in knights]
after_hp = [knight[-2] for knight in knights]
alive = [True for _ in range(N)]

def check(k_i, d, arr):
    # arr에 이동해야 할 기사의 인덱스 추가
    if k_i not in arr:
        arr.append(k_i)

    barrier_range = knights[k_i][-1]
    for b_r, b_c in barrier_range:
        n_b_r = b_r + d[0]
        n_b_c = b_c + d[1]
        if not (0 <= n_b_r < L and 0 <= n_b_c < L) or chess[n_b_r][n_b_c][-1] == 2:
            # 벽이 있음
            return False
        else:
            # 재귀적으로 이동한 위치에 밀 수 있는지 찾는다
            if chess[n_b_r][n_b_c][-1] not in [0, 1, k_i + 3]:
                if check(chess[n_b_r][n_b_c][-1] - 3, d, arr):
                    # 다른 기사가 있음
                    pass
                else:
                    # 밀 수 없는 경우
                    return False
    return arr

for i, d in orders:
    # 죽었을 경우 건너 뜀
    if not alive[i]:
        continue
    d = move[d]

    # 부딪히는지 구하기
    pushed_knights = check(i, d, [])

    # 밀 수 있는 경우, 밀기
    if pushed_knights:
        # 현재 barrier_range의 위치 찾기
        max_r = [-1 for _ in range(N)]
        min_r = [float("inf") for _ in range(N)]
        max_c = [-1 for _ in range(N)]
        min_c = [float("inf") for _ in range(N)]
        for k_i in pushed_knights:
            for b_r, b_c in knights[k_i][-1]:
                if max_r[k_i] < b_r:
                    max_r[k_i] = b_r
                if min_r[k_i] > b_r:
                    min_r[k_i] = b_r
                if max_c[k_i] < b_c:
                    max_c[k_i] = b_c
                if min_c[k_i] > b_c:
                    min_c[k_i] = b_c

        # 인덱스 붙여서, 조건에 맞는 순서대로 정렬
        max_r = [(max_r[i], i) for i in range(N)]
        min_r = [(min_r[i], i) for i in range(N)]
        max_c = [(max_c[i], i) for i in range(N)]
        min_c = [(min_c[i], i) for i in range(N)]
        if d == [-1, 0]:
            # 상일 경우 min_r이 가장 낮은 순서대로
            pushed_knights = sorted(min_r, key=lambda x: x[0])
        elif d == [0, 1]:
            # 우일 경우 max_c이 가장 높은 순서대로
            pushed_knights = sorted(max_c, key=lambda x: -x[0])
        elif d == [1, 0]:
            # 하일 경우 max_r이 가장 높은 순서대로
            pushed_knights = sorted(max_r, key=lambda x: -x[0])
        else:
            # 좌일 경우 min_c이 가장 낮은 순서대로
            pushed_knights = sorted(min_c, key=lambda x: x[0])

        for _, k_i in pushed_knights:
            traps = 0
            for b_i, (b_r, b_c) in enumerate(knights[k_i][-1]):
                n_b_r = b_r + d[0]
                n_b_c = b_c + d[1]

                # 트랩 개수 구하기
                if chess[n_b_r][n_b_c][0] == 1:
                    traps += 1

                chess[b_r][b_c].pop() # 현위치 0으로
                chess[n_b_r][n_b_c].append(k_i + 3)  # 밀린 곳으로 이동
                # barrier_range 변경
                knights[k_i][-1][b_i] = [n_b_r, n_b_c]

            # 다른 기사들은 피해를 입음
            if k_i != i:
                after_hp[k_i] -= traps

                # 기사가 죽었을 경우, 맵에서 해제함
                if after_hp[k_i] <= 0:
                    for b_r, b_c in knights[k_i][-1]:
                        chess[b_r][b_c].pop()

answer = [o_hp - a_hp for o_hp, a_hp in zip(origin_hp, after_hp) if a_hp > 0]
print(sum(answer))