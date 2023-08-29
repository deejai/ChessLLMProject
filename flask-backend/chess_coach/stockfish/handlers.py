from queue import Queue
import subprocess
from threading import Lock
import os
from chess_coach.stockfish.utilities import ROOT_DIR

class StockfishInstance:
    def __init__(self):
        stockfish_executable = None
        if os.name == 'posix':  # Unix-like OS (Linux, macOS)
            stockfish_executable = ROOT_DIR / "stockfish/stockfish"
        elif os.name == 'nt':  # Windows
            stockfish_executable = ROOT_DIR / "stockfish/stockfish.exe"

        if stockfish_executable:
            self.proc = subprocess.Popen(
                stockfish_executable,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )
        else:
            raise Exception("Unsupported OS")

        self.lock = Lock()

        # Clear the initial messages from stdout
        line = self.proc.stdout.readline().strip()
        print(line)

    def send_command(self, command):
        with self.lock:
            self.proc.stdin.write(f"{command}\n")
            self.proc.stdin.flush()

    def read_output(self):
        with self.lock:
            return self.proc.stdout.readline().strip()

    def get_board_ascii(self, fen):
        self.send_command(f"position fen {fen}")
        self.send_command("d")
        ascii_board = []
        capture = False
        while True:
            output = self.read_output().strip()
            print(output)

            if not capture and output == "+---+---+---+---+---+---+---+---+":
                capture = True

            if capture:
                ascii_board.append(output)

                if output[:len("Checkers:")] == "Checkers:":
                    break

        return '\n'.join(ascii_board)

    def get_fen(self, fen):
        self.send_command(f"position fen {fen}")
        self.send_command("d")
        while True:
            output = self.read_output()
            if "Fen: " in output:
                return output.split("Fen: ")[1]

    def get_top_moves(self, fen, num_moves=10, time_limit=1000):
        self.send_command(f"position fen {fen}")
        self.send_command(f"setoption name MultiPV value {num_moves}")
        self.send_command(f"go movetime {time_limit}")

        top_moves = []
        while True:
            output = self.read_output()
            if "bestmove" in output:
                break

            if " pv " in output:
                parts = output.strip().split(" ")
                idx = parts.index('pv')

                # Capture the sequence of moves that follow the initial move
                move_sequence = parts[idx + 1:]
                primary_move = move_sequence[0]
                following_moves = move_sequence[1:]

                if following_moves:
                    move_str = f"{primary_move} ({', '.join(following_moves)})"
                else:
                    move_str = primary_move

                top_moves.append(move_str)

            if len(top_moves) >= num_moves:
                break

        top_moves_str = "\n".join(top_moves)
        return top_moves_str

class StockfishPool:
    def __init__(self, size):
        self.pool = Queue()
        for _ in range(size):
            instance = StockfishInstance()
            self.pool.put(instance)

    def get_instance(self):
        return self.pool.get()

    def release_instance(self, instance):
        self.pool.put(instance)
