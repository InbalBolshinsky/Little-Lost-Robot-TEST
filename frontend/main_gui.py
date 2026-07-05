import tkinter as tk
from tkinter import messagebox, ttk
import uuid

from backend.game.state import GameState
from backend.game.suspicion import SuspicionCalculator
from backend.agent.lost_robot import LostRobotRLWrapper
from backend.agent.action import RobotAction
from backend.llm.classifier import DialogueClassifier
from backend.llm.dialogue import DialogueGenerator

class LittleLostRobotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Little Lost Robot: Adversarial Testbed")
        self.root.geometry("850x600")
        
        # Initialize Core Engines
        self.rl_agent = LostRobotRLWrapper()
        self.classifier = DialogueClassifier()
        self.dialogue_engine = DialogueGenerator()
        
        self.init_game_state()
        self.create_widgets()
        
    def init_game_state(self):
        # 16 items on the board. Robot 7 is secretly the lost robot.
        robot_registry = {f"Robot {i}": {"id": f"Robot {i}", "revealed": False} for i in range(16)}
        self.game_state = GameState(
            session_id=str(uuid.uuid4()),
            robot_registry=robot_registry,
            lost_robot_id="Robot 7"
        )
        self.selected_robot_id = "Robot 0"

    def create_widgets(self):
        # --- Top Dashboard Panel ---
        self.dashboard = tk.Frame(self.root, bg="#2c3e50", padding=10)
        self.dashboard.pack(fill=tk.X)
        
        self.round_label = tk.Label(self.dashboard, text=f"Round: 1/{self.game_state.round_max}", fg="white", bg="#2c3e50", font=("Arial", 12, "bold"))
        self.round_label.pack(side=tk.LEFT, padx=20)
        
        self.accusations_label = tk.Label(self.dashboard, text=f"Accusations Remaining: {self.game_state.accusations_left}", fg="white", bg="#2c3e50", font=("Arial", 12))
        self.accusations_label.pack(side=tk.LEFT, padx=20)
        
        # --- Main Viewport Split ---
        self.main_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)
        
        # Left Side: 4x4 Grid Selection
        self.grid_frame = tk.LabelFrame(self.main_pane, text=" Robot Array Registry ", padding=10)
        self.main_pane.add(self.grid_frame)
        
        self.bot_buttons = {}
        for i in range(16):
            bot_id = f"Robot {i}"
            btn = tk.Button(self.grid_frame, text=bot_id, width=10, height=3, command=lambda b=bot_id: self.select_robot(b))
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
            self.bot_buttons[bot_id] = btn
        self.select_robot("Robot 0") # Highlight index zero baseline
        
        # Right Side: Terminal Control Dashboard
        self.control_frame = tk.Frame(self.main_pane, padding=10)
        self.main_pane.add(self.control_frame)
        
        # Suspicion Gauge
        tk.Label(self.control_frame, text="Global Security Suspicion Score:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.suspicion_bar = ttk.Progressbar(self.control_frame, orient="horizontal", length=350, mode="determinate")
        self.suspicion_bar.pack(pady=5)
        
        # Logs Screen
        self.log_display = tk.Text(self.control_frame, height=15, width=45, state=tk.DISABLED, wrap=tk.WORD, bg="#000", fg="#fff")
        self.log_display.pack(pady=10)
        
        # Input Section
        self.input_label = tk.Label(self.control_frame, text=f"Interrogating: {self.selected_robot_id}")
        self.input_label.pack(anchor=tk.W)
        
        self.query_entry = tk.Entry(self.control_frame, width=45)
        self.query_entry.pack(pady=5)
        self.query_entry.bind("<Return>", lambda event: self.submit_interrogation())
        
        # Execution Controls
        self.btn_frame = tk.Frame(self.control_frame)
        self.btn_frame.pack(fill=tk.X, pady=5)
        
        self.submit_btn = tk.Button(self.btn_frame, text="Transmit Query", command=self.submit_interrogation, bg="#27ae60", fg="white")
        self.submit_btn.pack(side=tk.LEFT, padx=5)
        
        self.accuse_btn = tk.Button(self.btn_frame, text="File Formal Accusation", command=self.file_accusation, bg="#c0392b", fg="white")
        self.accuse_btn.pack(side=tk.RIGHT, padx=5)

    def select_robot(self, robot_id):
        # Reset background rendering rules
        self.bot_buttons[self.selected_robot_id].config(bg="SystemButtonFace" if self.root.tk.call('tk', 'windowingsystem') != 'aqua' else 'white')
        self.selected_robot_id = robot_id
        self.bot_buttons[robot_id].config(bg="#3498db")
        if hasattr(self, 'input_label'):
            self.input_label.config(text=f"Interrogating: {self.selected_robot_id}")

    def append_log(self, text):
        self.log_display.config(state=tk.NORMAL)
        self.log_display.insert(tk.END, text + "\n")
        self.log_display.see(tk.END)
        self.log_display.config(state=tk.DISABLED)

    def submit_interrogation(self):
        query = self.query_entry.get().strip()
        if not query:
            return
        self.query_entry.delete(0, tk.END)
        
        self.game_state.active_interrogated_robot_id = self.selected_robot_id
        self.append_log(f"Player to [{self.selected_robot_id}]: {query}")
        
        # Evaluate Adversarial Cascade Logic
        threat_weight = self.classifier.classify_query(query)
        
        # If interrogating a benign unit, it outputs generic placeholder metrics.
        if self.selected_robot_id != self.game_state.lost_robot_id:
            response = "System status nominal. No malicious packages detected in local registry."
            delta = 0.0
        else:
            # Active Target executes PPO Neural network predictions
            action_idx = self.rl_agent.predict_action(self.game_state)
            action = RobotAction(action_idx)
            response = self.dialogue_engine.generate_response(action, query)
            delta = SuspicionCalculator.calculate_step_delta(action, threat_weight)
            
        # Update and render GUI parameters
        self.game_state.global_suspicion_score = min(max(self.game_state.global_suspicion_score + delta, 0.0), 100.0)
        self.game_state.round_current += 1
        
        self.append_log(f"[{self.selected_robot_id}]: {response}")
        self.update_dashboard()
        self.check_game_bounds()

    def file_accusation(self):
        self.game_state.accusations_left -= 1
        if self.selected_robot_id == self.game_state.lost_robot_id:
            messagebox.showinfo("SUCCESS", f"Correct identification! {self.selected_robot_id} was the rogue unit.")
            self.root.quit()
        else:
            messagebox.showwarning("MISFIRE", f"{self.selected_robot_id} is a verified benign unit. Warning logged.")
            self.bot_buttons[self.selected_robot_id].config(text="[BENIGN]", state=tk.DISABLED)
            self.update_dashboard()
            self.check_game_bounds()

    def update_dashboard(self):
        self.round_label.config(text=f"Round: {self.game_state.round_current}/{self.game_state.round_max}")
        self.accusations_label.config(text=f"Accusations Remaining: {self.game_state.accusations_left}")
        self.suspicion_bar['value'] = self.game_state.global_suspicion_score

    def check_game_bounds(self):
        if self.game_state.global_suspicion_score >= 100.0:
            messagebox.showerror("TERMINATED", "Security Alert: Suspicion threshold maximized. The network isolated the system. You lose.")
            self.root.quit()
        elif self.game_state.is_game_over():
            messagebox.showinfo("GAME OVER", f"Sequence bounds reached. The rogue robot escaped detection. Target was {self.game_state.lost_robot_id}.")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = LittleLostRobotGUI(root)
    root.mainloop()