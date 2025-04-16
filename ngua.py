import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Các bước di chuyển của con mã
MOVES = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]


# Hàm kiểm tra vị trí hợp lệ
def is_valid(x, y, n, board):
    return 0 <= x < n and 0 <= y < n and board[x][y] == -1


# Hàm đếm số nước đi khả thi (Warnsdorff's Heuristic)
def get_degree(x, y, n, board):
    count = 0
    for dx, dy in MOVES:
        next_x, next_y = x + dx, y + dy
        if is_valid(next_x, next_y, n, board):
            count += 1
    return count


# Hàm giải bài toán mã đi tuần
def knight_tour(n, start_x, start_y):
    board = [[-1 for _ in range(n)] for _ in range(n)]
                                                            # Khởi tạo bàn cờ với tất cả ô = -1
    board[start_x][start_y] = 0                             # Đánh dấu ô bắt đầu là bước 0
    stack = [(start_x, start_y)]                            # Stack lưu vị trí hiện tại
    step = 1                                                # Số thứ tự bước hiện tại
    path = [(start_x, start_y)]                             # Đường đi (lưu toàn bộ các ô đã đi qua)

    while stack and step < n * n:                           # Lặp cho đến khi stack rỗng hoặc đã đi qua tất cả ô
        x, y = stack[-1]                                    # Lấy vị trí hiện tại trên đỉnh stack
        next_moves = []                                     # Danh sách các bước đi tiếp theo khả thi
        # Tìm tất cả các bước đi hợp lệ từ vị trí hiện tại
        for dx, dy in MOVES:
            next_x, next_y = x + dx, y + dy
            if is_valid(next_x, next_y, n, board):
                degree = get_degree(next_x, next_y, n, board)  # Tính số nước đi tiếp theo từ vị trí mới
                next_moves.append((next_x, next_y, degree))  # Lưu vị trí và số nước đi

        if not next_moves:                                  # Nếu không có bước đi tiếp theo hợp lệ
            stack.pop()                                     # Quay lại bước trước (backtracking)
            if path:                                        # Xóa bước đi cuối cùng khỏi path
                last_x, last_y = path.pop()
                board[last_x][last_y] = -1                  # Đánh dấu lại ô này chưa đi qua
                step -= 1                                   # Giảm số bước
        else:
            # Sắp xếp các bước đi theo số lượng nước đi tiếp theo (Warnsdorff's Heuristic)
            next_moves.sort(key=lambda move: move[2])
            next_x, next_y, _ = next_moves[0]               # Chọn ô có ít nước đi tiếp theo nhất
            board[next_x][next_y] = step                    # Đánh dấu ô với số thứ tự bước
            stack.append((next_x, next_y))                  # Thêm vị trí mới vào stack
            path.append((next_x, next_y))                   # Thêm vị trí mới vào path
            step += 1                                       # Tăng số bước

    # Kiểm tra nếu đã đi qua tất cả các ô
    if step == n * n:
        return board, path
    return None, None                                       # Không tìm thấy đường đi


# Hàm vẽ bàn cờ với bước hiện tại
def draw_board(board, path, step_index, start_x, start_y):
    n = len(board)
    chess_board = np.zeros((n, n))
    chess_board[::2, 1::2] = 1
    chess_board[1::2, ::2] = 1

    fig, ax = plt.subplots(figsize=(10, 10))  # Tăng kích thước
    ax.imshow(chess_board, cmap='Pastel1', alpha=0.8)

    # Tô màu ô đã đi qua
    for i in range(min(step_index + 1, len(path))):
        x, y = path[i]
        ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, fill=True, color='lightgreen', alpha=0.3))

    # Vẽ số bước
    for i in range(n):
        for j in range(n):
            if board[i][j] != -1 and board[i][j] <= step_index:
                color = 'black' if chess_board[i, j] == 0 else 'darkblue'
                if i == start_x and j == start_y:
                    ax.text(j, i, f"{board[i][j]}", ha='center', va='center', fontsize=18, color='red',
                            fontweight='bold')
                else:
                    ax.text(j, i, f"{board[i][j]}", ha='center', va='center', fontsize=16, color=color)

    # Vẽ đường đi đến bước hiện tại
    for i in range(min(step_index, len(path) - 1)):
        x1, y1 = path[i][1], path[i][0]
        x2, y2 = path[i + 1][1], path[i + 1][0]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="green", lw=1))

    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title(f"Bước {step_index} / {n * n - 1}", fontsize=18, pad=15)
    return fig


# Giao diện Streamlit
def main():
    st.set_page_config(page_title="Bài toán mã đi tuần")
    st.markdown(
        """
        <style>
        .title {color: #FFFFFF; font-size: 36px; font-weight: bold; text-align: center;}
        .subtitle {color: #FFFFFF; font-size: 20px; text-align: center; margin-bottom: 20px;}
        .path-box {background-color: #E8F0FE; padding: 15px; border-radius: 8px; color: #000000; font-size: 16px;}
        .info-box {background-color: #F9E79F; padding: 10px; border-radius: 5px; color: #333333; font-size: 14px;}
        .stButton>button {background-color: #4CAF50; color: white; font-size: 16px;}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="title">Hành trình của con mã</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Theo dõi từng bước di chuyển của con mã trên bàn cờ!</div>',
                unsafe_allow_html=True)

    # Nhập liệu
    col1, col2, col3 = st.columns(3)
    with col1:
        n = st.number_input("Kích thước bàn cờ (n x n):", min_value=5, max_value=8, value=5, step=1)
    with col2:
        start_x = st.number_input("Tọa độ x bắt đầu:", min_value=0, max_value=n - 1, value=0)
    with col3:
        start_y = st.number_input("Tọa độ y bắt đầu:", min_value=0, max_value=n - 1, value=0)

    # Trạng thái
    if 'board' not in st.session_state:
        st.session_state.board = None
        st.session_state.path = None
        st.session_state.step_index = 0

    if st.button("Tìm đường đi"):
        with st.spinner("Đang tìm đường đi..."):
            board, path = knight_tour(n, start_x, start_y)
            time.sleep(0.5)
            st.session_state.board = board
            st.session_state.path = path
            st.session_state.step_index = 0

    if st.session_state.board is not None and st.session_state.path is not None:
        st.success("Đã tìm thấy đường đi!")
        fig = draw_board(st.session_state.board, st.session_state.path, st.session_state.step_index, start_x, start_y)
        st.pyplot(fig)

        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("Bước trước") and st.session_state.step_index > 0:
                st.session_state.step_index -= 1
        with col_next:
            if st.button("Bước sau") and st.session_state.step_index < n * n - 1:
                st.session_state.step_index += 1

        st.markdown(f'<div class="path-box">Đường đi đầy đủ: {st.session_state.path}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="info-box">Cách đọc: Số trên ô là thứ tự bước (0 là điểm bắt đầu, màu đỏ). '
            'Ô xanh nhạt là các ô đã đi qua. Mũi tên xanh chỉ hướng di chuyển.</div>',
            unsafe_allow_html=True
        )
    elif st.session_state.board is not None:
        st.error("Không tìm được đường đi! Hãy thử vị trí khác nhé :')))")


if __name__ == "__main__":
    main()