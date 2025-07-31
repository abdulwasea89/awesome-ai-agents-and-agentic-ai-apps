import chess
import chess.svg
import streamlit as st
from autogen import ConversableAgent, register_function

# ---------- STREAMLIT SESSION STATE ----------
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = None
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "made_move" not in st.session_state:
    st.session_state.made_move = False
if "board_svg" not in st.session_state:
    st.session_state.board_svg = None
if "move_history" not in st.session_state:
    st.session_state.move_history = []
if "max_turns" not in st.session_state:
    st.session_state.max_turns = 5

st.sidebar.title("Chess Agent Configuration")
gemini_api_key = st.sidebar.text_input("Enter your Gemini API key:", type="password")
if gemini_api_key:
    st.session_state.gemini_api_key = gemini_api_key
    st.sidebar.success("Gemini API key saved!")

st.sidebar.info("""
For a full chess game with potential checkmate, use max_turns > 200.
But that may take a lot of time. For demo use 5-10 turns.
""")

max_turns_input = st.sidebar.number_input(
    "Enter the number of turns (max_turns):",
    min_value=1,
    max_value=1000,
    value=st.session_state.max_turns,
    step=1
)

if max_turns_input:
    st.session_state.max_turns = max_turns_input
    st.sidebar.success(f"Max turns set to {st.session_state.max_turns}!")

st.title("Chess with Gemini Agents")

# ---------- MOVE FUNCTIONS ----------
def available_moves() -> str:
    available_moves = [str(move) for move in st.session_state.board.legal_moves]
    return "Available moves are: " + ",".join(available_moves)

def execute_move(move: str) -> str:
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move not in st.session_state.board.legal_moves:
            return f"Invalid move: {move}. Please call available_moves() to see valid moves."
        
        # Update board
        st.session_state.board.push(chess_move)
        st.session_state.made_move = True

        # Generate board visualization
        board_svg = chess.svg.board(
            st.session_state.board,
            arrows=[(chess_move.from_square, chess_move.to_square)],
            fill={chess_move.from_square: "gray"},
            size=400
        )
        st.session_state.board_svg = board_svg
        st.session_state.move_history.append(board_svg)

        # Get move info
        moved_piece = st.session_state.board.piece_at(chess_move.to_square)
        piece_unicode = moved_piece.unicode_symbol()
        piece_type_name = chess.piece_name(moved_piece.piece_type)
        piece_name = piece_type_name.capitalize() if piece_unicode.isupper() else piece_type_name
        
        from_square = chess.SQUARE_NAMES[chess_move.from_square]
        to_square = chess.SQUARE_NAMES[chess_move.to_square]
        move_desc = f"Moved {piece_name} ({piece_unicode}) from {from_square} to {to_square}."

        if st.session_state.board.is_checkmate():
            winner = 'White' if st.session_state.board.turn == chess.BLACK else 'Black'
            move_desc += f"\nCheckmate! {winner} wins!"
        elif st.session_state.board.is_stalemate():
            move_desc += "\nGame ended in stalemate!"
        elif st.session_state.board.is_insufficient_material():
            move_desc += "\nGame ended - insufficient material!"
        elif st.session_state.board.is_check():
            move_desc += "\nCheck!"

        return move_desc
    except ValueError:
        return f"Invalid move format: {move}. Please use UCI format (e.g., 'e2e4')."

def check_made_move(msg):
    if st.session_state.made_move:
        st.session_state.made_move = False
        return True
    return False


# ---------- GEMINI AGENTS ----------
if st.session_state.gemini_api_key:
    try:
        # ✅ FIX: Use config_list with Gemini API info
        config_list_gemini = [
            {
                "model": "gemini-2.5-pro",      # or gemini-2.0-flash if available
                "api_key": st.session_state.gemini_api_key,
                "api_type": "google"
            }
        ]

        agent_white = ConversableAgent(
            name="Agent_White",  
            system_message="You are a professional chess player and you play as white. "
                           "First call available_moves() to get legal moves, "
                           "then call execute_move(move) to make a move.",
            llm_config={"config_list": config_list_gemini},
        )

        agent_black = ConversableAgent(
            name="Agent_Black",  
            system_message="You are a professional chess player and you play as black. "
                           "First call available_moves() to get legal moves, "
                           "then call execute_move(move) to make a move.",
            llm_config={"config_list": config_list_gemini},
        )

        game_master = ConversableAgent(
            name="Game_Master",  
            llm_config=False,
            is_termination_msg=check_made_move,
            default_auto_reply="Please make a move.",
            human_input_mode="NEVER",
        )

        # Register functions for both agents
        for agent in [agent_white, agent_black]:
            register_function(execute_move, caller=agent, executor=game_master,
                              name="execute_move", description="Make a move on the board.")
            register_function(available_moves, caller=agent, executor=game_master,
                              name="available_moves", description="Get all legal moves.")

        # Connect agents for turn-taking
        agent_white.register_nested_chats(
            trigger=agent_black,
            chat_queue=[{"sender": game_master, "recipient": agent_white, "summary_method": "last_msg"}]
        )
        agent_black.register_nested_chats(
            trigger=agent_white,
            chat_queue=[{"sender": game_master, "recipient": agent_black, "summary_method": "last_msg"}]
        )

        # ---------- STREAMLIT UI ----------
        st.info("""
        This chess game is played between **two Gemini agents**:
        - **Agent White**: Gemini AI controlling white pieces  
        - **Agent Black**: Gemini AI controlling black pieces  

        Managed by **Game Master** that validates and updates the board.
        """)

        initial_board_svg = chess.svg.board(st.session_state.board, size=300)
        st.subheader("Initial Board")
        st.image(initial_board_svg)

        if st.button("Start Game"):
            st.session_state.board.reset()
            st.session_state.made_move = False
            st.session_state.move_history = []
            st.session_state.board_svg = chess.svg.board(st.session_state.board, size=300)
            st.info("The Gemini AI agents will now play against each other...")
            st.write("Game started! White's turn.")

            chat_result = agent_black.initiate_chat(
                recipient=agent_white, 
                message="Let's play chess! You go first.",
                max_turns=st.session_state.max_turns,
                summary_method="reflection_with_llm"
            )
            st.markdown(chat_result.summary)

            # Move history
            st.subheader("Move History")
            for i, move_svg in enumerate(st.session_state.move_history):
                move_by = "Agent White" if i % 2 == 0 else "Agent Black"
                st.write(f"Move {i + 1} by {move_by}")
                st.image(move_svg)

        if st.button("Reset Game"):
            st.session_state.board.reset()
            st.session_state.made_move = False
            st.session_state.move_history = []
            st.session_state.board_svg = None
            st.write("Game reset! Click 'Start Game' to begin a new game.")

    except Exception as e:
        st.error(f"Error: {e}. Check your Gemini API key and try again.")

else:
    st.warning("Please enter your Gemini API key in the sidebar to start the game.")
