# Huffman Compression Tool Desktop App

---

## **1. Overview**

The **Huffman Compression Tool** is a desktop application designed to compress and decompress plain text files using Huffman encoding—a lossless data compression algorithm. This tool demonstrates practical applications of algorithm design, file I/O operations, error handling, and graphical user interface (GUI) development in Python. It is particularly useful for understanding how variable-length encoding can reduce file size based on character frequency. It's one of my most favourite algorithm , i really enjoyed devoloping this classic algorithm.

---

<img width="382" alt="Image" src="https://github.com/user-attachments/assets/175e1106-c459-41e3-977f-a27ea9bffa33" />

## **2. Core Functionality**

### **2.1. Compression Process**

- **File Reading & Encoding Handling:**  
  This tool reads an input file (typically a `.txt` file) and attempts to decode it using UTF‑8 encoding. If the file contains non-UTF‑8 encoded characters, it automatically falls back to an alternative encoding (Latin‑1) to ensure robust file handling.

- **Frequency Analysis:**  
  Using Python's `collections.Counter`, the application calculates the frequency of each character in the text. This frequency table is essential for constructing the Huffman tree, as it determines which characters should receive shorter binary codes.

- **Huffman Tree Construction:**  
  This tool builds a binary tree (Huffman tree) by:
  - Initializing a min-heap where each node represents a character and its frequency.
  - Iteratively combining the two least frequent nodes into a new parent node until only one tree remains.
  - This tree structure guarantees that the most frequent characters are positioned closer to the root, resulting in shorter codes.

- **Code Generation:**  
  A recursive traversal of the Huffman tree generates a unique, prefix-free binary code for each character. This ensures that no code is a prefix of another, allowing for unambiguous decoding.

- **Encoding the Text:**  
  The original text is transformed into a long string of bits by replacing each character with its corresponding Huffman code. The resulting bit string is padded to ensure that its length is a multiple of 8, making it suitable for conversion into a byte array.

- **Header Creation:**  
  To facilitate decompression, a header is generated and prepended to the compressed data. The header, serialized in JSON format, contains the frequency table and the amount of padding added. This metadata is critical for accurately reconstructing the Huffman tree during decompression.

- **Output:**  
  The final output is a binary file (typically with a `.huff` extension) that includes:
  - A fixed-size header length indicator (4 bytes).
  - The JSON-serialized header.
  - The compressed byte array representing the original text.

<img width="184" alt="Image" src="https://github.com/user-attachments/assets/f0d529d3-1377-452c-a014-05f41ffc7356" />

### **2.2. Decompression Process**

- **Reading the Header:**  
  The application starts by reading the first 4 bytes to determine the length of the header. It then parses the JSON header to retrieve the frequency table and padding information.

- **Reconstructing the Huffman Tree:**  
  Using the frequency table from the header, the tool rebuilds the original Huffman tree.

- **Decoding the Data:**  
  The compressed byte array is converted back into a bit string. The extra padding bits are removed, and the tool traverses the Huffman tree bit by bit to decode the original characters.

- **Restoring the Original File:**  
  Finally, the decoded text is written back to a new output file, effectively reconstructing the original file content.

---

## **3. Technical Implementation**

### **3.1. Programming Language & Libraries**

- **Python 3:**  
  I devoloped this project in Python due to its simplicity, readability, and rich standard library.

- **Tkinter & ttk:**  
  The GUI is built using Tkinter along with the themed widgets provided by ttk. This creates an attractive and user-friendly interface.

- **Key Libraries:**
  - **heapq:** Implements a min-heap for efficient tree construction.
  - **collections.Counter:** Quickly counts character frequencies.
  - **json:** Serializes the header metadata for later use.
  - **struct:** Packs and unpacks binary data, specifically for managing the header length.
  
### **3.2. Code Structure & Organization**

- **Modular Design:**  
  The code is organized into functional blocks, each responsible for a specific aspect of the process:
  - **File I/O & Encoding:** Robust file reading with fallback mechanisms.
  - **Huffman Tree & Code Generation:** Building the tree and generating binary codes.
  - **Compression & Decompression Functions:** Core logic for encoding and decoding.
  - **GUI Implementation:** A modern and responsive interface that integrates all functionalities.

- **Error Handling:**  
  Try/except blocks and informative dialog messages ensure that users are notified of any issues, such as file reading errors or corrupted data.

- **User Feedback:**  
  The GUI provides status updates during compression and decompression processes, enhancing the user experience.

---

## **4. How to Use the Project**

### **4.1. Prerequisites**

- **Python 3 Installation:**  
  Ensure that Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/).

- **Tkinter Availability:**  
  Tkinter usually comes bundled with Python. If not, refer to your system’s package manager or Python documentation to install it.

### **4.2. Setting Up the Project**

1. **Download/Clone the Code:**  
   Save the source code as `huffman_tool.py` in a dedicated project directory (e.g., `HuffmanCompressor/`).

2. **Project Directory Structure:**
   ```
   HuffmanCompressor/
   ├── huffman_tool.py   # Main application file
   ├── README.md                    # Project overview and instructions
   └── requirements.txt             # (Optional) List of dependencies
   ```

3. **Optional Virtual Environment:**  
   Create and activate a virtual environment to manage dependencies if you plan to extend the project.

### **4.3. Running the Application**

1. **Open the Project in an IDE:**  
   Use Visual Studio Code, PyCharm, or any other preferred IDE to open the project folder.

2. **Run the Script:**  
   Open an integrated terminal in your IDE and execute:
   ```bash
   python huffman_tool.py
   ```

3. **Interact with the GUI:**  
   - **Compress File:**  
     Click the *Compress File* button, select a plain text file (e.g., a `.txt` file), and choose a destination to save the compressed file (with a `.huff` extension).
   - **Decompress File:**  
     Click the *Decompress File* button, select a `.huff` file, and specify an output file path for the decompressed text.

### **4.4. Troubleshooting and Tips**

- **File Encoding Issues:**  
  If you encounter errors like `"utf-8 codec can't decode byte"`, it means the file is not encoded in UTF‑8. The tool includes a fallback to Latin‑1 encoding, but you may need to verify the file's encoding or convert it to UTF‑8 using a text editor.

- **Error Messages:**  
  The application uses error dialogs to inform users of issues such as file read/write errors or corrupted files. Follow these messages to resolve any issues.

- **Extending the Tool:**  
  The modular code design allows easy extension. You can add support for additional file formats or integrate other compression algorithms.

---

## **5. Conclusion**

This Huffman Compression Tool is an excellent example of how classic algorithms can be applied in modern software development. It combines efficient data compression techniques with a user-friendly interface.

---
