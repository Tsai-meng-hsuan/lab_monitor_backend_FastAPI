def topological_sort(nodes, edges):
    # 建立節點入度與鄰接圖
    in_degree = {}
    graph = {}

    # 初始化，在in_degree、graph字典中加入所有節點
    for node in nodes:
        node_id = node["id"]
        in_degree[node_id] = 0
        graph[node_id] = [] # graph為list，儲存每個node的下一個節點ID

    # 填入邊的資訊，注意這邊的source、target其實就是node的id
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        graph[source].append(target)    # 以<邊>為單位，建立每一個node的對應關係list(graph[source]),EX: graph[0] = [1,2,5]
        in_degree[target] += 1  # 計算入度累加，EX: in_degree[1] = 1, in_degree[2] = 1, in_degree[5] = 1

    # 找出入度為 0 的節點
    queue = [node_id for node_id in in_degree if in_degree[node_id] == 0]
    sorted_nodes = []

    # 拓撲排序主迴圈，持續執行直到queue中沒有資料
    while queue:
        node = queue.pop(0)  # 取出第一個元素（index 0），並從列表中移除它，模擬 queue（效率不如 deque，但可用）
        sorted_nodes.append(node) # 將當前節點加入排序結果

        for neighbor in graph[node]:    # EX: graph[0] = [1,2,5]
            in_degree[neighbor] -= 1    # 對下一個節點的degree進行遞減
            if in_degree[neighbor] == 0:    # 若下一個節點的degree為0，則由後方加入queue list中，保證先入先出的順序
                queue.append(neighbor)

    # 檢查是否有循環（即無法排序完整，最終只輸出一個序列的list，且必須包含所有的node
    if len(sorted_nodes) != len(nodes):
        raise ValueError("圖中有循環，無法進行拓撲排序")

    return sorted_nodes
