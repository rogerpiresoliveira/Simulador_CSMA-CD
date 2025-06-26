import tkinter as tk
from tkinter import messagebox
import random
import math
import threading
import time

C = 3e8  # Speed of light in m/s
MIN_FRAME_SIZE = 64 * 8  # in bits
MAX_FRAME_SIZE = 1518 * 8  # in bits

class Transmitter:
    def __init__(self, id, frames):
        self.id = id
        self.frames = frames
        self.retries = 0

def calculate_propagation_delay(length, factor):
    return length / (C * factor)

def calculate_slot_time(length, factor):
    return 2 * calculate_propagation_delay(length, factor)

def transmission_time(frame_size_bits, bandwidth):
    return frame_size_bits / bandwidth

def generate_frame_size():
    size = int(random.normalvariate((MIN_FRAME_SIZE + MAX_FRAME_SIZE) / 2, 200))
    return max(MIN_FRAME_SIZE, min(size, MAX_FRAME_SIZE))

class CSMACDSimulator:
    def __init__(self, root):
        self.root = root
        root.title("CSMA/CD Simulator")

        self.create_widgets()

    def create_widgets(self):
        labels = [
            "Number of Transmitters:",
            "Frames per Transmitter:",
            "Bandwidth (Mbps):",
            "Cable Length (meters):",
            "Cable Speed Factor (0.6 - 0.7):",
            "Max Retransmissions:"
        ]

        defaults = [5, 3, 10, 1000, 0.66, 10]
        self.entries = []

        for i, (text, default) in enumerate(zip(labels, defaults)):
            tk.Label(self.root, text=text).grid(row=i, column=0, sticky="e")
            entry = tk.Entry(self.root)
            entry.insert(0, str(default))
            entry.grid(row=i, column=1)
            self.entries.append(entry)

        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.run_simulation)
        self.start_button.grid(row=len(labels), column=0, columnspan=2)

        self.output = tk.Text(self.root, height=25, width=80)
        self.output.grid(row=len(labels)+1, column=0, columnspan=2)

    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def run_simulation(self):
        try:
            num_transmitters = int(self.entries[0].get())
            frames_per_transmitter = int(self.entries[1].get())
            bandwidth_mbps = float(self.entries[2].get())
            bandwidth = bandwidth_mbps * 1e6  # Convert to bps
            cable_length = float(self.entries[3].get())
            speed_factor = float(self.entries[4].get())
            max_retries = int(self.entries[5].get())

            if not (0 < speed_factor <= 1):
                raise ValueError("Speed factor must be greater than 0 and less than 1.0.")

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        self.output.delete(1.0, tk.END)

        threading.Thread(target=self.simulate, args=(num_transmitters,
                                                     frames_per_transmitter,
                                                     bandwidth, cable_length,
                                                     speed_factor, max_retries), daemon=True).start()

    def simulate(self, num_transmitters, frames_per_transmitter, bandwidth, cable_length, speed_factor, max_retries):
        transmitters = [Transmitter(i, frames_per_transmitter) for i in range(num_transmitters)]
        slot_time = calculate_slot_time(cable_length, speed_factor)
        prop_delay = calculate_propagation_delay(cable_length, speed_factor)

        self.log(f"Slot time: {slot_time * 1e6:.2f} µs | Propagation delay: {prop_delay * 1e6:.2f} µs")

        total_frames = num_transmitters * frames_per_transmitter
        collisions = 0
        total_retries = 0

        # Event queue: stores tuples of (time, transmitter)
        event_queue = []

        # Initialize randomly first attempts
        for t in transmitters:
            if t.frames > 0:
                delay = random.uniform(0, slot_time) # Random delay to "try" to start transmitting
                event_queue.append((delay, t))
                # event_queue = [
                # (time, transmiter_ID)
                # (10.0, transmiter__A),
                # (12.0, transmiter__B), 
                # (25.0, transmiter__C),
                # (27.0, transmiter__D)
                # ]

        while event_queue:
            # Sort by time
            event_queue.sort(key=lambda x: x[0])
            batch_time = event_queue[0][0]

            # Get all transmitters attempting at the same time
            batch = [event for event in event_queue if abs(event[0] - batch_time) < prop_delay]
            event_queue = [event for event in event_queue if event not in batch]

            if len(batch) > 1:
                # Collision occurred
                collisions += 1
                self.log(f"Collision among {[t.id for _, t in batch]} at {batch_time * 1e6:.2f} µs")

                for _, t in batch:
                    t.retries += 1
                    total_retries += 1
                    if t.retries > max_retries:
                        self.log(f"Transmitter {t.id}: Dropped frame after {max_retries} retries.")
                        t.frames -= 1
                        t.retries = 0
                    else:
                        # Value from 0 to 2^10
                        # The t.retries is not controlled, so we truncate to 10
                        backoff_time = random.randint(0, 2 ** min(t.retries, 10) - 1) * slot_time
                        # 1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 1023, 1023...
                        event_queue.append((batch_time + backoff_time, t))
            else:
                # Successful transmission
                _, t = batch[0]
                frame_size = generate_frame_size()
                tx_time = transmission_time(frame_size, bandwidth)
                self.log(f"Transmitter {t.id} sends {frame_size // 8} bytes. Duration: {tx_time * 1e6:.2f} µs")
                time.sleep(tx_time / 10_000) # Channel is busy
                t.frames -= 1
                t.retries = 0

                # Schedule next frame if there are more
                if t.frames > 0:
                    delay = random.uniform(0, slot_time)
                    event_queue.append((batch_time + tx_time + delay, t))

        avg_retries = total_retries / total_frames if total_frames > 0 else 0

        self.log("\n--- Simulation Statistics ---")
        self.log(f"Total frames sent: {total_frames}")
        self.log(f"Total collisions: {collisions}")
        self.log(f"Average retries per frame: {avg_retries:.2f}")
        self.log("Simulation complete.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CSMACDSimulator(root)
    root.mainloop()
