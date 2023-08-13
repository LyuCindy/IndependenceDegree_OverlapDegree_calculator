# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 16:08:21 2023

@author: LyBabyGQ
"""
import tkinter as tk
import math
from tkinter import filedialog
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Independence and Coincidence Calculator")

        # Create file input widgets
        self.file1_label = tk.Label(master, text="File 1:")
        self.file1_label.grid(row=0, column=0)

        self.file1_entry = tk.Entry(master, width=30)
        self.file1_entry.grid(row=0, column=1)

        self.file1_button = tk.Button(master, text="Browse...", command=self.browse_file1)
        self.file1_button.grid(row=0, column=2)
        
      
        self.file2_label = tk.Label(master, text="File 2:")
        self.file2_label.grid(row=1, column=0)

        self.file2_entry = tk.Entry(master, width=30)
        self.file2_entry.grid(row=1, column=1)

        self.file2_button = tk.Button(master, text="Browse...", command=self.browse_file2)
        self.file2_button.grid(row=1, column=2)

        # Create independence calculator widgets
        self.independence_label = tk.Label(master, text="Independence Degree")
        self.independence_label.grid(row=2, column=0)

        self.independence_thresh_label = tk.Label(master, text="Threshold(Å):")
        self.independence_thresh_label.grid(row=3, column=0)

        self.independence_thresh_entry = tk.Entry(master, width=10)
        self.independence_thresh_entry.grid(row=3, column=1)

        self.independence_button = tk.Button(master, text="Calculate", command=self.calculate_independence)
        self.independence_button.grid(row=3, column=2)

        self.independence_result_label = tk.Label(master, text="")
        self.independence_result_label.grid(row=4, column=0, columnspan=3)

        # Create coincidence calculator widgets
        self.coincidence_label = tk.Label(master, text="Overlap Degree")
        self.coincidence_label.grid(row=2, column=3)

        self.coincidence_thresh_label = tk.Label(master, text="Threshold(Å):")
        self.coincidence_thresh_label.grid(row=3, column=3)

        self.coincidence_thresh_entry = tk.Entry(master, width=10)
        self.coincidence_thresh_entry.grid(row=3, column=4)

        self.coincidence_button = tk.Button(master, text="Calculate", command=self.calculate_coincidence)
        self.coincidence_button.grid(row=3, column=5)

        self.coincidence_result_label = tk.Label(master, text="")
        self.coincidence_result_label.grid(row=4, column=3, columnspan=3)

    def browse_file1(self):
        file_path = filedialog.askopenfilename()
        self.file1_entry.delete(0, tk.END)
        self.file1_entry.insert(0, file_path)

    def browse_file2(self):
        file_path = tk.filedialog.askopenfilename()
        self.file2_entry.delete(0, tk.END)
        self.file2_entry.insert(0, file_path)

    def calculate_independence(self):
        file1_path = self.file1_entry.get()
        with open(file1_path, 'r') as f:
          a_coords = []
          for line in f:
              x, y, z = line.strip().split()
              a_coords.append((float(x), float(y), float(z)))

        file2_path = self.file2_entry.get()
        with open(file2_path, 'r') as f:
          b_coords = []
          for line in f:
              x, y, z = line.strip().split()
              b_coords.append((float(x), float(y), float(z)))

        threshold = float(self.independence_thresh_entry.get())
        independence = self.calc_independence(a_coords, b_coords, threshold)

    def calculate_coincidence(self):
        file1_path = self.file1_entry.get()
        with open(file1_path, 'r') as f:
            a_coords = []
            for line in f:
                x, y, z = line.strip().split()
                a_coords.append((float(x), float(y), float(z)))

        file2_path = self.file2_entry.get()
        with open(file2_path, 'r') as f:
            b_coords = []
            for line in f:
                x, y, z = line.strip().split()
                b_coords.append((float(x), float(y), float(z)))

        threshold = float(self.coincidence_thresh_entry.get())
        coincidence = self.calc_coincidence(a_coords, b_coords, threshold)
     
    def calc_independence(self, a_coords, b_coords, threshold):
        num_a = len(a_coords)
        num_b = len(b_coords)
        no_overlap = True
        for i in range(num_a):
            for j in range(num_b):
                dx = b_coords[j][0] - a_coords[i][0]
                dy = b_coords[j][1] - a_coords[i][1]
                dz = b_coords[j][2] - a_coords[i][2]
                dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                if dist < 0.2:
                   self.independence_result_label.config(text="No independent occupancy phenomenon")
                   no_overlap = False
                   break
            if not no_overlap:
                break
        
        if no_overlap:
           distances = [[0.0 for j in range(num_b)] for i in range(num_a)]
           
           for i in range(num_a):
               for j in range(num_b):
                   dx = b_coords[j][0] - a_coords[i][0]
                   dy = b_coords[j][1] - a_coords[i][1]
                   dz = b_coords[j][2] - a_coords[i][2]
                   dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                   distances[i][j] = dist
           total_pairs = num_a * num_b 
           count = 0 
           for i in range(num_a):
               for j in range(num_b):
                   if distances[i][j] > threshold:
                      count += 1
           if count == 0:
              self.coincidence_result_label.config(text="No independent occupancy phenomenon")
           else:
              percentage = count / total_pairs * 100
              self.independence_result_label.config(text=f"ID(>{threshold}Å)% ={percentage:.2f}%")

    def calc_coincidence(self, a_coords, b_coords, threshold):
        matched_pairs = []
      
        for b_idx, b_coord in enumerate(b_coords):
            for a_idx, a_coord in enumerate(a_coords):
                dx = abs(b_coord[0] - a_coord[0])
                dy = abs(b_coord[1] - a_coord[1])
                dz = abs(b_coord[2] - a_coord[2])
                if dx <= 0.1 and dy <= 0.1 and dz <= 0.1:
                    matched_pairs.append((b_idx, a_idx))
      
        total_pairs = len(matched_pairs)
        count = 0
        for b_idx, a_idx in matched_pairs:
            dx = b_coords[b_idx][0] - a_coords[a_idx][0]
            dy = b_coords[b_idx][1] - a_coords[a_idx][1]
            dz = b_coords[b_idx][2] - a_coords[a_idx][2]
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist < threshold:
                count += 1
        if count == 0:
            self.coincidence_result_label.config(text="No competitive adsorption occupancy phenomenon")
        else:
            percentage = count / total_pairs * 100
            self.coincidence_result_label.config(text=f"OD(<{threshold}Å)% ={percentage:.2f}%")
    
     
     
if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
