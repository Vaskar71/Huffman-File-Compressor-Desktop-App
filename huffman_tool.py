# huffman_tool.py
# A desktop application for Huffman encoding/decoding with an attractive Tkinter GUI using ttk.
# This version includes a fallback for file reading to handle non-UTF-8 encoded text files.

import os
import heapq                        # For priority queue operations in building the Huffman tree
from collections import Counter      # To count character frequencies in the text
import json                         # For serializing header information
import struct                       # For packing/unpacking binary data (header length)
import tkinter as tk                # Base Tkinter module
from tkinter import filedialog, messagebox
from tkinter import ttk             # Themed widgets for a good UI

# -----------------------------
# Block 1: Defining the Huffman Tree Node
# -----------------------------
class Node:
    def __init__(self, char, freq):
        self.char = char      # The character (or None for internal nodes)
        self.freq = freq      # Frequency of the character
        self.left = None      # Left child
        self.right = None     # Right child

    # Allow nodes to be compared based on frequency (required for heapq)
    def __lt__(self, other):
        return self.freq < other.freq

# -----------------------------
# Block 2: Build Frequency Table & Huffman Tree
# -----------------------------
def build_frequency_table(text):
    """Count the frequency of each character in the text."""
    return Counter(text)

def build_huffman_tree(freq_table):
    """Build the Huffman tree using a min-heap."""
    heap = [Node(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0] if heap else None

# -----------------------------
# Block 3: Generate Huffman Codes
# -----------------------------
def generate_codes(node, current_code="", code_table=None):
    """
    Recursively traverse the Huffman tree to generate binary codes for each character.
    """
    if code_table is None:
        code_table = {}

    if node is None:
        return code_table

    # If the node is a leaf, assign its code (handle single-node tree)
    if node.char is not None:
        code_table[node.char] = current_code or "0"
        return code_table

    generate_codes(node.left, current_code + "0", code_table)
    generate_codes(node.right, current_code + "1", code_table)
    return code_table

# -----------------------------
# Block 4: Encode Text & Create Bit Stream
# -----------------------------
def encode_text(text, code_table):
    """Convert the text into a string of bits using the Huffman code table."""
    return "".join(code_table[char] for char in text)

def pad_encoded_text(encoded_text):
    """
    Pad the encoded text with extra zeros so its length is a multiple of 8.
    Returns the padded text and the number of padding bits added.
    """
    extra_padding = 8 - (len(encoded_text) % 8)
    if extra_padding == 8:
        extra_padding = 0  # No padding needed if already a multiple of 8
    padded_encoded_text = encoded_text + "0" * extra_padding
    return padded_encoded_text, extra_padding

def get_byte_array(padded_encoded_text):
    """Convert the padded bit string into a bytearray."""
    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))
    return b

# -----------------------------
# Block 5: Compress File (Write Compressed Output)
# -----------------------------
def compress_file(input_path, output_path):
    try:
        # Try reading with UTF-8; if that fails, fall back to Latin-1.
        try:
            with open(input_path, "r", encoding="utf-8") as file:
                text = file.read()
        except UnicodeDecodeError:
            with open(input_path, "r", encoding="latin-1") as file:
                text = file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file: {e}")
        return

    if not text:
        messagebox.showwarning("Warning", "Input file is empty!")
        return

    # Build the frequency table and Huffman tree, then generate codes.
    freq_table = build_frequency_table(text)
    huffman_tree = build_huffman_tree(freq_table)
    code_table = generate_codes(huffman_tree)
    
    # Encode the text using the Huffman code table.
    encoded_text = encode_text(text, code_table)
    padded_encoded_text, extra_padding = pad_encoded_text(encoded_text)
    byte_array = get_byte_array(padded_encoded_text)
    
    # Creating header information to help during decompression.
    header = {
        "freq": dict(freq_table),   # Convert Counter to a dict for JSON serialization.
        "padding": extra_padding
    }
    header_json = json.dumps(header)
    header_bytes = header_json.encode("utf-8")
    header_length = len(header_bytes)
    
    try:
        with open(output_path, "wb") as output:
            # Write header length (4 bytes), then the header, then the compressed data.
            output.write(struct.pack("I", header_length))
            output.write(header_bytes)
            output.write(byte_array)
    except Exception as e:
        messagebox.showerror("Error", f"Could not write output file: {e}")
        return

    messagebox.showinfo("Success", "File compressed successfully!")

# -----------------------------
# Block 6: Decompress File (Read and Decode)
# -----------------------------
def decompress_file(input_path, output_path):
    try:
        with open(input_path, "rb") as file:
            header_length_bytes = file.read(4)
            if len(header_length_bytes) < 4:
                raise Exception("Invalid file format or corrupted file.")
            header_length = struct.unpack("I", header_length_bytes)[0]
            
            header_bytes = file.read(header_length)
            header_json = header_bytes.decode("utf-8")
            header = json.loads(header_json)
            freq_table = header["freq"]
            extra_padding = header["padding"]
            
            compressed_data = file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Could not read compressed file: {e}")
        return

    if not compressed_data:
        messagebox.showwarning("Warning", "Compressed file is empty!")
        return

    # Rebuild the Huffman tree from the stored frequency table.
    huffman_tree = build_huffman_tree(freq_table)
    
    # Convert the compressed byte data back into a bit string.
    bit_string = "".join(bin(byte)[2:].rjust(8, '0') for byte in compressed_data)
    
    # Remove the extra padding bits added during compression.
    if extra_padding > 0:
        bit_string = bit_string[:-extra_padding]
    
    # Decode the bit string using the Huffman tree.
    decoded_text = ""
    current_node = huffman_tree
    for bit in bit_string:
        current_node = current_node.left if bit == "0" else current_node.right
        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = huffman_tree

    try:
        with open(output_path, "w", encoding="utf-8") as output:
            output.write(decoded_text)
    except Exception as e:
        messagebox.showerror("Error", f"Could not write decompressed file: {e}")
        return

    messagebox.showinfo("Success", "File decompressed successfully!")

# -----------------------------
# Block 7: Building the Desktop GUI
# -----------------------------
def create_gui():
    root = tk.Tk()
    root.title("Huffman Compression Tool")
    root.geometry("500x300")
    
    # Use a modern theme for the UI.
    style = ttk.Style(root)
    style.theme_use("clam")
    
    # Header Frame.
    header_frame = ttk.Frame(root, padding="10")
    header_frame.grid(row=0, column=0, sticky="ew")
    header_label = ttk.Label(header_frame, text="Huffman Compression Tool", font=("Helvetica", 18, "bold"))
    header_label.pack()
    
    # Button Frame for actions.
    button_frame = ttk.Frame(root, padding="10")
    button_frame.grid(row=1, column=0, sticky="nsew")
    
    # Status Label (to display current operation status).
    status_label = ttk.Label(root, text="Welcome! Please choose an action.", relief="sunken", anchor="w", padding=5)
    status_label.grid(row=2, column=0, sticky="ew", padx=10, pady=(0,10))
    
    # Define actions as inner functions so they have access to 'root' and 'status_label'.
    def compress_action():
        input_path = filedialog.askopenfilename(
            title="Select file to compress",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not input_path:
            return
        output_path = filedialog.asksaveasfilename(
            title="Save compressed file as",
            defaultextension=".huff",
            filetypes=[("Huffman Compressed", "*.huff"), ("All Files", "*.*")]
        )
        if not output_path:
            return
        status_label.config(text="Compressing file...")
        root.update_idletasks()
        compress_file(input_path, output_path)
        status_label.config(text="Compression finished.")
    
    def decompress_action():
        input_path = filedialog.askopenfilename(
            title="Select file to decompress",
            filetypes=[("Huffman Compressed", "*.huff"), ("All Files", "*.*")]
        )
        if not input_path:
            return
        output_path = filedialog.asksaveasfilename(
            title="Save decompressed file as",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not output_path:
            return
        status_label.config(text="Decompressing file...")
        root.update_idletasks()
        decompress_file(input_path, output_path)
        status_label.config(text="Decompression finished.")
    
    # Create attractive, well-spaced buttons using ttk.
    compress_btn = ttk.Button(button_frame, text="Compress File", command=compress_action)
    compress_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
    decompress_btn = ttk.Button(button_frame, text="Decompress File", command=decompress_action)
    decompress_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    
    # Configure grid to ensure proper resizing.
    root.columnconfigure(0, weight=1)
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
