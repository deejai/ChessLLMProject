from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()

def is_valid_fen(fen):
    fields = fen.strip().split(' ')
    if len(fields) != 6:
        return False
    
    rows = fields[0].split('/')
    if len(rows) != 8:
        return False
    
    for row in rows:
        empty_count = 0
        for c in row:
            if c.isdigit():
                empty_count += int(c)
            elif c.isalpha() and c.lower() in 'prnbqk':
                empty_count += 1
            else:
                return False
        if empty_count != 8:
            return False
            
    if fields[1] not in ('w', 'b'):
        return False
    
    if not set(fields[2]).issubset(set('KQkq-')):
        return False
    
    if fields[3] != '-' and not (fields[3][0] in 'abcdefgh' and fields[3][1] in '36'):
        return False
    
    if not fields[4].isdigit() or not fields[5].isdigit():
        return False

    return True

def fen_to_description(fen):
    piece_names = {
        'p': 'Pawn',
        'r': 'Rook',
        'n': 'Knight',
        'b': 'Bishop',
        'q': 'Queen',
        'k': 'King',
        'P': 'Pawn',
        'R': 'Rook',
        'N': 'Knight',
        'B': 'Bishop',
        'Q': 'Queen',
        'K': 'King'
    }
    
    board, turn, castling, en_passant, halfmove, fullmove = fen.split(' ')
    rows = board.split('/')
    description = "Board layout:\n"
    for row_num, row in enumerate(reversed(rows)):
        description += f"Rank {8 - row_num}: "
        for char in row:
            if char.isdigit():
                for i in range(int(char)):
                    description += "[  ] "
            else:
                piece = piece_names[char]
                color = "White" if char.isupper() else "Black"
                description += f"[{color[0]}{piece[0]}] "
        description += "\n"
    
    description += f"\nTurn: {'White' if turn == 'w' else 'Black'}"
    description += f"\nCastling availability: {castling if castling != '-' else 'None'}"
    description += f"\nEn passant square: {en_passant if en_passant != '-' else 'None'}"
    description += f"\nHalfmove clock: {halfmove}"
    description += f"\nFullmove number: {fullmove}"
    
    return description
