# MIPS Processor Simulator

A simple 32-bit **MIPS processor simulator** implemented in Python, supporting separate instruction and data memories and executing instructions using the classic **five pipeline stages**.

## 🚀 Overview

This project simulates the behavior of a basic MIPS CPU. It reads instructions from an external text file, processes them through the CPU pipeline, interacts with data memory, and displays the results.

The simulator implements the following stages:

1. **Fetch** – Read instruction from instruction memory  
2. **Decode** – Determine operation and operands  
3. **Execute** – Perform ALU or arithmetic operations  
4. **Memory** – Read/write data memory if needed  
5. **Writeback** – Store results into registers  

This makes the project helpful for learning how CPU execution works internally.

---

## 📁 Repository Structure

---

## ✨ Features

- 32-bit MIPS architecture simulation  
- Fully separated instruction and data memory  
- Implements 5-stage execution pipeline  
- Easy to modify instructions via `.txt` files  
- Written entirely in Python (no external libraries)  
- Good for learning, debugging, and experimenting with CPU architecture concepts  

---

## 🛠️ Getting Started

### ✅ Requirements
- Python **3.x**

### ▶️ Running the Simulator

1. Clone the repo:
   ```bash
   git clone https://github.com/Ahilnandan/Processor.git
   cd Processor


