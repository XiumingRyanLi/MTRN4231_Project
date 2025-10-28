# chess_to_coords.py

def get_real_world_coords(square: str):
    # Define corner coordinates
    A1 = (309, -818.0)
    H1 = (309, -519.9)
    A8 = (4.9, -818.0)
    H8 = (4.9, -519.9)

    # Extract file (A-H) and rank (1-8)
    file = square[0].upper()
    rank = int(square[1])

    if file not in "ABCDEFGH" or rank not in range(1, 9):
        raise ValueError("Invalid square. Use like 'e4' or 'A1'.")

    # Calculate step size
    dx_per_file = (H1[0] - A1[0]) / 7
    dy_per_file = (H1[1] - A1[1]) / 7
    dx_per_rank = (A8[0] - A1[0]) / 7
    dy_per_rank = (A8[1] - A1[1]) / 7

    # Compute offsets
    file_index = ord(file) - ord('A')
    rank_index = rank - 1

    x = A1[0] + file_index * dx_per_file + rank_index * dx_per_rank
    y = A1[1] + file_index * dy_per_file + rank_index * dy_per_rank

    return x, y


if __name__ == "__main__":
    while True:
        square = input("Enter chess square (e.g., e4) or 'q' to quit: ").strip()
        if square.lower() == 'q':
            break
        try:
            x, y = get_real_world_coords(square)
            print(f"{square.upper()} → X: {x:.2f} mm, Y: {y:.2f} mm\n")
        except ValueError as e:
            print(e)
